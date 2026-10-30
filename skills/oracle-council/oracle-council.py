#!/usr/bin/env python3
"""Ask the council: one hard question to three models at once.

ChatGPT and Claude run at max effort; Gemini uses the effort in members.json.

    python3 oracle-council.py --check
    python3 oracle-council.py --login [--headless]
    python3 oracle-council.py --question question.md --out DIR --claude max|pro|none --chatgpt yes|no \
        [--file PATH_OR_GLOB ...] [--seat chatgpt|claude|gemini ...] [--no-web] [--dry-run] [--timeout MINUTES]

--check shows which of Claude Code and Codex are installed and signed in
on a plan and whether an OpenRouter key is set, so the owner
can be walked through what's missing.

Seats and models come from members.json next to this script. Each answer is saved as
DIR/<seat>.md, and DIR/council.json records which model and route served each seat.
Standard library only. OpenRouter seats read OPENROUTER_API_KEY, then the key saved by
--login at $XDG_CONFIG_HOME/guava-stack/openrouter-key (default ~/.config/guava-stack/openrouter-key).
ChatGPT uses only Codex with --chatgpt yes, or OpenRouter with --chatgpt no.
Gemini runs on OpenRouter only. OpenRouter is billed per use and only uses providers
that do not store or train on data.
"""
import argparse
import base64
import fnmatch
import functools
import glob
import hashlib
import http.server
import json
import os
import secrets
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
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

Answer from the briefing and files below{only}. {tools} Cite files as path:line when you rely on them. Say plainly where you are unsure or where the briefing leaves something out, and what would settle it. Take a clear position rather than listing options. End with a short "Bottom line" paragraph.

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


def build_prompt(question, files, web):
    tools = ("You can search the web and read pages: use that to check current facts such as prices, releases "
             "and versions, and cite the URLs you rely on. Never put private details from the briefing or files "
             "(client or people's names, internal numbers, code or document text) into a search or URL. You can't "
             "read or run anything on this computer, so don't ask for more files."
             if web else "Don't search the web or use any tools, and don't ask for more files or try to run anything.")
    parts = [PREAMBLE.format(only="" if web else " only", tools=tools), "# Briefing\n\n", question.strip(), "\n"]
    if files:
        parts.append("\n# Files\n")
        for path, text in files:
            numbered = "\n".join(f"{i:5}  {line}" for i, line in enumerate(text.splitlines(), 1))
            parts.append(f"\n## {path}\n\n```\n{numbered}\n```\n")
    return "".join(parts)


def without(*keys):
    """This environment minus API keys, so Claude Code and Codex use the owner's plan login."""
    return {k: v for k, v in os.environ.items() if k not in keys}


def run_claude(model, effort, prompt, timeout, web):
    cmd = ["claude", "-p", "--model", model, "--effort", effort, "--tools", "WebSearch,WebFetch" if web else "",
           "--strict-mcp-config", "--no-session-persistence", "--output-format", "json"]
    if web:
        cmd += ["--allowedTools", "WebSearch,WebFetch"]
    done = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout,
                          env=without("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"))
    try:
        reply = json.loads(done.stdout)
    except json.JSONDecodeError:
        raise RuntimeError((done.stderr or done.stdout).strip()[-500:] or f"exit {done.returncode}")
    if reply.get("is_error") or not reply.get("result"):
        raise RuntimeError(str(reply.get("result") or reply.get("subtype") or "empty answer")[-500:])
    return reply["result"], None


def run_codex(model, effort, prompt, timeout, out, web):
    out.unlink(missing_ok=True)
    cmd = ["codex", "exec", "-m", model, "-c", f"model_reasoning_effort={effort}", "-s", "read-only",
           "--skip-git-repo-check", "-o", str(out), "-"]
    if web:
        cmd.insert(1, "--search")
    done = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout,
                          env=without("OPENAI_API_KEY", "CODEX_API_KEY"))
    answer = out.read_text().strip() if out.exists() else ""
    if done.returncode or not answer:
        raise RuntimeError((done.stderr or done.stdout).strip()[-500:] or f"exit {done.returncode}")
    return answer, None


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


def openrouter_key_file():
    """Where --login saves the OpenRouter key."""
    config = os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config"
    return Path(config) / "guava-stack" / "openrouter-key"


@functools.cache
def openrouter_key():
    """Read the environment first, then the saved key."""
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if key:
        return key
    try:
        return openrouter_key_file().read_text().strip() or None
    except OSError:
        return None


def code_challenge(verifier):
    """The S256 PKCE challenge, without padding."""
    return base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")


def callback_server(state):
    """Accept a login code only with the matching state."""
    class Callback(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            url = urllib.parse.urlsplit(self.path)
            query = urllib.parse.parse_qs(url.query)
            valid = url.path == "/callback" and query.get("state") == [state] and len(query.get("code", [])) == 1
            if valid:
                self.server.code = query["code"][0]
            page = b"Sign-in received. You can close this page." if valid else b"Invalid callback. You can close this page."
            self.send_response(200 if valid else 400)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)

        def log_message(self, format, *args):
            pass

    server = http.server.HTTPServer(("127.0.0.1", 0), Callback)
    server.code = None
    return server


def login(headless=False):
    """Sign in with PKCE and save the new key privately."""
    verifier, state = secrets.token_urlsafe(64), secrets.token_urlsafe(32)
    params = {"code_challenge": code_challenge(verifier), "code_challenge_method": "S256",
              "state": state, "key_label": "guava-stack oracle-council"}
    if headless:
        print("https://openrouter.ai/auth?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote))
        print("Open this URL; the page will show a code.")
        code = input("Code: ").strip()
    else:
        with callback_server(state) as server:
            params["callback_url"] = f"http://localhost:{server.server_port}/callback"
            url = "https://openrouter.ai/auth?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
            print(url, flush=True)
            try:
                webbrowser.open(url)
            except webbrowser.Error:
                pass
            deadline = time.monotonic() + 600
            while not server.code:
                server.timeout = max(0, deadline - time.monotonic())
                if not server.timeout:
                    raise SystemExit("OpenRouter sign-in timed out; run --login again.")
                server.handle_request()
            code = server.code
    if not code:
        raise SystemExit("No sign-in code received; run --login again.")
    request = urllib.request.Request(
        "https://openrouter.ai/api/v1/auth/keys",
        data=json.dumps({"code": code, "code_verifier": verifier, "code_challenge_method": "S256"}).encode(),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            key = json.load(response).get("key")
        if not isinstance(key, str) or not key.strip():
            raise ValueError("missing key")
    except (OSError, ValueError):
        raise SystemExit("OpenRouter key exchange failed; run --login again.")
    path = openrouter_key_file()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.parent.chmod(0o700)
    fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as file:
        os.chmod(path, 0o600)
        file.write(key.strip() + "\n")
    openrouter_key.cache_clear()
    print(f"Signed in to OpenRouter. Key saved to {path}")
    print("Tip: set a monthly credit limit on the key at https://openrouter.ai/settings/keys")


def run_openrouter(model, effort, prompt, timeout, web):
    key = openrouter_key()
    if not key:
        raise RuntimeError("not signed in to OpenRouter: run `python3 oracle-council.py --login`, or set OPENROUTER_API_KEY")
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "reasoning": {"effort": effort}, "stream": True, "usage": {"include": True},
            "provider": {"data_collection": "deny"}}
    if web:
        body["plugins"] = [{"id": "web"}]
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
    claude = probe(["claude", "auth", "status", "--json"], ["ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"])
    try:
        claude = json.loads(claude[1]) if claude else {}
    except json.JSONDecodeError:
        claude = {"error": claude[1][-300:]}
    report["claude_code"] = {
        "installed": version[1].split()[0] if version else False,
        "signed_in": bool(claude.get("loggedIn")),
        **{k: claude[k] for k in ("authMethod", "subscriptionType", "error") if claude.get(k)},
        "fix": None if claude.get("loggedIn") else
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
    key = openrouter_key()
    report["openrouter"] = {
        "key_set": bool(key),
        "source": ("OPENROUTER_API_KEY" if os.environ.get("OPENROUTER_API_KEY", "").strip() else "key file") if key else None,
        "fix": None if key else
            "run `python3 oracle-council.py --login` to sign in to OpenRouter in your browser (add --headless on a computer without one), or set OPENROUTER_API_KEY"}
    report["flags"] = {
        "--claude": (claude.get("subscriptionType") if claude.get("subscriptionType") in ("max", "pro")
                     else "max or pro (ask the owner which plan)") if report["claude_code"]["signed_in"] else "none",
        "--chatgpt": "yes" if on_plan else "no"}
    return report


def routes(seat, args):
    """The (model name, model id, route) attempts for a seat, in order."""
    member = MEMBERS[seat]
    if seat == "chatgpt":
        if args.chatgpt == "yes":
            return [(member["name"], member["id"], "Codex")]
        return [(member["name"], member["openrouter"], "OpenRouter")]
    if seat == "claude":
        pick = member[args.claude] if args.claude != "none" else member["openrouter"]
        return [(pick["name"], pick["id"], "OpenRouter" if args.claude == "none" else "Claude Code")]
    return [(member["name"], member["openrouter"], "OpenRouter")]


def ask(seat, args, prompt, results):
    effort, timeout = MEMBERS[seat]["effort"], args.timeout * 60
    web = not args.no_web
    out = args.out / f"{seat}.md"
    failures = []
    for name, model, route in routes(seat, args):
        start = time.time()
        try:
            if route == "Claude Code":
                answer, cost = run_claude(model, effort, prompt, timeout, web)
            elif route == "Codex":
                answer, cost = run_codex(model, effort, prompt, timeout, out, web)
            else:
                answer, cost = run_openrouter(model, effort, prompt, timeout, web)
        except Exception as error:  # one seat failing never stops the others
            failures.append(f"{route}: {str(error).strip() or type(error).__name__}")
            if route == "Codex":
                failures[-1] += ("; to run this seat on OpenRouter instead, billed per use, "
                                 "rerun with --seat chatgpt --chatgpt no once the owner says yes")
            continue
        out.write_text(f"# {name} via {route}\n\n{answer}\n")
        results[seat] = {"ok": True, "model": name, "id": model, "route": route,
                         "seconds": round(time.time() - start), "cost_usd": cost,
                         "answer": str(out), "failed_first": failures}
        return
    results[seat] = {"ok": False, "failures": failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="show which CLIs are installed and signed in, and which keys are set")
    parser.add_argument("--login", action="store_true", help="sign in to OpenRouter and save a key")
    parser.add_argument("--headless", action="store_true", help="show a sign-in code instead of using a browser callback")
    parser.add_argument("--question", type=Path, help="the briefing and question, as markdown")
    parser.add_argument("--out", type=Path, help="folder for the answers")
    parser.add_argument("--claude", choices=["max", "pro", "none"], help="the owner's Claude plan")
    parser.add_argument("--chatgpt", choices=["yes", "no"], help="whether Codex is signed in on the owner's ChatGPT plan")
    parser.add_argument("--file", action="append", default=[], help="file, folder or glob to include; !glob excludes")
    parser.add_argument("--seat", action="append", choices=list(MEMBERS),
                        help="ask only this seat, such as one that failed (default: all three)")
    parser.add_argument("--timeout", type=int, default=45, help="minutes per seat (default 45)")
    parser.add_argument("--no-web", action="store_true",
                        help="turn off web search, such as when the briefing or files hold client-confidential details")
    parser.add_argument("--dry-run", action="store_true", help="show files, size and routes without asking anyone")
    args = parser.parse_args()
    if args.check:
        print(json.dumps(check(), indent=2))
        return
    if args.login:
        login(args.headless)
        return
    missing = [f"--{k}" for k in ("question", "out", "claude", "chatgpt") if getattr(args, k) is None]
    if missing:
        parser.error(f"needs {', '.join(missing)} (run --check first to see what to pass)")
    seats = args.seat or list(MEMBERS)

    files, skipped = bundle(args.file)
    prompt = build_prompt(args.question.read_text(), files, not args.no_web)
    tokens = len(prompt) // 4
    plan = {"files": [str(p) for p, _ in files], "skipped": skipped, "tokens_estimate": tokens, "web": not args.no_web,
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
