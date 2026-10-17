<p align="center"><img src="assets/logo.png" alt="Pixel-art router" width="120"></p>

# guava-router: Model Router

Part of the [Guava Stack](../README.md). Sends hard thinking and reviews to a **head-chef** model and heavy lifting to a **line-cook** model, on your Claude Pro and ChatGPT Plus plans or higher. Grok Bot or Muse routes each job through Claude Code and Codex on its own computer. Think of it as a kitchen:

<!-- models:kitchen roles=yes assets=../assets -->
<table>
<tr>
<td align="center" width="50%"><img src="../assets/head-chef.png" width="120" alt="Pixel-art head chef"> <img src="../assets/claude.svg" width="48" alt="Claude logo"><br><strong>head-chef</strong><br><sub>Plans and reviews. Today's best: Claude Opus 5.5</sub></td>
<td align="center" width="50%"><img src="../assets/line-cook.png" width="120" alt="Pixel-art line cook"> <img src="../assets/chatgpt.svg" width="48" alt="ChatGPT logo"><br><strong>line-cook</strong><br><sub>Does the work. Today's best: GPT-6.1 Sol</sub></td>
</tr>
<tr>
<td>Orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems.</td>
<td>Bulk execution, coding, sub-agent tasks, worker threads, long-running jobs.</td>
</tr>
</table>
<!-- /models -->

Works best with [guava-hub](../guava-hub/), since both tools read the same hub.

<!-- models:commands -->
| Slot | Model | Tool | Run it |
|---|---|---|---|
| head-chef | Claude Opus 5.5, effort high (`claude-opus-5-5`) | Claude Code | `claude -p --model claude-opus-5-5 --effort high "<task>" < /dev/null` |
| line-cook | GPT-6.1 Sol, effort high (`gpt-6.1-sol`) | Codex | `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |
<!-- /models -->

*Coming soon:* Claude-only and ChatGPT-only plans, local models, and more agents, such as Grok Build, Cursor, Copilot and OpenCode, through [acpx](https://github.com/openclaw/acpx).

- Model picks: [models.yaml](models.yaml) is the one place they're kept. To swap in a newer model, change it there and run `python3 scripts/sync-models.py` from the repo root, which updates every README and skill that shows them. Owners already set up say "check for newer models".
- Skill: [guava-router](skills/guava-router/SKILL.md)
- Power users, as a Claude Code plugin: `claude plugin marketplace add romeodiaz/guava-stack`, then `/plugin install guava-router@guava`
- Update: say "update guava-router", or "update guava-stack" for every piece.
- Uninstall: say "uninstall guava-router", or "uninstall guava-stack" for every piece.
- Install: see [Start here](../README.md#start-here) in the stack README.
