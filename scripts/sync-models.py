#!/usr/bin/env python3
"""Copy the model picks in guava-router/models.yaml into every file that shows them.

Files mark generated parts with HTML comments:
    <!-- models:KIND key="value" ... -->  generated text  <!-- /models -->
Run from anywhere: python3 scripts/sync-models.py  (add --check to only report stale files)
"""
import re
import shlex
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = yaml.safe_load((ROOT / "guava-router" / "models.yaml").read_text())
SETUPS = CONFIG["setups"]
ROLES = CONFIG["roles"]
DEFAULT = next(s for s in SETUPS.values() if s.get("default"))
TOOLS = {"claude-code": "Claude Code", "codex": "Codex"}
APPS = {"claude": "Claude app", "chatgpt": "ChatGPT app"}
LOCAL = "Local models on your own hardware (Ollama, LM Studio and others)"
BLOCK = re.compile(r"<!-- models:(\S+)(.*?) -->(.*?)<!-- /models -->", re.S)


def effort(slot):
    return slot["effort"].capitalize()


def detailed(slot):
    return f"{slot['name']} ({effort(slot)}) via {TOOLS[slot['tool']]}"


def command(slot):
    if slot["tool"] == "claude-code":
        return f'claude -p --model {slot["id"]} --effort {slot["effort"]} "<task>" < /dev/null'
    return (f'codex exec -m {slot["id"]} -c model_reasoning_effort={slot["effort"]} '
            f'--skip-git-repo-check "<task>" < /dev/null')


def table(args):
    simple = args.get("style") == "simple"
    head = args.get("head", "Head chef")
    line = args.get("line", "Line cook")
    first = "You pay for" if simple else args.get("first", "You pay for")
    rows = [f"| {first} | {head} | {line} |", "|---|---|---|"]
    for s in SETUPS.values():
        if simple:
            rows.append(f"| {s['pays_for']} | {s['head_chef']['name']} | {s['line_cook']['name']} |")
        else:
            label = f"**{s['label']}** (default)" if s.get("default") else s["label"]
            rows.append(f"| {label} | {detailed(s['head_chef'])} | {detailed(s['line_cook'])} |")
    local = "Local models on your own computer" if simple else LOCAL
    rows.append(f"| {local} | *Coming soon* | *Coming soon* |")
    return "\n" + "\n".join(rows) + "\n"


def kitchen(args):
    head, line = DEFAULT["head_chef"], DEFAULT["line_cook"]
    pre_h = "Planner + reviewer. " if args.get("roles") == "yes" else ""
    pre_l = "Builder. " if args.get("roles") == "yes" else ""
    cap = lambda t: t[0].upper() + t[1:] + "."
    return f"""
<table>
<tr>
<td align="center" width="50%"><img src="assets/head-chef.png" width="120" alt="Pixel-art head chef"><br><strong>Head chef</strong><br><sub>{pre_h}Today's best: {head['name']}</sub></td>
<td align="center" width="50%"><img src="assets/line-cook.png" width="120" alt="Pixel-art line cook"><br><strong>Line cook</strong><br><sub>{pre_l}Today's best: {line['name']}</sub></td>
</tr>
<tr>
<td>{cap(ROLES['head_chef'])}</td>
<td>{cap(ROLES['line_cook'])}</td>
</tr>
</table>
"""


def setup(args):
    s = SETUPS[args["name"]]
    rows = ["| Slot | Model | Tool | Run it |", "|---|---|---|---|"]
    for slot_name, key in (("Planner", "head_chef"), ("Builder", "line_cook")):
        m = s[key]
        rows.append(f"| {slot_name} | {m['name']}, effort {m['effort']} (`{m['id']}`) | "
                    f"{TOOLS[m['tool']]} | `{command(m)}` |")
    h, l = s["head_chef"], s["line_cook"]
    if h["app"] == l["app"]:
        apps = (f"both in the {APPS[h['app']]}. Plan on {h['name']} and execute on {l['name']}, "
                "each in its own new chat.")
    else:
        apps = (f"plan in the {APPS[h['app']]} on {h['name']}; execute in the {APPS[l['app']]} "
                f"on {l['name']}. The hand-off moves the plan from one app to the other.")
    return "\n" + "\n".join(rows) + f"\n\n**In the apps:** {apps}\n"


def stack_example(args):
    h, l = DEFAULT["head_chef"], DEFAULT["line_cook"]
    return f"""
  ```
  Stack settings
  - Hub: Notion
  - Day-to-day assistant: Grok Bot
  - AI setup: {DEFAULT['label']}
  - Planner: {detailed(h)}
  - Builder: {detailed(l)}
  ```
  """


def default_pair(args):
    return f"{DEFAULT['head_chef']['name']} and {DEFAULT['line_cook']['name']}"


def app_routing_example(args):
    return (f"Model routing: plan with {DEFAULT['head_chef']['name']}. "
            f"Execute with {DEFAULT['line_cook']['name']}.")


KINDS = {"table": table, "kitchen": kitchen, "setup": setup,
         "stack-example": stack_example, "default-pair": default_pair,
         "app-routing-example": app_routing_example}


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
    verb = "Out of date" if check else "Updated"
    for p in stale:
        print(f"{verb}: {p}")
    if not stale:
        print("Everything matches models.yaml.")
    sys.exit(1 if check and stale else 0)


if __name__ == "__main__":
    main()
