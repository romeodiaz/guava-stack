#!/usr/bin/env python3
"""Ask the council: one hard question to three models at once, each at max effort.

    python3 oracle-council.py --question question.md --out DIR --claude max|pro|none --chatgpt yes|no \
        [--file PATH_OR_GLOB ...] [--seat chatgpt|claude|gemini ...] [--dry-run] [--timeout MINUTES]

Seats and models come from members.json next to this script (written by
scripts/sync-models.py from guava-router/models.yaml). Each answer is saved as
DIR/<seat>.md, and DIR/council.json records which model and route served each seat.
Standard library only. OPENROUTER_API_KEY must be set for any seat that runs on OpenRouter.
"""
import argparse
import fnmatch
import glob
import json
import os
import subprocess
import sys
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
    deadline, text, cost = time.time() + timeout, [], None
    try:
        response = urllib.request.urlopen(request, timeout=600)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"HTTP {error.code}: {error.read().decode(errors='replace')[:500]}")
    with response:
        for raw in response:
            if time.time() > deadline:
                raise TimeoutError(f"no full answer after {timeout // 60} minutes")
            line = raw.decode().strip()
            if not line.startswith("data: ") or line == "data: [DONE]":
                continue
            chunk = json.loads(line[6:])
            if "error" in chunk:
                raise RuntimeError(chunk["error"].get("message", str(chunk["error"])))
            for choice in chunk.get("choices", []):
                text.append((choice.get("delta") or {}).get("content") or "")
            cost = (chunk.get("usage") or {}).get("cost", cost)
    answer = "".join(text).strip()
    if not answer:
        raise RuntimeError("empty answer")
    return answer, cost


def routes(seat, args):
    """The (model name, model id, route) attempts for a seat, in order."""
    member = MEMBERS[seat]
    if seat == "chatgpt":
        openrouter = (member["name"], member["openrouter"], "OpenRouter")
        return [(member["name"], member["id"], "Codex"), openrouter] if args.chatgpt == "yes" else [openrouter]
    if seat == "claude":
        pick = member[args.claude] if args.claude != "none" else member["openrouter"]
        return [(pick["name"], pick["id"], "OpenRouter" if args.claude == "none" else "Claude Code")]
    return [(member["name"], member["openrouter"], "OpenRouter")]


def ask(seat, args, prompt, results):
    effort, timeout = MEMBERS[seat]["effort"], args.timeout * 60
    out = args.out / f"{seat}.md"
    failures = []
    for name, model, route in routes(seat, args):
        start = time.time()
        try:
            if route == "Claude Code":
                answer, cost = run_claude(model, effort, prompt, timeout)
            elif route == "Codex":
                answer, cost = run_codex(model, effort, prompt, timeout, out)
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
    results[seat] = {"ok": False, "failures": failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--question", type=Path, required=True, help="the briefing and question, as markdown")
    parser.add_argument("--out", type=Path, required=True, help="folder for the answers")
    parser.add_argument("--claude", choices=["max", "pro", "none"], required=True, help="the owner's Claude plan")
    parser.add_argument("--chatgpt", choices=["yes", "no"], required=True, help="whether the owner has a ChatGPT plan")
    parser.add_argument("--file", action="append", default=[], help="file, folder or glob to include; !glob excludes")
    parser.add_argument("--seat", action="append", choices=list(MEMBERS),
                        help="ask only this seat, such as one that failed (default: all three)")
    parser.add_argument("--timeout", type=int, default=45, help="minutes per seat (default 45)")
    parser.add_argument("--dry-run", action="store_true", help="show files, size and routes without asking anyone")
    args = parser.parse_args()
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
