#!/usr/bin/env python3
"""Copy the model picks in guava-router/models.yaml into every file that shows them.

Files mark generated parts with HTML comments:
    <!-- models:KIND key="value" ... -->  generated text  <!-- /models -->
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
ROLES = CONFIG["roles"]
FOUNDER_MODE = json.loads((ROOT / "founder-mode" / ".claude-plugin" / "plugin.json").read_text())["version"]
BLOCK = re.compile(r"<!-- models:(\S+)(.*?) -->(.*?)<!-- /models -->", re.S)


def effort(slot):
    return slot["effort"].capitalize()


def detailed(slot, tool):
    return f"{slot['name']} ({effort(slot)}) via {tool}"


def kitchen(args):
    pre_h = "Plans and reviews. " if args.get("roles") == "yes" else ""
    pre_l = "Does the work. " if args.get("roles") == "yes" else ""
    cap = lambda t: t[0].upper() + t[1:] + "."
    img = args.get("assets", "assets")
    return f"""
<table>
<tr>
<td align="center" width="50%"><img src="{img}/head-chef.png" width="120" alt="Pixel-art head chef"><br><strong>head-chef</strong><br><sub>{pre_h}Today's best: {HEAD['name']}</sub></td>
<td align="center" width="50%"><img src="{img}/line-cook.png" width="120" alt="Pixel-art line cook"><br><strong>line-cook</strong><br><sub>{pre_l}Today's best: {LINE['name']}</sub></td>
</tr>
<tr>
<td>{cap(ROLES['head_chef'])}</td>
<td>{cap(ROLES['line_cook'])}</td>
</tr>
</table>
"""


def commands(args):
    h, l = HEAD, LINE
    return f"""
| Slot | Model | Tool | Run it |
|---|---|---|---|
| head-chef | {h['name']}, effort {h['effort']} (`{h['id']}`) | Claude Code | `claude -p --model {h['id']} --effort {h['effort']} "<task>" < /dev/null` |
| line-cook | {l['name']}, effort {l['effort']} (`{l['id']}`) | Codex | `codex exec -m {l['id']} -c model_reasoning_effort={l['effort']} --skip-git-repo-check "<task>" < /dev/null` |
"""


def stack_example(args):
    return f"""
  ```
  ## guava-stack settings
  ### Rules
  - founder-mode v{FOUNDER_MODE}
  ### guava-router
  head-chef
  - {detailed(HEAD, 'Claude Code')}
    - Orchestration, research, planning, brainstorming, copywriting, validation, review, verification, and fuzzy and hard problems. On important work, checks the line-cook's result before it's called done.
  line-cook
  - {detailed(LINE, 'Codex')}
    - Bulk execution, coding, sub-agent tasks, worker threads and long-running jobs.
  ```
  """


def default_pair(args):
    return f"{HEAD['name']} and {LINE['name']}"


KINDS = {"kitchen": kitchen, "commands": commands,
         "stack-example": stack_example, "default-pair": default_pair}


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
