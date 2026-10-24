import AppKit
import Combine
import MachO
import ServiceManagement
import SwiftUI
import Darwin

let slots = ["head-chef", "line-cook"]
let allEfforts = ["Low", "Medium", "High", "xhigh", "Max"]

let tools = ["claude": "Claude Code", "codex": "Codex", "agy": "Antigravity CLI", "pi": "Pi"]

// One slot of one plan row in guava-router's slots.json, which sync-models.py writes from models.yaml.
struct Slot: Decodable {
    struct Fallback: Decodable { let name: String; let id: String; let effort: String }
    let name: String
    let id: String
    let effort: String
    let tool: String
    let fallback: Fallback?
}

func label(_ effort: String) -> String { allEfforts.first { $0.lowercased() == effort.lowercased() } ?? effort }

struct Pick: Hashable {
    let name: String
    let tool: String
    let fallback: String?
    let id: String
    let plan: String  // the slots.json row it came from, which router-check.py tests it on
    let effort: String
    // Antigravity CLI's models come at Low, Medium and High, each its own ID (`agy models`).
    var efforts: [String] { tool == "Antigravity CLI" ? Array(allEfforts.prefix(3)) : allEfforts }

    func id(_ effort: String) -> String {
        guard tool == "Antigravity CLI", let dash = id.lastIndex(of: "-") else { return id }
        return id[..<dash] + "-" + effort.lowercased()
    }

    init(_ s: Slot, plan: String) {
        name = s.name; tool = tools[s.tool] ?? s.tool; id = s.id; self.plan = plan; effort = label(s.effort)
        fallback = s.fallback.map { "\($0.name) (\(label($0.effort)))" }
    }

    // On Google AI, the slot's Gemini fallback can also be picked on its own.
    init(gemini s: Slot.Fallback) {
        name = s.name; tool = "Antigravity CLI"; id = s.id; plan = "google"; effort = label(s.effort); fallback = nil
    }

    func line(_ effort: String) -> String {
        let base = "\(name) (\(effort)) via \(tool)"
        return fallback.map { "\(base), falling back to \($0) when its usage runs out" } ?? base
    }
}

// Both slots at once, such as every plan row of slots.json.
struct Pair: Hashable {
    let name: String
    let head: Pick
    let line: Pick
}

let plans = ["claude-and-chatgpt": "Claude + ChatGPT", "claude": "Claude", "chatgpt": "ChatGPT",
             "google": "Google AI", "openrouter": "OpenRouter"]

func catalog(_ rows: [String: [String: Slot]]) -> (picks: [String: [Pick]], pairs: [Pair]) {
    var picks: [String: [Pick]] = [:], pairs: [Pair] = []
    for plan in ["claude-and-chatgpt", "claude", "chatgpt", "google", "openrouter"] {
        guard let row = rows[plan], let head = row["head-chef"], let line = row["line-cook"] else { continue }
        pairs.append(Pair(name: plans[plan]!, head: Pick(head, plan: plan), line: Pick(line, plan: plan)))
        if let h = head.fallback, let l = line.fallback {
            pairs.append(Pair(name: "Google AI, Gemini", head: Pick(gemini: h), line: Pick(gemini: l)))
        }
    }
    for pair in pairs {
        for (slot, pick) in [("head-chef", pair.head), ("line-cook", pair.line)]
        where !picks[slot, default: []].contains(where: { $0.line("") == pick.line("") }) {
            picks[slot, default: []].append(pick)
        }
    }
    return (picks, pairs)
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

    // Switch a slot in the hub copy, which local sessions read before each hand-off; Notion catches up after.
    static func write(_ slot: String, _ line: String) -> Bool {
        let url = directory.appendingPathComponent("context.md")
        guard let text = try? String(contentsOf: url, encoding: .utf8) else { return false }
        var rows = text.components(separatedBy: "\n")
        guard let label = rows.firstIndex(where: { $0.trimmingCharacters(in: .whitespaces) == slot }),
              let bullet = rows[(label + 1)...].firstIndex(where: { !$0.trimmingCharacters(in: .whitespaces).isEmpty }),
              let dash = rows[bullet].range(of: "- "),
              rows[bullet][..<dash.lowerBound].allSatisfy(\.isWhitespace) else { return false }
        rows[bullet] = rows[bullet][..<dash.upperBound] + line
        return (try? rows.joined(separator: "\n").write(to: url, atomically: true, encoding: .utf8)) != nil
    }

    var age: String {
        synced.map { "refreshed \(max(0, Int(Date().timeIntervalSince($0) / 60))) min ago" } ?? "no hub copy yet"
    }

    // Offered: the tools installed on this Mac, plus those the slots already name, which stand for the
    // owner's plans. A tool that's installed but not on a plan fails guava-bar's test and switches back.
    func owned(_ installed: Set<String>) -> Set<String> {
        installed.union(lines.values.map(bare).compactMap { line in
            line.range(of: " via ").map { line[$0.upperBound...].components(separatedBy: ",")[0] }
        })
    }

    func picks(_ slot: String, from rows: [String: [String: Slot]], installed: Set<String>) -> [Pick] {
        let owned = owned(installed)
        return catalog(rows).picks[slot, default: []].filter { owned.contains($0.tool) }
    }

    func pairs(from rows: [String: [String: Slot]], installed: Set<String>) -> [Pair] {
        let owned = owned(installed)
        return catalog(rows).pairs.filter { owned.contains($0.head.tool) && owned.contains($0.line.tool) }
    }

    func option(_ slot: String, _ line: String, from rows: [String: [String: Slot]], installed: Set<String>) -> (Pick, String)? {
        for pick in picks(slot, from: rows, installed: installed) {
            if let effort = pick.efforts.first(where: { pick.line($0) == line }) { return (pick, effort) }
        }
        return nil
    }

    func bare(_ line: String) -> String {
        line.replacingOccurrences(of: " (own pick)", with: "", options: .caseInsensitive)
    }

    func matches(_ slot: String, _ option: String) -> Bool {
        bare(lines[slot, default: ""]).caseInsensitiveCompare(option) == .orderedSame
    }

    // "Claude Opus 5.5 (High) via Claude Code" → "Opus", "GPT-6.1 Sol (High) via Codex" → "Sol".
    func short(_ slot: String) -> String {
        guard let line = lines[slot] else { return "?" }
        return line.components(separatedBy: " (")[0].split(separator: " ").dropFirst()
            .filter { $0.first?.isNumber != true }.joined(separator: " ")
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

// The head-chef and line-cook pixel art, 18 points tall in the menu bar.
let icons: [String: NSImage] = Dictionary(uniqueKeysWithValues: slots.map { slot in
    let image = NSImage(contentsOf: resource("\(slot).png")) ?? NSImage()
    if image.size.height > 0 { image.size = NSSize(width: 18 * image.size.width / image.size.height, height: 18) }
    return (slot, image)
})

// shortcut: trusts the session's own last line, so "done: nothing. failed: …" counts as failed; read Notion back if that slips
func succeeded(_ line: String) -> Bool { line.hasPrefix("done:") && !line.lowercased().contains("fail") }

struct Change: Hashable, Sendable {
    let slot: String
    let line: String
}

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

    static func installed() -> Set<String> {
        let found = (try? shell(["for t in claude codex agy pi; do command -v $t > /dev/null && echo $t; done"], timeout: 15))?.0 ?? ""
        return Set(found.split(separator: "\n").compactMap { tools[String($0)] })
    }

    static func setPrompt(_ changes: [Change], old: [String: String]) -> String {
        let what = changes.map { "the \($0.slot) model line to \"\($0.line)\" (it was \"\(old[$0.slot] ?? "not set")\")" }
            .joined(separator: " and ")
        return """
        guava-bar: the owner switched their models in the guava-bar menu, so that click is their yes for this one change. guava-bar already switched it in ~/.guava-hub/context.md and tested the new models. Now make my Notion context page match: in guava-stack settings, set only \(what), marking each (own pick) if it isn't today's pick for my plans, as Change your setup in guava-hub/skills/guava-hub/SKILL.md from github.com/romeodiaz/guava-stack says. Leave ~/.guava-hub, ~/.claude/settings.json and ~/.codex/config.toml alone, skip the test, and skip logging a task for this one change. Make no other change. End your reply with one line: "done: <what changed>" or "failed: <why>".
        """
    }

    static let refreshPrompt = """
    guava-bar: refresh my local hub copy in ~/.guava-hub now, as Local copy in guava-hub/skills/guava-hub/backends/notion.md from github.com/romeodiaz/guava-stack says (build it if there's none yet). Change nothing in Notion. End your reply with one line: "done: <what changed>" or "failed: <why>".
    """

    // No shell, so the session can't run anything. A change gets Notion's read tools and update-page and
    // no file edits (guava-bar already switched the copy); a refresh gets the read tools and the hub copy.
    static func run(_ prompt: String, tool: String, write: Bool) -> String {
        let args: [String]
        if tool == "claude" {
            let notion = ["notion-fetch", "notion-search"] + (write ? ["notion-update-page"] : [])
            args = ["-p", prompt, "--allowedTools"]
                + notion.flatMap { ["mcp__claude_ai_Notion__\($0)", "mcp__notion__\($0)"] }
                + ["Read", "WebFetch(domain:github.com)", "WebFetch(domain:raw.githubusercontent.com)"]
                + (write ? [] : ["Edit(~/.guava-hub/**)", "Write(~/.guava-hub/**)"])
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
    // Check the new model answers, with router-check.py's own command for its tool.
    static func test(_ pick: Pick, effort: String, slot: String) -> String? {
        let args = ["exec \"$@\"", "guava-bar", "python3", resource("router-check.py").path, "--plan", pick.plan,
                    "--slot", slot, "--\(slot)", "\(pick.id(effort)):\(effort.lowercased())", "--timeout", "240"]
        guard let (output, _, timedOut) = try? shell(args, timeout: 300) else { return "failed: couldn't run router-check.py" }
        if timedOut { return "failed: testing \(pick.name) timed out" }
        guard let start = output.firstIndex(of: "{"), let end = output.lastIndex(of: "}"),
              let report = try? JSONSerialization.jsonObject(with: Data(output[start...end].utf8)) as? [String: Any],
              let result = (report["slots"] as? [[String: Any]])?.first else {
            return "failed: couldn't test \(pick.name): " + output.suffix(200)
        }
        if result["ok"] as? Bool == true { return nil }
        return "failed: \(pick.name) at \(effort) didn't pass its test: "
            + "\(result["verdict"] ?? "")\(result["error"].map { " (\($0))" } ?? "")"
    }

    // Switch on this Mac at once, then test and update Notion. Picking the current line again just retries Notion.
    static func change(_ changes: [Change], rows: [String: [String: Slot]], installed: Set<String>, tool: String,
                       switched: (String) -> Void) -> String {
        let hub = Hub()
        var tests: [(Pick, String, String)] = []
        for change in changes {
            guard let (pick, effort) = hub.option(change.slot, change.line, from: rows, installed: installed),
                  hub.lines[change.slot] != nil else { return "failed: \(change.line) isn't one of guava-bar's picks" }
            tests.append((pick, effort, change.slot))
        }
        var written: [Change] = []
        func undo() { for change in written { _ = Hub.write(change.slot, hub.lines[change.slot]!) } }
        for change in changes where !hub.matches(change.slot, change.line) {
            guard Hub.write(change.slot, change.line) else { undo(); return "failed: couldn't change \(change.slot) in the hub copy" }
            written.append(change)
        }
        let now = changes.map { "\($0.slot) is now \($0.line)" }.joined(separator: ", ")
        switched("\(now) on this Mac. Testing, then updating Notion…")
        for (pick, effort, slot) in tests {
            if let failure = test(pick, effort: effort, slot: slot) {
                undo()
                return written.isEmpty ? failure : failure + ". Switched back."
            }
        }
        let result = run(setPrompt(changes, old: hub.lines), tool: tool, write: true)
        guard succeeded(result) else {
            return "failed: switched on this Mac, but Notion wasn't updated (pick it again to retry): "
                + (result.hasPrefix("failed: ") ? String(result.dropFirst(8)) : result)
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
    } else if args == ["pairs"] || args.count == 2 && args[0] == "picks" && slots.contains(args[1])
                || args.first == "set" && [3, 5].contains(args.count) {
        do {
            let rows = try loadPicks(), installed = Agent.installed()
            if args == ["pairs"] {
                for pair in hub.pairs(from: rows, installed: installed) {
                    print("\(pair.name): set head-chef \"\(pair.head.line(pair.head.effort))\" line-cook \"\(pair.line.line(pair.line.effort))\"")
                }
                return 0
            }
            if args[0] == "picks" {
                hub.picks(args[1], from: rows, installed: installed).forEach { pick in pick.efforts.forEach { print(pick.line($0)) } }
                return 0
            }
            let changes = stride(from: 1, to: args.count, by: 2).map { Change(slot: args[$0], line: args[$0 + 1]) }
            guard Set(changes.map(\.slot)).count == changes.count, changes.allSatisfy({ slots.contains($0.slot)
                      && hub.option($0.slot, $0.line, from: rows, installed: installed) != nil }) else {
                fputs("Invalid option. See: guava-bar picks <head-chef|line-cook>, or guava-bar pairs\n", stderr)
                return 1
            }
            guard let tool = Agent.find() else { print(Agent.missing); return 1 }
            let result = Agent.change(changes, rows: rows, installed: installed, tool: tool) {
                print($0)
                fflush(stdout)
            }
            print(result)
            return succeeded(result) ? 0 : 1
        } catch {
            fputs("failed: cannot load slots.json: \(error.localizedDescription)\n", stderr)
            return 1
        }
    } else {
        fputs("Usage: guava-bar [show | picks <head-chef|line-cook> | pairs | set <slot> \"<option>\" [<slot> \"<option>\"] | refresh]\n", stderr)
        return 2
    }
    guard let tool = Agent.find() else { print(Agent.missing); return 1 }
    let result = Agent.run(prompt, tool: tool, write: false)
    print(result)
    return succeeded(result) ? 0 : 1
}

@MainActor
final class BarState: ObservableObject {
    @Published var hub = Hub()
    @Published var picks: [String: [String: Slot]] = [:]
    @Published var installed: Set<String> = []
    @Published var running = false  // the background test and Notion update; switching stays open meanwhile
    @Published var status = ""
    // Slots switched on this Mac that Notion doesn't show yet, each with the line Notion still has.
    // Kept across restarts, so a switch Notion never got is retried, not forgotten.
    @Published var unsynced = UserDefaults.standard.dictionary(forKey: "unsynced") as? [String: String] ?? [:] {
        didSet { UserDefaults.standard.set(unsynced, forKey: "unsynced") }
    }
    @Published var loginStatus = SMAppService.mainApp.status

    init() {
        reload()
        Task {
            installed = await Task.detached { Agent.installed() }.value
            sync()
        }
    }

    func reload() {
        hub = Hub()
        loginStatus = SMAppService.mainApp.status
        do { picks = try loadPicks() }
        catch { status = "failed: cannot load slots.json: \(error.localizedDescription)" }
    }

    // Switch on this Mac at once, then let the background catch Notion up.
    func request(_ changes: [Change]) {
        let hub = Hub()
        guard changes.allSatisfy({ hub.option($0.slot, $0.line, from: picks, installed: installed) != nil }) else { return }
        for change in changes where !hub.matches(change.slot, change.line) {
            guard Hub.write(change.slot, change.line) else { status = "failed: couldn't change \(change.slot) in the hub copy"; return }
            if unsynced[change.slot] == nil { unsynced[change.slot] = hub.lines[change.slot] }
            // Switched back to what Notion has: nothing left to send.
            if let notion = unsynced[change.slot], hub.bare(notion).caseInsensitiveCompare(change.line) == .orderedSame {
                unsynced[change.slot] = nil
            }
        }
        reload()
        sync()
    }

    // Test what changed, then send Notion the latest lines in one update; runs again if more changed meanwhile.
    func sync() {
        guard !running, !unsynced.isEmpty else { return }
        running = true
        let rows = picks, installed = installed, notion = unsynced
        let wanted = notion.keys.sorted().compactMap { slot in hub.lines[slot].map { Change(slot: slot, line: hub.bare($0)) } }
        status = "Testing \(wanted.map(\.line).joined(separator: " and "))…"
        Task {
            let result = await Task.detached { () async -> String in
                let hub = Hub()
                for change in wanted {
                    guard let (pick, effort) = hub.option(change.slot, change.line, from: rows, installed: installed) else { continue }
                    if let failure = Agent.test(pick, effort: effort, slot: change.slot) {
                        // Undo the whole batch, like the CLI, but never a switch made after it while the test ran.
                        for change in wanted where Hub().matches(change.slot, change.line) {
                            if let old = notion[change.slot] { _ = Hub.write(change.slot, old) }
                        }
                        return failure + ". Switched back."
                    }
                }
                await MainActor.run { self.status = "Updating Notion…" }
                guard let tool = Agent.find() else { return "failed: \(Agent.missing)" }
                return Agent.run(Agent.setPrompt(wanted, old: notion), tool: tool, write: true)
            }.value
            reload()
            let switchedBack = result.hasSuffix("Switched back.")
            if succeeded(result) || switchedBack {
                for change in wanted where (succeeded(result) && hub.matches(change.slot, change.line))
                    || (switchedBack && hub.lines[change.slot] == notion[change.slot]) {
                    unsynced[change.slot] = nil
                }
                status = result
            } else {
                status = "failed: switched on this Mac, but Notion wasn't updated (Retry below): "
                    + (result.hasPrefix("failed: ") ? String(result.dropFirst(8)) : result)
            }
            running = false
            if succeeded(result) || switchedBack { sync() }
        }
    }

    func refresh() {
        guard !running else { return }
        running = true
        status = "Refreshing from Notion…"
        Task {
            status = await Task.detached { () -> String in
                guard let tool = Agent.find() else { return Agent.missing }
                return Agent.run(Agent.refreshPrompt, tool: tool, write: false)
            }.value
            running = false
            reload()
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

// The menu bar label shows only one image and one text, so both icons and names are drawn into one image.
func bar(_ hub: Hub, running: Bool) -> NSImage {
    let font = NSFont.menuBarFont(ofSize: 0)
    let parts = slots.map { (icons[$0]!, hub.synced == nil ? "" : hub.short($0)) } + (running ? [(NSImage(), "…")] : [])
    let gap: CGFloat = 4, space: CGFloat = 8
    let style: [NSAttributedString.Key: Any] = [.font: font, .foregroundColor: NSColor.labelColor]
    let width = parts.reduce(-space) { $0 + $1.0.size.width + gap + ($1.1 as NSString).size(withAttributes: style).width + space }
    return NSImage(size: NSSize(width: max(width, 1), height: 18), flipped: false) { _ in
        NSGraphicsContext.current?.imageInterpolation = .none  // keep the pixel art crisp
        var x: CGFloat = 0
        for (icon, text) in parts {
            icon.draw(in: NSRect(x: x, y: 0, width: icon.size.width, height: icon.size.height))
            x += icon.size.width + (icon.size.width > 0 ? gap : 0)
            let size = (text as NSString).size(withAttributes: style)
            (text as NSString).draw(at: NSPoint(x: x, y: (18 - size.height) / 2), withAttributes: style)
            x += size.width + space
        }
        return true
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
                    ForEach(state.hub.picks(slot, from: state.picks, installed: state.installed), id: \.self) { pick in
                        Menu("\(pick.name) via \(pick.tool)") {
                            ForEach(pick.efforts, id: \.self) { effort in
                                Button { state.request([Change(slot: slot, line: pick.line(effort))]) } label: {
                                    if state.hub.matches(slot, pick.line(effort)) {
                                        Label(effort, systemImage: "checkmark")
                                    } else { Text(effort) }
                                }
                            }
                        }
                    }
                }
            }
            Menu("Switch both") {
                ForEach(state.hub.pairs(from: state.picks, installed: state.installed), id: \.self) { pair in
                    let changes = [Change(slot: "head-chef", line: pair.head.line(pair.head.effort)),
                                   Change(slot: "line-cook", line: pair.line.line(pair.line.effort))]
                    Button { state.request(changes) } label: {
                        let title = "\(pair.name): \(pair.head.name) + \(pair.line.name)"
                        if changes.allSatisfy({ state.hub.matches($0.slot, $0.line) }) {
                            Label(title, systemImage: "checkmark")
                        } else { Text(title) }
                    }
                }
            }
            Divider()
            Text(state.hub.synced == nil ? "No hub copy yet" : "Hub copy \(state.hub.age)").disabled(true)
            Button("Refresh from Notion") { state.refresh() }.disabled(state.running || !state.unsynced.isEmpty)
            if !state.unsynced.isEmpty && !state.running { Button("Retry Notion update") { state.sync() } }
            if !state.status.isEmpty { Text(state.status).disabled(true) }
            Divider()
            Toggle("Open at login", isOn: Binding(
                get: { state.loginStatus == .enabled || state.loginStatus == .requiresApproval },
                set: { state.login($0) }
            ))
            Text("Open at login: \(state.loginDescription)").disabled(true)
            Button("Quit guava-bar") { NSApp.terminate(nil) }
        } label: {
            Image(nsImage: bar(state.hub, running: state.running)).onReceive(timer) { _ in state.reload() }
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
