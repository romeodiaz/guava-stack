#!/usr/bin/env python3
"""Copy the model picks in guava-router/models.yaml into every file that shows them.

Files mark generated parts with HTML comments:
    <!-- models:KIND key="value" ... -->  generated text  <!-- /models -->
The oracle_council section is also written to guava-hub/skills/oracle-council/members.json, and
each plan row's slots to guava-router/skills/guava-router/slots.json for router-check.py.
Run from anywhere: python3 scripts/sync-models.py  (add --check to only report stale files)
"""
import json
import re
import shlex
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = yaml.safe_load((ROOT / "guava-router" / "models.yaml").read_text())
HEAD, LINE = CONFIG["head_chef"], CONFIG["line_cook"]
HEAD_NEXT, LINE_NEXT = HEAD["next_best"], LINE["next_best"]
GOOGLE_HEAD, GOOGLE_LINE = CONFIG["google_only"]["head_chef"], CONFIG["google_only"]["line_cook"]
OR_HEAD, OR_LINE = CONFIG["openrouter_only"]["head_chef"], CONFIG["openrouter_only"]["line_cook"]
ROLES = CONFIG["roles"]
COUNCIL = CONFIG["oracle_council"]
MEMBERS = ROOT / "guava-hub" / "skills" / "oracle-council" / "members.json"
SLOTS = ROOT / "guava-router" / "skills" / "guava-router" / "slots.json"
FOUNDER_MODE = json.loads((ROOT / "founder-mode" / ".claude-plugin" / "plugin.json").read_text())["version"]
BLOCK = re.compile(r"<!-- models:(\S+)(.*?) -->(.*?)<!-- /models -->", re.S)


def effort(slot):
    return slot["effort"].capitalize()


def detailed(slot, tool):
    return f"{slot['name']} ({effort(slot)}) via {tool}"


def company(slot):
    return "Claude" if slot["name"].startswith("Claude") else "ChatGPT"


def tool(slot):
    return "Claude Code" if company(slot) == "Claude" else "Codex"


def pick(slot, plan):
    """The slot's model for an owner who pays for only one plan."""
    return slot if company(slot) == plan else slot["next_best"]


def google(slot):
    """A google_only slot as shown in tables and settings: its Claude model, then its fallback."""
    return f"{detailed(slot, 'Antigravity CLI')}, falling back to {slot['fallback']['name']} ({effort(slot['fallback'])}) when its usage runs out"


def agy(slot):
    return f'agy -p "<task>" --model {slot["id"]} --effort {slot["effort"]} --mode accept-edits < /dev/null'


def pi(slot):
    return f'pi -p --provider openrouter --model {slot["id"]} --thinking {slot["effort"]} "<task>" < /dev/null'


def run(slot):
    if tool(slot) == "Claude Code":
        return f'claude -p --model {slot["id"]} --effort {slot["effort"]} "<task>" < /dev/null'
    return f'codex exec -m {slot["id"]} -c model_reasoning_effort={slot["effort"]} --skip-git-repo-check "<task>" < /dev/null'


def logo(img, name):
    if name.startswith("Claude"):
        return f'<img src="{img}/claude.svg" width="20" alt="Claude logo">'
    return f'<img src="{img}/chatgpt.svg" width="20" alt="ChatGPT logo">'


def picks(img, slot):
    return (f"Today's best: {slot['name']} {logo(img, slot['name'])}<br>"
            f"Next best: {slot['next_best']['name']} {logo(img, slot['next_best']['name'])}")


def kitchen(args):
    cap = lambda t: t[0].upper() + t[1:] + "."
    img = args.get("assets", "assets")
    size = args.get("size", "120")
    return f"""
<table>
<tr>
<td align="center" width="50%"><img src="{img}/head-chef.png" width="{size}" alt="Pixel-art head chef"><br><strong>head-chef</strong><br><sub>{picks(img, HEAD)}</sub></td>
<td align="center" width="50%"><img src="{img}/line-cook.png" width="{size}" alt="Pixel-art line cook"><br><strong>line-cook</strong><br><sub>{picks(img, LINE)}</sub></td>
</tr>
<tr>
<td>{cap(ROLES['head_chef'])}</td>
<td>{cap(ROLES['line_cook'])}</td>
</tr>
</table>
"""


def commands(args):
    row = lambda label, s: f"| {label} | {s['name']}, effort {s['effort']} (`{s['id']}`) | {tool(s)} | `{run(s)}` |"
    return "\n" + "\n".join([
        "| Slot | Model | Tool | Run it |",
        "|---|---|---|---|",
        row("head-chef", HEAD),
        row("line-cook", LINE),
        row(f"head-chef, {company(HEAD_NEXT)} only", HEAD_NEXT),
        row(f"line-cook, {company(LINE_NEXT)} only", LINE_NEXT),
        *[f"| {label} | {s['name']}, effort {s['effort']} (`{s['id']}`) | Antigravity CLI | `{agy(s)}` |"
          for label, s in (("head-chef, Google AI only", GOOGLE_HEAD),
                           ("head-chef fallback, Google AI only", GOOGLE_HEAD["fallback"]),
                           ("line-cook, Google AI only", GOOGLE_LINE),
                           ("line-cook fallback, Google AI only", GOOGLE_LINE["fallback"]))],
        *[f"| {label} | {s['name']}, effort {s['effort']} (`{s['id']}`) | Pi | `{pi(s)}` |"
          for label, s in (("head-chef, OpenRouter only", OR_HEAD), ("line-cook, OpenRouter only", OR_LINE))],
    ]) + "\n"


def plans(args):
    row = lambda label, h, l: f"| {label} | {detailed(h, tool(h))} | {detailed(l, tool(l))} |"
    return "\n" + "\n".join([
        "| You pay for | head-chef | line-cook |",
        "|---|---|---|",
        row("Claude and ChatGPT (best)", HEAD, LINE),
        *[row(f"{plan} only", pick(HEAD, plan), pick(LINE, plan)) for plan in ("Claude", "ChatGPT")],
        f"| Google AI Pro or Ultra only | {google(GOOGLE_HEAD)} | {google(GOOGLE_LINE)} |",
        f"| OpenRouter only, billed per use | {detailed(OR_HEAD, 'Pi')} | {detailed(OR_LINE, 'Pi')} |",
    ]) + "\n"


def one_plan(args):
    return (f"{LINE_NEXT['name']} as line-cook on {company(LINE_NEXT)} only, "
            f"and {HEAD_NEXT['name']} as head-chef on {company(HEAD_NEXT)} only. "
            f"On Google AI Pro or Ultra only, {GOOGLE_HEAD['name']} and {GOOGLE_LINE['name']} run through "
            f"Google's Antigravity CLI, and fall back to {GOOGLE_HEAD['fallback']['name']} and "
            f"{GOOGLE_LINE['fallback']['name']} when their usage runs out. With none of these plans, "
            f"{OR_HEAD['name']} and {OR_LINE['name']} run on OpenRouter, billed per use, through the Pi coding agent")


def stack_example(args):
    return f"""
  ```
  ## guava-stack settings
  ### guava-router
  head-chef
  - {detailed(HEAD, 'Claude Code')}
    - Orchestration, research, planning, brainstorming, copywriting, validation, review, verification, and fuzzy and hard problems. On important work, checks the line-cook's result before it's called done.
  line-cook
  - {detailed(LINE, 'Codex')}
    - Bulk execution, coding, computer use, sub-agent tasks, worker threads and long-running jobs.
  ### Rules
  - founder-mode v{FOUNDER_MODE}
  ```
  """


def default_pair(args):
    return f"{HEAD['name']} and {LINE['name']}"


def oracle_council(args):
    gpt, claude, gemini = COUNCIL["chatgpt"], COUNCIL["claude"], COUNCIL["gemini"]
    return "\n" + "\n".join([
        "| Seat | On your plan | Billed per use |",
        "|---|---|---|",
        f"| ChatGPT | {gpt['name']} via Codex (`{gpt['id']}`) | OpenRouter `{gpt['openrouter']}`, with no ChatGPT plan or when Codex fails |",
        f"| Claude | Max: {claude['max']['name']} via Claude Code (`{claude['max']['id']}`)<br>Pro: {claude['pro']['name']} via Claude Code (`{claude['pro']['id']}`) | OpenRouter {claude['openrouter']['name']} (`{claude['openrouter']['id']}`), only with no Claude plan |",
        f"| Gemini | Google AI Pro or Ultra: {gemini['name']} via Antigravity CLI (`{gemini['agy']}`) | Gemini API `{gemini['api']}`, or OpenRouter `{gemini['openrouter']}` |",
    ]) + f"\n\nEvery seat runs at {gpt['effort']} effort (high on Google's own routes, its top level).\n"


def slots():
    """Each plan row's head-chef and line-cook with the tool that runs it, for router-check.py."""
    slot = lambda s, t: {"name": s["name"], "id": s["id"], "effort": s["effort"], "tool": t,
                         **({"fallback": {k: s["fallback"][k] for k in ("name", "id", "effort")}} if "fallback" in s else {})}
    cli = lambda s: "claude" if tool(s) == "Claude Code" else "codex"
    one = lambda plan: {"head-chef": slot(pick(HEAD, plan), cli(pick(HEAD, plan))),
                        "line-cook": slot(pick(LINE, plan), cli(pick(LINE, plan)))}
    return {"claude-and-chatgpt": {"head-chef": slot(HEAD, cli(HEAD)), "line-cook": slot(LINE, cli(LINE))},
            "claude": one("Claude"), "chatgpt": one("ChatGPT"),
            "google": {"head-chef": slot(GOOGLE_HEAD, "agy"), "line-cook": slot(GOOGLE_LINE, "agy")},
            "openrouter": {"head-chef": slot(OR_HEAD, "pi"), "line-cook": slot(OR_LINE, "pi")}}


KINDS = {"kitchen": kitchen, "commands": commands, "plans": plans, "one-plan": one_plan,
         "stack-example": stack_example, "default-pair": default_pair,
         "oracle-council": oracle_council}


def render(match):
    kind, raw_args = match.group(1), match.group(2)
    args = dict(a.split("=", 1) for a in shlex.split(raw_args))
    return f"<!-- models:{kind}{raw_args} -->{KINDS[kind](args)}<!-- /models -->"


def main():
    check = "--check" in sys.argv
    stale = []
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text()
        new = BLOCK.sub(render, text)
        if new != text:
            stale.append(path.relative_to(ROOT))
            if not check:
                path.write_text(new)
    for path, data in ((MEMBERS, COUNCIL), (SLOTS, slots())):
        text = json.dumps(data, indent=2) + "\n"
        if not path.exists() or path.read_text() != text:
            stale.append(path.relative_to(ROOT))
            if not check:
                path.write_text(text)
    verb = "Out of date" if check else "Updated"
    for p in stale:
        print(f"{verb}: {p}")
    if not stale:
        print("Everything matches models.yaml.")
    sys.exit(1 if check and stale else 0)


if __name__ == "__main__":
    main()
