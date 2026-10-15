<p align="center"><img src="assets/logo.png" alt="Guava logo" width="120"></p>

# guava-router: Model Router

Part of the [Guava Stack](../README.md). Sends hard thinking to a **planner** model and heavy lifting to a **worker** model, on the plans you already pay for. With Grok Bot, Muse or a coding tool, it routes through each model's command-line tool. With just the Claude or ChatGPT app (web, desktop or mobile), it adds instructions so every new chat checks your first request and sends you to the right model with a ready-to-paste prompt. Works best with [guava-hub](../guava-hub/), since both tools load your AI Context Hub.

| You pay for | Planner | Worker |
|---|---|---|
| **Claude + ChatGPT** (default) | Claude Opus 5.5 (High) via Claude Code | GPT-6.1 Sol (High) via Codex |
| ChatGPT only | Astra (High) via Codex | GPT-6.1 Sol (High) via Codex |
| Claude only | Claude Opus 5.5 (High) via Claude Code | Claude Sonnet 5.5 (High) via Claude Code |
| Other tools or a custom mix (Cursor, Devin, Droid, Amp and others) | Your pick | Your pick |

- Skill: [model-router-setup](skills/model-router-setup/SKILL.md), with details for each setup in [setups.md](skills/model-router-setup/setups.md)
- Claude Code: `/plugin install guava-router --marketplace romeodiaz/guava-stack`
- Install: see [Start here](../README.md#start-here) in the stack README.
