<p align="center"><img src="../assets/logo.png" alt="Pixel-art guava" width="120"></p>

# guava-bar: your kitchen in the menu bar

Part of the [Guava Stack](../README.md), and optional. A small Mac menu bar app that shows your guava-router **head-chef** and **line-cook** anytime, such as `Opus · Sol`, and swaps either one from a menu. A lite take on Peter Steinberger's [CodexBar](https://github.com/steipete/CodexBar), with models only.

- **See it:** click the guava for each slot's full model line and when your hub copy last refreshed.
- **Change it:** **Change line-cook**, pick a model and an effort, then **Change**. guava-bar asks Claude Code (or Codex) to make the change in your Notion hub and test it, so every assistant follows it. It takes a minute or two.
- **Picks:** today's best and next best for each slot from [models.yaml](../guava-router/models.yaml), at Low, Medium, High, xhigh or Max. Changing plans ("I only have ChatGPT now") still goes through "change my setup" in chat.

Needs a Mac on macOS 14 or later, the [Model Router](../guava-router/), and Claude Code or Codex signed in on that Mac. Your AI builds it on your Mac from this folder, so there's no download to trust and no Gatekeeper warning.

- Install: paste "Install guava-bar from github.com/romeodiaz/guava-stack" into Claude Code or Codex (or the Code or Codex tab in the Claude or ChatGPT app, set to Local).
- Skill: [guava-bar](skills/guava-bar/SKILL.md), which also lists exactly what a change runs.
- Update: say "update guava-bar", or "update guava-stack" for every piece.
- Uninstall: say "uninstall guava-bar", or "uninstall guava-stack" for every piece.
- From Terminal: `guava-bar show`, `guava-bar picks line-cook`, `guava-bar set line-cook "GPT-6.1 Sol (Medium) via Codex"`, `guava-bar refresh`.
- Build it yourself: `sh guava-bar/build.sh` (add `--no-install` to only build and test).
