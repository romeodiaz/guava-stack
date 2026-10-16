<p align="center"><img src="assets/logo.png" alt="Pixel-art router" width="120"></p>

# guava-router: Model Router

Part of the [Guava Stack](../README.md). Sends hard thinking and reviews to a **head-chef** model and heavy lifting to a **line-cook** model, on the plans you already pay for. With Grok Bot, Muse or the Claude desktop app's Code tab, it routes through each model's command-line tool. With just the Claude or ChatGPT app (web, desktop or mobile), it adds instructions so every new chat checks your first request and sends you to the right model with a ready-to-paste prompt. Think of it as a kitchen:

<!-- models:kitchen roles=yes -->
<table>
<tr>
<td align="center" width="50%"><img src="assets/head-chef.png" width="120" alt="Pixel-art head chef"><br><strong>head-chef</strong><br><sub>Plans and reviews. Today's best: Claude Opus 5.5</sub></td>
<td align="center" width="50%"><img src="assets/line-cook.png" width="120" alt="Pixel-art line cook"><br><strong>line-cook</strong><br><sub>Does the work. Today's best: GPT-6.1 Sol</sub></td>
</tr>
<tr>
<td>Orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems.</td>
<td>Bulk execution, coding, sub-agent tasks, worker threads, long-running jobs.</td>
</tr>
</table>
<!-- /models -->

Works best with [guava-hub](../guava-hub/), since both tools read the same hub.

<!-- models:table -->
| You pay for | head-chef | line-cook |
|---|---|---|
| **Claude + ChatGPT** (default) | Claude Opus 5.5 (High) via Claude Code | GPT-6.1 Sol (High) via Codex |
| ChatGPT only | GPT-6 Astra (High) via Codex | GPT-6.1 Sol (High) via Codex |
| Claude only | Claude Opus 5.5 (High) via Claude Code | Claude Sonnet 5.5 (High) via Claude Code |
| Local models on your own hardware (Ollama, LM Studio and others) | *Coming soon* | *Coming soon* |
<!-- /models -->

- Model picks: [models.yaml](models.yaml) is the one place they're kept. To swap in a newer model, change it there and run `python3 scripts/sync-models.py` from the repo root, which updates every README and skill that shows them. Owners already set up say "check for newer models".
- Skill: [guava-router](skills/guava-router/SKILL.md), with details for each setup in [setups.md](skills/guava-router/setups.md)
- Claude Code: `/plugin install guava-router --marketplace romeodiaz/guava-stack`
- Update: say "update guava-router", or "update guava-stack" for every piece.
- Install: see [Start here](../README.md#start-here) in the stack README.
