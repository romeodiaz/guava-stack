#!/usr/bin/env python3
"""Ask the council: one hard question to three models at once, each at max effort.

    python3 oracle-council.py --check
    python3 oracle-council.py --question question.md --out DIR --claude max|pro|none --chatgpt yes|no --google yes|no \
        [--file PATH_OR_GLOB ...] [--seat chatgpt|claude|gemini ...] [--dry-run] [--timeout MINUTES]

--check shows which of Claude Code, Codex and Antigravity CLI are installed and signed in
on a plan, and which API keys are set, so the owner can be walked through what's missing.

Seats and models come from members.json next to this script (written by
scripts/sync-models.py from guava-router/models.yaml). Each answer is saved as
DIR/<seat>.md, and DIR/council.json records which model and route served each seat.
Standard library only. Seats that run on an API read OPENROUTER_API_KEY or GEMINI_API_KEY.
"""
import argparse
import fnmatch
import glob
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEMBERS = json.loads((HERE / "members.json").read_text())
MAX_TOKENS = 196_000
MAX_FILE_BYTES = 1_000_000
SKIP_DIRS = {".git", "node_modules", "dist", "build", "coverage", ".next", ".turbo", "tmp",
             ".venv", "venv", "__pycache__"}
SECRETS = [".env", ".env.*", "*.pem", "*.key", "*.p12", "*.pfx", "id_rsa*", "id_ed25519*",
           "*credentials*", "*secret*", ".npmrc", ".netrc"]
PREAMBLE = """You are one of three independent experts on a council. The other two are different AI models answering the same question separately; the owner will compare all three answers.

Answer from the briefing and files below only. You have no tools, so don't ask for more files or try to run anything. Cite files as path:line when you rely on them. Say plainly where you are unsure or where the briefing leaves something out, and what would settle it. Take a clear position rather than listing options. End with a short "Bottom line" paragraph.

"""


def bundle(patterns):
    """Resolve --file patterns into (path, text) pairs, skipping secrets, binaries and big files."""
    excludes = [p[1:] for p in patterns if p.startswith("!")]
    found, skipped = [], []
    for pattern in (p for p in patterns if not p.startswith("!")):
        path = Path(pattern).expanduser()
        if path.is_dir():
            paths = sorted(p for p in path.rglob("*") if p.is_file())
        elif path.is_file():
            paths = [path]
        else:
            paths = sorted(Path(p) for p in glob.glob(pattern, recursive=True) if Path(p).is_file())
        for p in paths:
            if p in (f for f, _ in found) or SKIP_DIRS & set(p.parts):
                continue
            rel = str(p)
            if any(fnmatch.fnmatch(rel, x) or fnmatch.fnmatch(p.name, x) for x in excludes):
                continue
            if any(fnmatch.fnmatch(p.name.lower(), s) for s in SECRETS):
                skipped.append((rel, "looks like a secret"))
                continue
            if p.stat().st_size > MAX_FILE_BYTES:
                skipped.append((rel, "over 1 MB"))
                continue
            raw = p.read_bytes()
            if b"\0" in raw[:8192]:
                skipped.append((rel, "binary"))
                continue
            found.append((p, raw.decode("utf-8", errors="replace")))
    return found, skipped


def build_prompt(question, files):
    parts = [PREAMBLE, "# Briefing\n\n", question.strip(), "\n"]
    if files:
        parts.append("\n# Files\n")
        for path, text in files:
            numbered = "\n".join(f"{i:5}  {line}" for i, line in enumerate(text.splitlines(), 1))
            parts.append(f"\n## {path}\n\n```\n{numbered}\n```\n")
    return "".join(parts)


def without(*keys):
    """This environment minus API keys, so Claude Code and Codex use the owner's plan login."""
    return {k: v for k, v in os.environ.items() if k not in keys}


def run_claude(model, effort, prompt, timeout):
    cmd = ["claude", "-p", "--model", model, "--effort", effort, "--tools", "", "--strict-mcp-config",
           "--no-session-persistence", "--output-format", "json"]
    done = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout,
                          env=without("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"))
    try:
        reply = json.loads(done.stdout)
    except json.JSONDecodeError:
        raise RuntimeError((done.stderr or done.stdout).strip()[-500:] or f"exit {done.returncode}")
    if reply.get("is_error") or not reply.get("result"):
        raise RuntimeError(str(reply.get("result") or reply.get("subtype") or "empty answer")[-500:])
    return reply["result"], None


def run_codex(model, effort, prompt, timeout, out):
    out.unlink(missing_ok=True)
    cmd = ["codex", "exec", "-m", model, "-c", f"model_reasoning_effort={effort}", "-s", "read-only",
           "--skip-git-repo-check", "-o", str(out), "-"]
    done = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout,
                          env=without("OPENAI_API_KEY", "CODEX_API_KEY"))
    answer = out.read_text().strip() if out.exists() else ""
    if done.returncode or not answer:
        raise RuntimeError((done.stderr or done.stdout).strip()[-500:] or f"exit {done.returncode}")
    return answer, None


def run_agy(model, effort, prompt, timeout):
    """Antigravity CLI on the owner's Google AI Pro or Ultra login; the prompt goes in on stdin.
    -p takes a value, so it gets an empty one, and agy runs in an empty folder so its tools see nothing."""
    cmd = ["agy", "-p=", "--model", model, "--effort", effort, "--mode", "plan",
           "--input-format", "stream-json", "--output-format", "stream-json",
           "--print-timeout", f"{timeout // 60}m"]
    message = json.dumps({"event": "user", "message": {"content": prompt}}) + "\n"
    with tempfile.TemporaryDirectory() as empty:
        done = subprocess.run(cmd, input=message, capture_output=True, text=True, timeout=timeout + 60,
                              cwd=empty, env=without("GEMINI_API_KEY", "GOOGLE_API_KEY"))
    result = {}
    for line in done.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict) and event.get("event") == "result":
            result = event.get("result") or {}
    if done.returncode or result.get("status") != "SUCCESS" or not result.get("response"):
        raise RuntimeError(str(result.get("error") or done.stderr.strip()[-500:] or f"exit {done.returncode}"))
    return result["response"], None


def sse(request, deadline):
    """Yield each JSON event of a server-sent-events response, raising on HTTP errors and the deadline."""
    try:
        response = urllib.request.urlopen(request, timeout=600)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"HTTP {error.code}: {error.read().decode(errors='replace')[:500]}")
    with response:
        for raw in response:
            if time.time() > deadline:
                raise TimeoutError("no full answer before the timeout")
            line = raw.decode().strip()
            if line.startswith("data: ") and line != "data: [DONE]":
                yield json.loads(line[6:])


def run_gemini_api(model, effort, prompt, timeout):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"thinkingConfig": {"thinkingLevel": effort}}}
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:streamGenerateContent?alt=sse",
        data=json.dumps(body).encode(), headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    text = []
    for chunk in sse(request, time.time() + timeout):
        if "error" in chunk:
            raise RuntimeError(chunk["error"].get("message", str(chunk["error"])))
        for candidate in chunk.get("candidates", []):
            text += [part.get("text", "") for part in candidate.get("content", {}).get("parts", [])
                     if not part.get("thought")]
    answer = "".join(text).strip()
    if not answer:
        raise RuntimeError("empty answer")
    return answer, None


def run_openrouter(model, effort, prompt, timeout):
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "reasoning": {"effort": effort}, "stream": True, "usage": {"include": True}}
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "HTTP-Referer": "https://github.com/romeodiaz/guava-stack", "X-Title": "guava-stack oracle-council"})
    text, cost = [], None
    for chunk in sse(request, time.time() + timeout):
        if "error" in chunk:
            raise RuntimeError(chunk["error"].get("message", str(chunk["error"])))
        for choice in chunk.get("choices", []):
            text.append((choice.get("delta") or {}).get("content") or "")
        cost = (chunk.get("usage") or {}).get("cost", cost)
    answer = "".join(text).strip()
    if not answer:
        raise RuntimeError("empty answer")
    return answer, cost


def probe(cmd, strip, timeout=60):
    """Run a status command without the API keys in strip; (exit code, output), or None if it isn't installed."""
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, env=without(*strip),
                              stdin=subprocess.DEVNULL)
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        return 124, "timed out"
    return done.returncode, (done.stdout + done.stderr).strip()


def check():
    """What each seat can run on here. Never prints a key, only whether it's set."""
    report = {}
    version = probe(["claude", "--version"], [])
    status = probe(["claude", "auth", "status", "--json"], ["ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"])
    try:
        status = json.loads(status[1]) if status else {}
    except json.JSONDecodeError:
        status = {"error": status[1][-300:]}
    report["claude_code"] = {
        "installed": version[1].split()[0] if version else False,
        "signed_in": bool(status.get("loggedIn")),
        **{k: status[k] for k in ("authMethod", "subscriptionType", "error") if status.get(k)},
        "fix": None if status.get("loggedIn") else
            ("run `claude auth login` and sign in with the Claude account that has the Max or Pro plan" if version
             else "install with `npm i -g @anthropic-ai/claude-code`, then run `claude auth login`")}
    version = probe(["codex", "--version"], [])
    status = probe(["codex", "login", "status"], ["OPENAI_API_KEY", "CODEX_API_KEY"])
    on_plan = bool(status) and status[0] == 0 and "chatgpt" in status[1].lower()
    report["codex"] = {
        "installed": version[1].split()[-1] if version else False,
        "signed_in_with_chatgpt": on_plan, "status": status[1][-200:] if status else None,
        "fix": None if on_plan else
            ("run `codex login` and choose Sign in with ChatGPT (`codex login --device-auth` without a browser)" if version
             else "install with `npm i -g @openai/codex`, then run `codex login`")}
    version = probe(["agy", "--version"], [])
    models = probe(["agy", "models"], ["GEMINI_API_KEY", "GOOGLE_API_KEY"]) if version else None
    has_argon = bool(models) and models[0] == 0 and MEMBERS["gemini"]["agy"] in models[1]
    report["antigravity_cli"] = {
        "installed": version[1].split()[-1] if version else False,
        "gemini_argon_on_plan": has_argon, "models": models[1][-300:] if models and not has_argon else None,
        "fix": None if has_argon else
            ("run `agy` and sign in with the Google account that has Google AI Pro or Ultra; "
             "if it's signed in and Argon still isn't listed, the plan doesn't include it" if version
             else "install with `curl -fsSL https://antigravity.google/cli/install.sh | bash`, then run `agy` to sign in")}
    report["keys_set"] = {k: bool(os.environ.get(k)) for k in ("GEMINI_API_KEY", "OPENROUTER_API_KEY")}
    report["flags"] = {
        "--claude": "max or pro (ask the owner which plan)" if report["claude_code"]["signed_in"] else "none",
        "--chatgpt": "yes" if on_plan else "no",
        "--google": "yes" if has_argon else "no"}
    return report


def routes(seat, args):
    """The (model name, model id, route) attempts for a seat, in order."""
    member = MEMBERS[seat]
    if seat == "chatgpt":
        openrouter = (member["name"], member["openrouter"], "OpenRouter")
        return [(member["name"], member["id"], "Codex"), openrouter] if args.chatgpt == "yes" else [openrouter]
    if seat == "claude":
        pick = member[args.claude] if args.claude != "none" else member["openrouter"]
        return [(pick["name"], pick["id"], "OpenRouter" if args.claude == "none" else "Claude Code")]
    return ([(member["name"], member["agy"], "Antigravity CLI")] if args.google == "yes" else []) + \
        ([(member["name"], member["api"], "Gemini API")] if os.environ.get("GEMINI_API_KEY") else []) + \
        ([(member["name"], member["openrouter"], "OpenRouter")] if os.environ.get("OPENROUTER_API_KEY") else [])


def ask(seat, args, prompt, results):
    effort, timeout = MEMBERS[seat]["effort"], args.timeout * 60
    google_effort = "high" if effort in ("xhigh", "max") else effort  # Google's top thinking level
    out = args.out / f"{seat}.md"
    failures = []
    for name, model, route in routes(seat, args):
        start = time.time()
        try:
            if route == "Claude Code":
                answer, cost = run_claude(model, effort, prompt, timeout)
            elif route == "Codex":
                answer, cost = run_codex(model, effort, prompt, timeout, out)
            elif route == "Antigravity CLI":
                answer, cost = run_agy(model, google_effort, prompt, timeout)
            elif route == "Gemini API":
                answer, cost = run_gemini_api(model, google_effort, prompt, timeout)
            else:
                answer, cost = run_openrouter(model, effort, prompt, timeout)
        except Exception as error:  # one seat failing never stops the others
            failures.append(f"{route}: {str(error).strip() or type(error).__name__}")
            continue
        out.write_text(f"# {name} via {route}\n\n{answer}\n")
        results[seat] = {"ok": True, "model": name, "id": model, "route": route,
                         "seconds": round(time.time() - start), "cost_usd": cost,
                         "answer": str(out), "failed_first": failures}
        return
    results[seat] = {"ok": False, "failures": failures or [
        "no route: sign in to Antigravity CLI on a Google plan, or set GEMINI_API_KEY or OPENROUTER_API_KEY"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="show which CLIs are installed and signed in, and which keys are set")
    parser.add_argument("--question", type=Path, help="the briefing and question, as markdown")
    parser.add_argument("--out", type=Path, help="folder for the answers")
    parser.add_argument("--claude", choices=["max", "pro", "none"], help="the owner's Claude plan")
    parser.add_argument("--chatgpt", choices=["yes", "no"], help="whether Codex is signed in on the owner's ChatGPT plan")
    parser.add_argument("--google", choices=["yes", "no"],
                        help="whether Antigravity CLI is signed in on the owner's Google AI Pro or Ultra plan")
    parser.add_argument("--file", action="append", default=[], help="file, folder or glob to include; !glob excludes")
    parser.add_argument("--seat", action="append", choices=list(MEMBERS),
                        help="ask only this seat, such as one that failed (default: all three)")
    parser.add_argument("--timeout", type=int, default=45, help="minutes per seat (default 45)")
    parser.add_argument("--dry-run", action="store_true", help="show files, size and routes without asking anyone")
    args = parser.parse_args()
    if args.check:
        print(json.dumps(check(), indent=2))
        return
    missing = [f"--{k}" for k in ("question", "out", "claude", "chatgpt", "google") if getattr(args, k) is None]
    if missing:
        parser.error(f"needs {', '.join(missing)} (run --check first to see what to pass)")
    seats = args.seat or list(MEMBERS)

    files, skipped = bundle(args.file)
    prompt = build_prompt(args.question.read_text(), files)
    tokens = len(prompt) // 4
    plan = {"files": [str(p) for p, _ in files], "skipped": skipped, "tokens_estimate": tokens,
            "seats": {seat: [f"{name} via {route}" for name, _, route in routes(seat, args)] for seat in seats}}
    if args.dry_run or tokens > MAX_TOKENS:
        if tokens > MAX_TOKENS:
            plan["error"] = f"about {tokens:,} tokens, over the {MAX_TOKENS:,} limit: drop or narrow some files"
        print(json.dumps(plan, indent=2))
        sys.exit(1 if tokens > MAX_TOKENS else 0)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "prompt.md").write_text(prompt)
    results = {}
    threads = [threading.Thread(target=ask, args=(seat, args, prompt, results)) for seat in seats]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    log = args.out / "council.json"
    earlier = json.loads(log.read_text())["results"] if log.exists() else {}
    report = {**plan, "results": {**earlier, **results}}
    log.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    sys.exit(0 if any(r["ok"] for r in results.values()) else 1)


if __name__ == "__main__":
    main()
