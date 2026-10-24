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
    let tool: String
    let fallback: Fallback?
}

struct Pick: Hashable {
    let name: String
    let tool: String
    let fallback: String?

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

    // Plan changes go through chat, so a slot on Antigravity CLI or Pi only offers that plan's picks.
    func picks(_ slot: String, from rows: [String: [String: Slot]]) -> [Pick] {
        let line = lines[slot, default: ""]
        let plans = line.contains("via Antigravity CLI") ? ["google"]
            : line.contains("via Pi") ? ["openrouter"] : ["claude-and-chatgpt", "chatgpt", "claude"]
        var seen: [Pick] = []
        for plan in plans {
            guard let s = rows[plan]?[slot] else { continue }
            let pick = Pick(name: s.name, tool: tools[s.tool] ?? s.tool,
                            fallback: s.fallback.map { "\($0.name) (\($0.effort.capitalized))" })
            if !seen.contains(pick) { seen.append(pick) }
        }
        return seen
    }

    func matches(_ slot: String, _ option: String) -> Bool {
        lines[slot, default: ""].replacingOccurrences(of: " (own pick)", with: "", options: .caseInsensitive)
            .caseInsensitiveCompare(option) == .orderedSame
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
        guava-bar: the owner picked this in the guava-bar menu and confirmed it there, so that click is their yes for this one change. Make my \(slot) "\(new)" (it was "\(old)"). Follow Change your setup in guava-hub/skills/guava-hub/SKILL.md from github.com/romeodiaz/guava-stack: edit only that slot's model line in guava-stack settings on my Notion context page, marking it (own pick) if it isn't today's pick for my plans, then refresh that page in ~/.guava-hub/context.md and set synced in ~/.guava-hub/sync.md. This is my own computer, not a bot's, so leave ~/.claude/settings.json and ~/.codex/config.toml alone. Test the new slot with one tiny prompt at its effort. Make no other change. End your reply with one line: "done: <what changed>" or "failed: <why>".
        """
    }

    static let refreshPrompt = """
    guava-bar: refresh my local hub copy in ~/.guava-hub now, as Local copy in guava-hub/skills/guava-hub/backends/notion.md from github.com/romeodiaz/guava-stack says (build it if there's none yet). Change nothing in Notion. End your reply with one line: "done: <what changed>" or "failed: <why>".
    """

    static func run(_ prompt: String, tool: String) -> String {
        let args: [String]
        if tool == "claude" {
            args = ["-p", prompt, "--allowedTools", "mcp__claude_ai_Notion", "mcp__notion", "Read", "Edit", "Write",
                    "Bash(claude -p:*)", "Bash(codex exec:*)", "Bash(agy -p:*)", "Bash(date:*)", "Bash(find:*)", "Bash(grep:*)"]
        } else {
            // shortcut: Codex path untested for Notion MCP approvals in exec mode, test on a ChatGPT-only setup
            args = ["exec", "--skip-git-repo-check", "--sandbox", "workspace-write", prompt]
        }
        do {
            let (output, code, timedOut) = try shell(["exec \"$@\"", "guava-bar", tool] + args)
            if timedOut { return "failed: timed out after 10 minutes" }
            return output.components(separatedBy: .newlines).map { $0.trimmingCharacters(in: .whitespaces) }
                .last(where: { !$0.isEmpty }) ?? "failed: \(tool) returned no output (exit \(code))"
        } catch {
            return "failed: \(error.localizedDescription)"
        }
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
            prompt = Agent.setPrompt(slot: args[1], old: hub.lines[args[1]] ?? "not set", new: args[2])
        } catch {
            fputs("failed: cannot load slots.json: \(error.localizedDescription)\n", stderr)
            return 1
        }
    } else {
        fputs("Usage: guava-bar [show | picks <head-chef|line-cook> | set <head-chef|line-cook> \"<option>\" | refresh]\n", stderr)
        return 2
    }
    guard let tool = Agent.find() else { print(Agent.missing); return 1 }
    let result = Agent.run(prompt, tool: tool)
    print(result)
    return result.hasPrefix("done") ? 0 : 1
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

    func start(_ prompt: String, tool: String, status message: String) async {
        status = message
        status = await Task.detached { Agent.run(prompt, tool: tool) }.value
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
                alert.informativeText = "From: \(old)\nTo: \(option)\n\nguava-bar asks \(toolName) to make this change in your Notion hub and test it. It takes a minute or two and uses a little of your plan."
                alert.addButton(withTitle: "Change")
                alert.addButton(withTitle: "Cancel")
                guard alert.runModal() == .alertFirstButtonReturn else { running = false; return }
                await start(Agent.setPrompt(slot: slot, old: old, new: option), tool: tool, status: "Changing \(slot)…")
            } else {
                await start(Agent.refreshPrompt, tool: tool, status: "Refreshing from Notion…")
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
