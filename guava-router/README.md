<p align="center"><img src="assets/logo.png" alt="Pixel-art router" width="120"></p>

# guava-router: Model Router

Part of the [Guava Stack](../README.md). Sends hard thinking and reviews to a **head-chef** model and heavy lifting to a **line-cook** model, on your Claude Pro or ChatGPT Plus plan or higher, or both, or on Google AI Pro or Ultra alone. Grok Bot or Muse routes each job through Claude Code, Codex or both on its own computer, or through Google's Antigravity CLI on Google AI alone. Think of it as a kitchen:

<!-- models:kitchen assets=../assets -->
<table>
<tr>
<td align="center" width="50%"><img src="../assets/head-chef.png" width="120" alt="Pixel-art head chef"><br><strong>head-chef</strong><br><sub>Today's best: Claude Opus 5.5 <img src="../assets/claude.svg" width="20" alt="Claude logo"><br>Next best: GPT-6 Astra <img src="../assets/chatgpt.svg" width="20" alt="ChatGPT logo"></sub></td>
<td align="center" width="50%"><img src="../assets/line-cook.png" width="120" alt="Pixel-art line cook"><br><strong>line-cook</strong><br><sub>Today's best: GPT-6.1 Sol <img src="../assets/chatgpt.svg" width="20" alt="ChatGPT logo"><br>Next best: Claude Sonnet 5.5 <img src="../assets/claude.svg" width="20" alt="Claude logo"></sub></td>
</tr>
<tr>
<td>Orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems.</td>
<td>Bulk execution, coding, computer use, sub-agent tasks, worker threads, long-running jobs.</td>
</tr>
</table>
<!-- /models -->

Works best with [guava-hub](../guava-hub/), since both tools read the same hub.

On one plan, the other slot uses that company's next best. On Google AI alone, both slots run Claude models through Antigravity CLI, and each falls back to a Gemini model when its Claude usage runs out:

<!-- models:plans -->
| You pay for | head-chef | line-cook |
|---|---|---|
| Claude and ChatGPT (best) | Claude Opus 5.5 (High) via Claude Code | GPT-6.1 Sol (High) via Codex |
| Claude only | Claude Opus 5.5 (High) via Claude Code | Claude Sonnet 5.5 (High) via Claude Code |
| ChatGPT only | GPT-6 Astra (High) via Codex | GPT-6.1 Sol (High) via Codex |
| Google AI Pro or Ultra only | Claude Opus 5.5 (High) via Antigravity CLI, falling back to Gemini 4 Argon (High) when its usage runs out | Claude Sonnet 5.5 (High) via Antigravity CLI, falling back to Gemini 3.8 Flash (High) when its usage runs out |
<!-- /models -->

<!-- models:commands -->
| Slot | Model | Tool | Run it |
|---|---|---|---|
| head-chef | Claude Opus 5.5, effort high (`claude-opus-5-5`) | Claude Code | `claude -p --model claude-opus-5-5 --effort high "<task>" < /dev/null` |
| line-cook | GPT-6.1 Sol, effort high (`gpt-6.1-sol`) | Codex | `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |
| head-chef, ChatGPT only | GPT-6 Astra, effort high (`gpt-6-astra`) | Codex | `codex exec -m gpt-6-astra -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |
| line-cook, Claude only | Claude Sonnet 5.5, effort high (`claude-sonnet-5-5`) | Claude Code | `claude -p --model claude-sonnet-5-5 --effort high "<task>" < /dev/null` |
| head-chef, Google AI only | Claude Opus 5.5, effort high (`claude-opus-5-5-high`) | Antigravity CLI | `agy -p "<task>" --model claude-opus-5-5-high --effort high --mode accept-edits < /dev/null` |
| head-chef fallback, Google AI only | Gemini 4 Argon, effort high (`gemini-4-argon-high`) | Antigravity CLI | `agy -p "<task>" --model gemini-4-argon-high --effort high --mode accept-edits < /dev/null` |
| line-cook, Google AI only | Claude Sonnet 5.5, effort high (`claude-sonnet-5-5-high`) | Antigravity CLI | `agy -p "<task>" --model claude-sonnet-5-5-high --effort high --mode accept-edits < /dev/null` |
| line-cook fallback, Google AI only | Gemini 3.8 Flash, effort high (`gemini-3.8-flash-high`) | Antigravity CLI | `agy -p "<task>" --model gemini-3.8-flash-high --effort high --mode accept-edits < /dev/null` |
<!-- /models -->

*Coming soon:* local models, and more agents, such as Grok Build, Cursor, Copilot and OpenCode, through [acpx](https://github.com/openclaw/acpx).

- Model picks: [models.yaml](models.yaml) is the one place they're kept. To swap in a newer model, change it there and run `python3 scripts/sync-models.py` from the repo root, which updates every README and skill that shows them. Owners already set up say "check for newer models".
- Skill: [guava-router](skills/guava-router/SKILL.md)
- Update: say "update guava-router", or "update guava-stack" for every piece.
- Uninstall: say "uninstall guava-router", or "uninstall guava-stack" for every piece.
- Install: see [Start here](../README.md#start-here) in the stack README.
