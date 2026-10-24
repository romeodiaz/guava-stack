import AppKit
import Combine
import MachO
import ServiceManagement
import SwiftUI
import Darwin

let slots = ["head-chef", "line-cook"]
let efforts = ["Low", "Medium", "High", "xhigh", "Max"]

let tools = ["claude": "Claude Code", "codex": "Codex", "agy": "Antigravity CLI", "pi": "Pi"]

// One slot of one plan row in guava-router's slots.json, which sync-models.py writes from models.yaml.
struct Slot: Decodable {
    struct Fallback: Decodable { let name: String; let effort: String }
    let name: String
    let id: String
    let tool: String
    let fallback: Fallback?
}

struct Pick: Hashable {
    let name: String
    let tool: String
    let fallback: String?
    let id: String
    let plan: String  // the slots.json row it came from, which router-check.py tests it on

    func line(_ effort: String) -> String {
        let base = "\(name) (\(effort)) via \(tool)"
        return fallback.map { "\(base), falling back to \($0) when its usage runs out" } ?? base
    }
}

struct Hub {
    static var directory: URL {
        URL(fileURLWithPath: ProcessInfo.processInfo.environment["GUAVA_HUB"]
            ?? NSHomeDirectory() + "/.guava-hub", isDirectory: true)
    }

    var lines: [String: String] = [:]
    var synced: Date?

    init() {
        let text = (try? String(contentsOf: Self.directory.appendingPathComponent("context.md"), encoding: .utf8)) ?? ""
        let rows = text.components(separatedBy: .newlines).map { $0.trimmingCharacters(in: .whitespaces) }
        for slot in slots {
            if let index = rows.firstIndex(of: slot),
               let next = rows.dropFirst(index + 1).first(where: { !$0.isEmpty }), next.hasPrefix("- ") {
                lines[slot] = String(next.dropFirst(2))
            }
        }
        synced = (try? FileManager.default.attributesOfItem(atPath: Self.directory.appendingPathComponent("sync.md").path))?[.modificationDate] as? Date
    }

    var age: String {
        synced.map { "refreshed \(max(0, Int(Date().timeIntervalSince($0) / 60))) min ago" } ?? "no hub copy yet"
    }

    // The tools both slots run on stand for the owner's plans, as "check for newer models" reads them,
    // so only those tools' picks are offered. Plan changes go through "change my setup" in chat.
    func picks(_ slot: String, from rows: [String: [String: Slot]]) -> [Pick] {
        let owned = Set(lines.values.map(bare).compactMap { line in
            line.range(of: " via ").map { line[$0.upperBound...].components(separatedBy: ",")[0] }
        })
        var seen: [Pick] = []
        for plan in ["claude-and-chatgpt", "claude", "chatgpt", "google", "openrouter"] {
            guard let s = rows[plan]?[slot], owned.contains(tools[s.tool] ?? s.tool) else { continue }
            let pick = Pick(name: s.name, tool: tools[s.tool] ?? s.tool,
                            fallback: s.fallback.map { "\($0.name) (\($0.effort.capitalized))" }, id: s.id, plan: plan)
            if !seen.contains(where: { $0.line("") == pick.line("") }) { seen.append(pick) }
        }
        return seen
    }

    func option(_ slot: String, _ line: String, from rows: [String: [String: Slot]]) -> (Pick, String)? {
        for pick in picks(slot, from: rows) {
            if let effort = efforts.first(where: { pick.line($0) == line }) { return (pick, effort) }
        }
        return nil
    }

    func bare(_ line: String) -> String {
        line.replacingOccurrences(of: " (own pick)", with: "", options: .caseInsensitive)
    }

    func matches(_ slot: String, _ option: String) -> Bool {
        bare(lines[slot, default: ""]).caseInsensitiveCompare(option) == .orderedSame
    }

    var title: String {
        slots.map { slot in
            guard let line = lines[slot] else { return "?" }
            return line.components(separatedBy: " (")[0].split(separator: " ").dropFirst()
                .filter { $0.first?.isNumber != true }.joined(separator: " ")
        }.joined(separator: " · ")
    }
}

func resource(_ name: String) -> URL {
    var size: UInt32 = 0
    _NSGetExecutablePath(nil, &size)
    var path = [CChar](repeating: 0, count: Int(size))
    _NSGetExecutablePath(&path, &size)
    let executable = URL(fileURLWithPath: String(cString: path)).resolvingSymlinksInPath()
    return executable.deletingLastPathComponent().appendingPathComponent("../Resources/\(name)").standardizedFileURL
}

func loadPicks() throws -> [String: [String: Slot]] {
    try JSONDecoder().decode([String: [String: Slot]].self, from: Data(contentsOf: resource("slots.json")))
}

let guava: NSImage = {
    let image = NSImage(contentsOf: resource("guava.png")) ?? NSImage()
    image.size = NSSize(width: 14.5, height: 18)
    return image
}()

enum Agent {
    static let missing = "guava-bar needs Claude Code or Codex: see guava-bar/README.md"

    static func shell(_ arguments: [String], timeout: Double = 600) throws -> (String, Int32, Bool) {
        try FileManager.default.createDirectory(at: Hub.directory, withIntermediateDirectories: true)
        let outputURL = FileManager.default.temporaryDirectory.appendingPathComponent("guava-bar-\(UUID().uuidString)")
        guard FileManager.default.createFile(atPath: outputURL.path, contents: nil) else {
            throw CocoaError(.fileWriteUnknown)
        }
        defer { try? FileManager.default.removeItem(at: outputURL) }
        let output = try FileHandle(forWritingTo: outputURL)
        defer { try? output.close() }
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/bin/zsh")
        process.arguments = ["-lc"] + arguments
        var env = ProcessInfo.processInfo.environment
        env["PATH"] = NSHomeDirectory() + "/.local/bin:/opt/homebrew/bin:/usr/local/bin:" + (env["PATH"] ?? "/usr/bin:/bin")
        process.environment = env
        process.currentDirectoryURL = Hub.directory
        process.standardInput = FileHandle.nullDevice
        process.standardOutput = output
        process.standardError = output
        let ended = DispatchSemaphore(value: 0)
        process.terminationHandler = { _ in ended.signal() }
        try process.run()
        let timedOut = ended.wait(timeout: .now() + timeout) == .timedOut
        if timedOut {
            process.terminate()
            if ended.wait(timeout: .now() + 2) == .timedOut {
                kill(process.processIdentifier, SIGKILL)
                process.waitUntilExit()
            }
        }
        return (try String(contentsOf: outputURL, encoding: .utf8), process.terminationStatus, timedOut)
    }

    static func find() -> String? {
        for tool in ["claude", "codex"] {
            if let result = try? shell(["command -v \(tool)"], timeout: 10), result.1 == 0, !result.2 {
                return tool
            }
        }
        return nil
    }

    static func setPrompt(slot: String, old: String, new: String) -> String {
        """
        guava-bar: the owner picked this in the guava-bar menu and confirmed it there, so that click is their yes for this one change. Make my \(slot) "\(new)" (it was "\(old)"). Follow Change your setup in guava-hub/skills/guava-hub/SKILL.md from github.com/romeodiaz/guava-stack: edit only that slot's model line in guava-stack settings on my Notion context page, marking it (own pick) if it isn't today's pick for my plans, then refresh that page in ~/.guava-hub/context.md and set synced in ~/.guava-hub/sync.md. This is my own computer, not a bot's, so leave ~/.claude/settings.json and ~/.codex/config.toml alone. guava-bar already tested the new model, so skip the test, and skip logging a task for this one change. Make no other change. End your reply with one line: "done: <what changed>" or "failed: <why>".
        """
    }

    static let refreshPrompt = """
    guava-bar: refresh my local hub copy in ~/.guava-hub now, as Local copy in guava-hub/skills/guava-hub/backends/notion.md from github.com/romeodiaz/guava-stack says (build it if there's none yet). Change nothing in Notion. End your reply with one line: "done: <what changed>" or "failed: <why>".
    """

    // Notion's read tools, plus update-page for a change; files only in the hub copy. No shell, so the
    // session can't run anything: guava-bar tests the model itself, before the change.
    static func run(_ prompt: String, tool: String, write: Bool) -> String {
        let args: [String]
        if tool == "claude" {
            let notion = ["notion-fetch", "notion-search"] + (write ? ["notion-update-page"] : [])
            args = ["-p", prompt, "--allowedTools"]
                + notion.flatMap { ["mcp__claude_ai_Notion__\($0)", "mcp__notion__\($0)"] }
                + ["Read", "Edit(~/.guava-hub/**)", "Write(~/.guava-hub/**)",
                   "WebFetch(domain:github.com)", "WebFetch(domain:raw.githubusercontent.com)"]
        } else {
            // shortcut: Codex path untested for Notion MCP approvals in exec mode, test on a ChatGPT-only setup
            args = ["exec", "--skip-git-repo-check", "--sandbox", "workspace-write", prompt]
        }
        do {
            let (output, code, timedOut) = try shell(["exec \"$@\"", "guava-bar", tool] + args)
            if timedOut { return "failed: timed out after 10 minutes" }
            let last = output.components(separatedBy: .newlines).map { $0.trimmingCharacters(in: .whitespaces) }
                .last(where: { !$0.isEmpty })
            guard code == 0 else { return "failed: \(tool) exited \(code)" + (last.map { ": \($0)" } ?? "") }
            return last ?? "failed: \(tool) returned no output"
        } catch {
            return "failed: \(error.localizedDescription)"
        }
    }
}

extension Agent {
    // Check the new model answers before changing anything, with router-check.py's own command for its tool.
    static func test(_ pick: Pick, effort: String, slot: String) -> String? {
        let args = ["exec \"$@\"", "guava-bar", "python3", resource("router-check.py").path, "--plan", pick.plan,
                    "--slot", slot, "--\(slot)", "\(pick.id):\(effort.lowercased())", "--timeout", "240"]
        guard let (output, _, timedOut) = try? shell(args, timeout: 300) else { return "failed: couldn't run router-check.py" }
        if timedOut { return "failed: testing \(pick.name) timed out" }
        guard let start = output.firstIndex(of: "{"), let end = output.lastIndex(of: "}"),
              let report = try? JSONSerialization.jsonObject(with: Data(output[start...end].utf8)) as? [String: Any],
              let result = (report["slots"] as? [[String: Any]])?.first else {
            return "failed: couldn't test \(pick.name): " + output.suffix(200)
        }
        if result["ok"] as? Bool == true { return nil }
        return "failed: \(pick.name) at \(effort) didn't pass its test, so nothing changed: "
            + "\(result["verdict"] ?? "")\(result["error"].map { " (\($0))" } ?? "")"
    }

    static func change(slot: String, to line: String, rows: [String: [String: Slot]], tool: String) -> String {
        let hub = Hub()
        guard let (pick, effort) = hub.option(slot, line, from: rows) else { return "failed: not one of guava-bar's picks" }
        if let failure = test(pick, effort: effort, slot: slot) { return failure }
        let result = run(setPrompt(slot: slot, old: hub.lines[slot] ?? "not set", new: line), tool: tool, write: true)
        guard result.hasPrefix("done:") else { return result.hasPrefix("failed") ? result : "failed: \(result)" }
        guard Hub().matches(slot, line) else {
            return "failed: \(tool) said done, but the hub copy shows \(Hub().lines[slot] ?? "no \(slot)"): refresh, then check Notion"
        }
        return result
    }
}

func cli(_ args: [String]) -> Int32 {
    let hub = Hub()
    if args == ["show"] {
        for slot in slots { print("\(slot): \(hub.lines[slot] ?? "not set")") }
        print("hub copy: " + (hub.synced == nil ? "none yet at \(Hub.directory.path)" : hub.age))
        return 0
    }
    let prompt: String
    if args == ["refresh"] {
        prompt = Agent.refreshPrompt
    } else if (args.count == 2 && args[0] == "picks" || args.count == 3 && args[0] == "set"), slots.contains(args[1]) {
        do {
            let options = hub.picks(args[1], from: try loadPicks()).flatMap { pick in efforts.map { pick.line($0) } }
            if args[0] == "picks" {
                options.forEach { print($0) }
                return 0
            }
            guard options.contains(args[2]) else {
                fputs("Invalid option. See: guava-bar picks \(args[1])\n", stderr)
                return 1
            }
            guard let tool = Agent.find() else { print(Agent.missing); return 1 }
            let result = Agent.change(slot: args[1], to: args[2], rows: try loadPicks(), tool: tool)
            print(result)
            return result.hasPrefix("done:") ? 0 : 1
        } catch {
            fputs("failed: cannot load slots.json: \(error.localizedDescription)\n", stderr)
            return 1
        }
    } else {
        fputs("Usage: guava-bar [show | picks <head-chef|line-cook> | set <head-chef|line-cook> \"<option>\" | refresh]\n", stderr)
        return 2
    }
    guard let tool = Agent.find() else { print(Agent.missing); return 1 }
    let result = Agent.run(prompt, tool: tool, write: false)
    print(result)
    return result.hasPrefix("done:") ? 0 : 1
}

@MainActor
final class BarState: ObservableObject {
    @Published var hub = Hub()
    @Published var picks: [String: [String: Slot]] = [:]
    @Published var running = false
    @Published var status = ""
    @Published var loginStatus = SMAppService.mainApp.status

    init() { reload() }

    func reload() {
        hub = Hub()
        loginStatus = SMAppService.mainApp.status
        do { picks = try loadPicks() }
        catch { status = "failed: cannot load slots.json: \(error.localizedDescription)" }
    }

    func start(status message: String, _ work: @escaping @Sendable () -> String) async {
        status = message
        status = await Task.detached { work() }.value
        running = false
        reload()
    }

    func request(slot: String? = nil, option: String? = nil) {
        guard !running else { return }
        if let slot, let option, hub.matches(slot, option) { return }
        running = true
        status = "Finding Claude Code or Codex…"
        Task {
            guard let tool = await Task.detached(operation: { Agent.find() }).value else {
                status = Agent.missing
                running = false
                return
            }
            if let slot, let option {
                let old = hub.lines[slot] ?? "not set"
                NSApp.activate(ignoringOtherApps: true)
                let alert = NSAlert()
                alert.messageText = "Change \(slot)?"
                let toolName = tool == "claude" ? "Claude Code" : "Codex"
                alert.informativeText = "From: \(old)\nTo: \(option)\n\nguava-bar tests the new model, then asks \(toolName) to make this change in your Notion hub. It takes a minute or two and uses a little of your plan."
                alert.addButton(withTitle: "Change")
                alert.addButton(withTitle: "Cancel")
                guard alert.runModal() == .alertFirstButtonReturn else { running = false; return }
                let rows = picks
                await start(status: "Testing, then changing \(slot)…") { Agent.change(slot: slot, to: option, rows: rows, tool: tool) }
            } else {
                await start(status: "Refreshing from Notion…") { Agent.run(Agent.refreshPrompt, tool: tool, write: false) }
            }
        }
    }

    func login(_ enabled: Bool) {
        do {
            if enabled { try SMAppService.mainApp.register() }
            else { try SMAppService.mainApp.unregister() }
        } catch { status = "failed: \(error.localizedDescription)" }
        loginStatus = SMAppService.mainApp.status
    }

    var loginDescription: String {
        switch loginStatus {
        case .enabled: return "Enabled"
        case .requiresApproval: return "Needs approval in System Settings"
        case .notRegistered: return "Off"
        case .notFound: return "App not found"
        @unknown default: return "Unknown"
        }
    }
}

struct GuavaBarApp: App {
    @StateObject private var state = BarState()
    private let timer = Timer.publish(every: 30, on: .main, in: .common).autoconnect()

    var body: some Scene {
        MenuBarExtra {
            ForEach(slots, id: \.self) { slot in
                Text("\(slot): \(state.hub.lines[slot] ?? "not set")").disabled(true)
                Menu("Change \(slot)") {
                    ForEach(state.hub.picks(slot, from: state.picks), id: \.self) { pick in
                        Menu("\(pick.name) via \(pick.tool)") {
                            ForEach(efforts, id: \.self) { effort in
                                Button { state.request(slot: slot, option: pick.line(effort)) } label: {
                                    if state.hub.matches(slot, pick.line(effort)) {
                                        Label(effort, systemImage: "checkmark")
                                    } else { Text(effort) }
                                }
                            }
                        }
                    }
                }.disabled(state.running)
            }
            Divider()
            Text(state.hub.synced == nil ? "No hub copy yet" : "Hub copy \(state.hub.age)").disabled(true)
            Button("Refresh from Notion") { state.request() }.disabled(state.running)
            if !state.status.isEmpty { Text(state.status).disabled(true) }
            Divider()
            Toggle("Open at login", isOn: Binding(
                get: { state.loginStatus == .enabled || state.loginStatus == .requiresApproval },
                set: { state.login($0) }
            ))
            Text("Open at login: \(state.loginDescription)").disabled(true)
            Button("Quit guava-bar") { NSApp.terminate(nil) }
        } label: {
            HStack {
                Image(nsImage: guava)
                Text((state.hub.synced == nil ? "" : state.hub.title) + (state.running ? " …" : ""))
            }.onReceive(timer) { _ in state.reload() }
        }.menuBarExtraStyle(.menu)
    }
}

@main
enum GuavaBar {
    @MainActor static func main() {
        let args = Array(CommandLine.arguments.dropFirst())
        if !args.isEmpty { exit(cli(args)) }
        GuavaBarApp.main()
    }
}
