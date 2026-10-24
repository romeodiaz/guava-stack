<p align="center"><img src="../assets/logo.png" alt="Pixel-art guava" width="120"></p>

# guava-bar: your kitchen in the menu bar

Part of the [Guava Stack](../README.md), and optional. A small Mac menu bar app that shows your guava-router **head-chef** and **line-cook** anytime, such as `Opus · Sol`, and swaps either one from a menu. A lite take on Peter Steinberger's [CodexBar](https://github.com/steipete/CodexBar), with models only.

- **See it:** click the guava for each slot's full model line and when your hub copy last refreshed.
- **Change it:** **Change line-cook**, then pick a model and an effort. Your Mac switches at once, so you can get back to work. In the background guava-bar tests the new model (switching back if it can't answer) and updates your Notion hub, so your bots and the Claude and ChatGPT apps follow within a minute or two.
- **Switch both:** move head-chef and line-cook to another plan's pair in one click, such as Claude Opus 5.5 + GPT-6.1 Sol, Gemini 4 Argon + Gemini 3.8 Flash via Antigravity CLI, or Kimi K3.1 Pro + DeepSeek V4.1 Flash 1017 via Pi. Your bots follow, as long as they have that plan's tool too ("change my setup" in the bot installs it).
- **Picks:** today's picks for each slot from [models.yaml](../guava-router/models.yaml), for every AI tool on your Mac (Claude Code, Codex, Antigravity CLI, Pi), at Low, Medium, High, xhigh or Max (Low to High on Antigravity CLI, its top level).

Needs a Mac on macOS 14 or later, the [Model Router](../guava-router/), and Claude Code or Codex signed in on that Mac. Your AI builds it on your Mac from this folder, so there's no download to trust and no Gatekeeper warning.

- Install: paste "Install guava-bar from github.com/romeodiaz/guava-stack" into Claude Code or Codex (or the Code or Codex tab in the Claude or ChatGPT app, set to Local).
- Skill: [guava-bar](skills/guava-bar/SKILL.md), which also lists exactly what a change runs.
- Update: say "update guava-bar", or "update guava-stack" for every piece.
- Uninstall: say "uninstall guava-bar", or "uninstall guava-stack" for every piece.
- From Terminal: `guava-bar show`, `guava-bar picks line-cook`, `guava-bar pairs`, `guava-bar set line-cook "GPT-6.1 Sol (Medium) via Codex"`, `guava-bar refresh`.
- Build it yourself: `sh guava-bar/build.sh` (add `--no-install` to only build and test).
