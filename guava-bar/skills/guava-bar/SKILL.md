---
name: guava-bar
description: Installs, updates or removes guava-bar, an optional Mac menu bar app that shows the owner's head-chef and line-cook from guava-stack settings anytime and swaps either one from a menu. Use when the owner says "install guava-bar", "update guava-bar" or "uninstall guava-bar", or asks to see or change their models from the menu bar. Mac only, and needs Claude Code or Codex on that Mac.
---

**One yes per step.** Before each numbered step below, show its whole plan in your message text: every command, edit, install and setting change, word for word. Wait for one yes, then do the whole step and report what you did. Put the plan in your message text, never only inside a question or approval card, since some apps don't show what's in the card. Never ask for a yes to a change the owner hasn't seen.

# guava-bar

A small Mac menu bar app, a lite take on [CodexBar](https://github.com/steipete/CodexBar) with models only. The menu bar shows both slots at a glance, such as `Opus · Sol`. Its menu shows each slot's full model line and offers today's picks from guava-router's `models.yaml` at each effort, Low to Max. A pick, once the owner confirms it, runs Claude Code (or Codex) in the background on **Change your setup** in the guava-hub skill: it edits that one model line in guava-stack settings in Notion, refreshes the local copy and tests the new model. Notion stays the source of truth, so every assistant follows the change, and an edit made in Notion shows in the bar once the local copy refreshes. It doesn't show usage limits.

The app is also a command, `guava-bar`: `guava-bar show`, `guava-bar picks line-cook`, `guava-bar set line-cook "<a line from picks>"` and `guava-bar refresh`.

## Before you start
These only read, so they need no yes:
- **A Mac** on macOS 14 or later: `sw_vers -productVersion`. Anywhere else, say guava-bar is Mac only and stop.
- **Claude Code or Codex** installed and signed in on this Mac: `claude --version`, `codex --version`. guava-bar uses Claude Code when it's there, otherwise Codex. With neither, say guava-bar needs one to change anything and stop. On Google AI or OpenRouter alone, that usually means saying "change my setup" in Antigravity or Pi instead. In the Claude or ChatGPT app, it runs from their Code or Codex tab set to Local.
- **The Model Router** is on: guava-stack settings has `head-chef` and `line-cook` lines. Without them, say guava-bar has nothing to show until the router is on ("turn on the router"), and stop.
- **Xcode Command Line Tools**, which build the app: `xcode-select -p`. If it fails, step 1 of the plan is `xcode-select --install`, which opens Apple's installer: the owner clicks **Install**, waits a few minutes and says done.
- **The local hub copy**: `~/.guava-hub/sync.md`. Missing is fine: **Refresh from Notion** in the menu builds it.

## Install
1. **Build it.** From a local copy of guava-stack, or a fresh one: `tmp=$(mktemp -d) && git clone --depth 1 https://github.com/romeodiaz/guava-stack "$tmp/guava-stack" && sh "$tmp/guava-stack/guava-bar/build.sh"`. The script builds the app, tests it, puts `GuavaBar.app` in `~/Applications`, links the `guava-bar` command into `~/.local/bin` and opens the app. It changes nothing else.
2. **Check it:** `~/.local/bin/guava-bar show` prints the same head-chef and line-cook lines as guava-stack settings, and the guava is in the menu bar. No icon: the menu bar may be full, or hidden by a menu bar manager; quit an app or two and look again.
3. **Offer Open at login:** the owner clicks **Open at login** in guava-bar's menu, so it's always there. It shows in System Settings > General > Login Items.

Confirm in two lines: where the app is, what `guava-bar show` printed, and how to change a slot (click the icon, **Change line-cook**, pick a model and an effort, then **Change**).

## Update
Use this when the owner says **"update guava-bar"**, or when the guava-hub skill's Update step sends you here. Run **Install** step 1 with the newest files: it replaces the app in place. Then **Install** step 2, and check **Open at login** is still ticked if the owner had it on. Update again whenever guava-router's `models.yaml` changes, since the picks are built into the app.

## Uninstall
Use this when the owner says **"uninstall guava-bar"**, or when the guava-hub skill's Uninstall step sends you here.
1. The owner turns off **Open at login** in guava-bar's menu, if it's on.
2. `pkill -f 'GuavaBar.app/Contents/MacOS/guava-bar'`, then delete `~/Applications/GuavaBar.app`, and `~/.local/bin/guava-bar` if it's a link to that app (`readlink ~/.local/bin/guava-bar`).
3. Nothing in Notion or `~/.guava-hub` needs undoing: guava-bar only changed what the owner picked, through **Change your setup**.

## What a change runs
Show this to the owner when they ask what guava-bar can do on their computer. After the confirm, it runs one of these from `~/.guava-hub`, with no input, and stops it after 10 minutes:
- `claude -p "<the change>" --allowedTools mcp__claude_ai_Notion mcp__notion Read Edit Write "Bash(claude -p:*)" "Bash(codex exec:*)" "Bash(agy -p:*)" "Bash(date:*)" "Bash(find:*)" "Bash(grep:*)"`: Notion's tools, the files in the local copy, the one-line model tests, and nothing else.
- With no Claude Code: `codex exec --skip-git-repo-check --sandbox workspace-write "<the change>"`.

The prompt names the slot, the old and new model lines, and says the owner already confirmed this one change in guava-bar. It tells the session to follow **Change your setup**, edit only that model line, mark it "(own pick)" if it isn't today's pick for the owner's plans, leave `~/.claude/settings.json` and `~/.codex/config.toml` alone (this is the owner's own computer, not a bot's), test the new model and end with `done: …` or `failed: …`. The menu shows that last line.

## If something fails
- **The bar shows an old model:** the local copy refreshes when an AI session runs, or when the owner clicks **Refresh from Notion**.
- **A change failed:** the menu shows the reason. Run `guava-bar set <slot> "<line>"` in Terminal to see it again, or say "change my setup" in Claude or ChatGPT instead.
- **"guava-bar needs Claude Code or Codex":** install one as guava-router's step 2 says, sign in, and try again.
