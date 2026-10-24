#!/usr/bin/env python3
"""Check the Model Router: is each tool installed, signed in and able to read the hub, and which model answers each slot.

    python3 router-check.py
    python3 router-check.py --plan claude-and-chatgpt|claude|chatgpt|google|openrouter \
        [--slot head-chef|line-cook] [--head-chef ID[:EFFORT]] [--line-cook ID[:EFFORT]] [--timeout SECONDS]

With no --plan, it only reads: which of Claude Code, Codex, Antigravity CLI and Pi are installed
(and any second copy on PATH), signed in, connected to Notion and allowed to read the hub, and which
plans' rows can run here. With --plan, it also sends each slot of that row a one-word prompt with the
slot's own command and reports the model that answered, as the tool reports it. Claude Code and Pi
report the model that served the answer; Codex reports only the model it asked for; Antigravity CLI
may report none. A slot that answers as a different model fails the check.

Slots come from slots.json next to this script (written by scripts/sync-models.py from
guava-router/models.yaml). --head-chef and --line-cook test an own pick instead. Standard library only.
Never prints a key, only whether one is set.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLOTS = json.loads((HERE / "slots.json").read_text())
TOOLS = {"claude": "Claude Code", "codex": "Codex", "agy": "Antigravity CLI", "pi": "Pi"}
HUB_TOOLS = ("notion-get-enabled-skills", "notion-fetch", "notion-search", "notion-download-skill")
PROMPT = "This is a quick check that you're working. Reply with just the word OK."


def probe(cmd, timeout=60):
    """(exit code, output) of a read-only command, or None if it isn't installed."""
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        return 124, "timed out"
    return done.returncode, (done.stdout + done.stderr).strip()


def copies(name):
    """Every copy of a command on PATH, first one first: an older copy ahead of the updated one rejects new models."""
    found = []
    for folder in os.environ.get("PATH", "").split(os.pathsep):
        path = Path(folder) / name
        if path.is_file() and os.access(path, os.X_OK) and path.resolve() not in (p.resolve() for p in found):
            found.append(path)
    return [str(p) for p in found]


def notion_line(tool):
    """The Notion line of `claude mcp list` or `codex mcp list`, or None if Notion isn't there."""
    listed = probe([tool, "mcp", "list"], timeout=90)
    if not listed or listed[0]:
        return None
    return next((line.strip() for line in listed[1].splitlines() if "notion" in line.lower()), None)


def hub_approved():
    """Which of Notion's four read-only tools Claude Code's settings pre-approve."""
    try:
        allow = json.loads((Path.home() / ".claude" / "settings.json").read_text())["permissions"]["allow"]
    except (OSError, ValueError, KeyError, TypeError):
        allow = []
    return [t for t in HUB_TOOLS if any(str(rule).endswith(f"__{t}") for rule in allow)]


def plan_ids(tool):
    """The model IDs a tool must run, across every plan row that uses it."""
    ids = set()
    for row in SLOTS.values():
        for slot in row.values():
            if slot["tool"] == tool:
                ids |= {slot["id"]} | ({slot["fallback"]["id"]} if "fallback" in slot else set())
    return sorted(ids)


def status(tool, hub):
    """What setup step 2 (and, with hub, steps 3 and 4) left in place for one tool, with a fix for each gap."""
    version = probe([tool, "--version"])
    number = re.search(r"\d+\.\d+[\w.-]*", version[1]) if version and version[0] == 0 else None
    report = {"installed": number.group(0) if number else bool(version and version[0] == 0)}
    if not report["installed"]:
        report["fix"] = "install it as setup step 2 says"
        return report
    if len(found := copies(tool)) > 1:
        report["copies_on_path"] = {path: (probe([path, "--version"]) or (1, ""))[1].split("\n")[0] for path in found}
    if tool == "claude":
        auth = probe(["claude", "auth", "status", "--json"])
        try:
            auth = json.loads(auth[1])
        except (TypeError, ValueError):
            auth = {}
        report["signed_in"] = bool(auth.get("loggedIn"))
        report.update({k: auth[k] for k in ("authMethod", "subscriptionType") if auth.get(k)})
        if os.environ.get("ANTHROPIC_API_KEY"):
            report["note"] = "ANTHROPIC_API_KEY is set, so Claude Code bills that key instead of the Claude plan"
    elif tool == "codex":
        login = probe(["codex", "login", "status"])
        report["signed_in"] = bool(login) and login[0] == 0
        report["status"] = login[1].splitlines()[-1][-200:] if login and login[1] else None
    elif tool == "agy":
        models = probe(["agy", "models"], timeout=90)
        listed = models[1] if models and models[0] == 0 else ""
        report["signed_in"] = bool(listed)
        if missing := [m for m in plan_ids("agy") if listed and m not in listed]:
            report["models_missing"] = missing
            report["fix"] = "`agy models` doesn't list these, so the Google plan may not include them; tell the owner"
    else:
        auth = probe(["pi", "auth", "check", "--provider", "openrouter", "--json"])
        try:
            auth = json.loads(auth[1])
        except (TypeError, ValueError):
            auth = {}
        report["signed_in"] = auth.get("status") == "ready"
        if report["signed_in"]:
            report["how"] = "browser sign-in" if auth.get("authType") == "oauth" else "API key"
    fixes = ([report.pop("fix")] if "fix" in report else []) + ([] if report["signed_in"] else ["sign in as setup step 2 says"])
    if hub and tool in ("claude", "codex"):
        line = notion_line(tool)
        report["notion"] = line or False
        if not line or re.search(r"fail|needs auth|not connected|error", line, re.I):
            fixes.append("connect Notion as setup step 3 says")
        if tool == "claude":
            report["hub_read_approved"] = approved = hub_approved()
            if len(approved) < len(HUB_TOOLS):
                fixes.append("approve Notion's four read-only tools as setup step 4 says")
    if len(set(report.get("copies_on_path", {}).values())) > 1:
        fixes.append("copies of different versions are on PATH and the first one runs: use the updated one, as Repair step 2 says")
    if fixes:
        report["fix"] = "; ".join(fixes)
    return report


def norm(model):
    """A model ID without its provider, separators or effort suffix, so aliases of one model compare equal."""
    model = re.sub(r"[._]", "-", model.lower().split("/")[-1])
    return re.sub(r"-(minimal|low|medium|high|xhigh|max)$", "", model)


def same(asked, answered):
    """The same model, or that model with a date or snapshot number added (never a shorter, older ID)."""
    a, b = norm(asked), norm(answered)
    return b == a or re.fullmatch(re.escape(a) + r"-\d+", b) is not None


def run(tool, model, effort, timeout):
    """Send the check prompt with the slot's own command: (answer, model the tool reported or None, how it knows)."""
    if tool == "claude":
        done = subprocess.run(["claude", "-p", "--model", model, "--effort", effort, "--output-format", "json",
                               "--no-session-persistence", PROMPT],
                              capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
        try:
            reply = json.loads(done.stdout)
        except json.JSONDecodeError:
            raise RuntimeError((done.stderr or done.stdout).strip()[-500:] or f"exit {done.returncode}")
        if reply.get("is_error") or not reply.get("result"):
            raise RuntimeError(str(reply.get("result") or reply.get("subtype") or "empty answer")[-500:])
        # Claude Code also makes small side calls on another model, so the slot's own model counts if it's there.
        usage = reply.get("modelUsage") or {}
        served = next((m for m in usage if same(model, m)), None) or (
            max(usage, key=lambda m: usage[m].get("costUSD", 0)) if usage else None)
        return reply["result"], served, "Claude Code's modelUsage, the model that served the answer"
    if tool == "codex":
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / "answer.md"
            done = subprocess.run(["codex", "exec", "-m", model, "-c", f"model_reasoning_effort={effort}",
                                   "-s", "read-only", "--skip-git-repo-check", "-o", str(out), PROMPT],
                                  capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
            answer = out.read_text().strip() if out.exists() else ""
        if done.returncode or not answer:
            raise RuntimeError((done.stderr or done.stdout).strip()[-500:] or f"exit {done.returncode}")
        header = re.search(r"^model: (\S+)", done.stderr, re.M)
        return answer, header and header.group(1), "Codex's header, the model it asked for (Codex doesn't report the one that answered)"
    if tool == "agy":
        message = json.dumps({"event": "user", "message": {"content": PROMPT}}) + "\n"
        with tempfile.TemporaryDirectory() as empty:
            done = subprocess.run(["agy", "-p=", "--model", model, "--effort", effort, "--mode", "plan",
                                   "--input-format", "stream-json", "--output-format", "stream-json",
                                   "--print-timeout", f"{max(1, timeout // 60)}m"],
                                  input=message, capture_output=True, text=True, timeout=timeout + 60, cwd=empty)
        result, served = {}, None
        for line in done.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                served = event.get("model") or (event.get("result") or {}).get("model") or served
                if event.get("event") == "result":
                    result = event.get("result") or {}
        if done.returncode or result.get("status") != "SUCCESS" or not result.get("response"):
            raise RuntimeError(str(result.get("error") or done.stderr.strip()[-500:] or f"exit {done.returncode}"))
        return result["response"], served, "Antigravity CLI's stream"
    done = subprocess.run(["pi", "-p", "--mode", "json", "--no-session", "--provider", "openrouter", "--model", model,
                           "--thinking", effort, PROMPT],
                          capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    reply = {}
    for line in done.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "message_end" and (event.get("message") or {}).get("role") == "assistant":
            reply = event["message"]
    answer = "".join(part.get("text", "") for part in reply.get("content", []) if part.get("type") == "text").strip()
    if done.returncode or reply.get("stopReason") == "error" or not answer:
        raise RuntimeError(str(reply.get("errorMessage") or done.stderr.strip()[-500:] or f"exit {done.returncode}"))
    return answer, reply.get("responseModel") or reply.get("model"), "OpenRouter's reply, the model that served the answer"


def test(name, slot, timeout):
    """One slot's verdict, falling back as the router does when its Claude usage on Google AI runs out."""
    start = time.time()
    try:
        answer, served, how = run(slot["tool"], slot["id"], slot["effort"], timeout)
    except Exception as error:
        text = str(error).strip() or type(error).__name__
        result = {"slot": name, "model": slot["name"], "id": slot["id"], "tool": TOOLS[slot["tool"]], "ok": False,
                  "error": text}
        if slot["tool"] == "agy" and "fallback" in slot and re.search(r"quota|rate.?limit|usage|exhaust|429", text, re.I):
            fallback = test(f"{name} fallback", {**slot["fallback"], "tool": "agy"}, timeout)
            result.update(ok=fallback["ok"], fallback=fallback, verdict=(
                "usage ran out, so the router runs the fallback, which works: not a failure" if fallback["ok"]
                else "usage ran out, and the fallback didn't pass either"))
        elif slot["tool"] == "pi" and re.search(r"\b402\b|credit", text, re.I):
            result["verdict"] = "OpenRouter credits or the key's limit ran out: top up, then check again (not a Repair)"
        else:
            result["verdict"] = "failed: follow Repair"
        return result
    result = {"slot": name, "model": slot["name"], "id": slot["id"], "tool": TOOLS[slot["tool"]],
              "seconds": round(time.time() - start), "answered_as": served, "how_known": how, "answer": answer[:80]}
    if not served:
        result.update(ok=True, verdict="answered; the tool didn't say which model")
    elif same(slot["id"], served):
        result.update(ok=True, verdict="answered; Codex asked for the named model" if slot["tool"] == "codex"
                      else "answered as the named model")
    else:
        result.update(ok=False, verdict=f"answered as {served}, not {slot['id']}: check the slot's model ID and the tool's version")
    return result


def own_pick(value, slot):
    model, _, effort = value.partition(":")
    return {**slot, "name": f"{model} (own pick)", "id": model, "effort": effort or slot["effort"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--plan", choices=list(SLOTS), help="the owner's plans' row: also test each slot with a one-word prompt")
    parser.add_argument("--slot", choices=["head-chef", "line-cook"], help="test only this slot (default: both)")
    parser.add_argument("--head-chef", metavar="ID[:EFFORT]", help="test this own pick as head-chef, on the plan's tool")
    parser.add_argument("--line-cook", metavar="ID[:EFFORT]", help="test this own pick as line-cook, on the plan's tool")
    parser.add_argument("--timeout", type=int, default=300, help="seconds per slot (default 300)")
    args = parser.parse_args()
    if not args.plan:
        if args.slot or args.head_chef or args.line_cook:
            parser.error("--slot, --head-chef and --line-cook need --plan")
        tools = {tool: status(tool, hub=tool in ("claude", "codex")) for tool in TOOLS}
        ready = [plan for plan, row in SLOTS.items()
                 if all(tools[s["tool"]].get("signed_in") for s in row.values())]
        report = {"tools": {TOOLS[t]: r for t, r in tools.items()}, "plans_ready_here": ready}
        print(json.dumps(report, indent=2))
        sys.exit(0 if ready else 1)

    row = dict(SLOTS[args.plan])
    for name, value in (("head-chef", args.head_chef), ("line-cook", args.line_cook)):
        if value:
            row[name] = own_pick(value, row[name])
    hub = args.plan not in ("google", "openrouter")  # those two get the hub through the prompt (setup step 3)
    tools = {TOOLS[t]: status(t, hub) for t in dict.fromkeys(s["tool"] for s in row.values())}
    slots = [test(name, slot, args.timeout) for name, slot in row.items() if args.slot in (None, name)]
    report = {"plan": args.plan, "tools": tools, "slots": slots}
    print(json.dumps(report, indent=2))
    sys.exit(0 if all(s["ok"] for s in slots) and not any("fix" in t for t in tools.values()) else 1)


if __name__ == "__main__":
    main()
