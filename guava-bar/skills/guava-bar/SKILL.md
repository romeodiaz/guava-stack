---
name: guava-bar
description: Installs, updates or removes guava-bar, an optional Mac menu bar app that shows the owner's head-chef and line-cook from guava-stack settings anytime and swaps either one from a menu. Use when the owner says "install guava-bar", "update guava-bar" or "uninstall guava-bar", or asks to see or change their models from the menu bar. Mac only, and needs Claude Code, Codex or Pi on that Mac.
---

**One yes per step.** Before each numbered step below, show its whole plan in your message text: every command, edit, install and setting change, word for word. Wait for one yes, then do the whole step and report what you did. Put the plan in your message text, never only inside a question or approval card, since some apps don't show what's in the card. Never ask for a yes to a change the owner hasn't seen.

# guava-bar

A small Mac menu bar app, a lite take on [CodexBar](https://github.com/steipete/CodexBar) with models only. The menu bar shows both slots at a glance: the head-chef and line-cook pixel art, each with its model's short name, such as `Opus` and `Sol`. Its menu shows each slot's full model line and offers today's picks from guava-router's `models.yaml` for every AI tool installed on the Mac (Claude Code, Codex, Antigravity CLI and Pi) and the ones the slots already name, at each effort: Low to Max, or Low, Medium and High on Antigravity CLI, which has no higher level. **Switch both** sets head-chef and line-cook together to one plan's pair, such as Claude Opus 5.5 + GPT-6.1 Sol, Gemini 4 Argon + Gemini 3.8 Flash via Antigravity CLI, or Kimi K3.1 Pro + DeepSeek V4.1 Flash 1017 via Pi, so an owner with several plans can move their whole kitchen, bots included, in one click. On the owner's Mac, guava-bar is the main place to change models: a pick switches that slot in the local copy (`~/.guava-hub/context.md`) at once, which Claude Code and Codex there read before every hand-off. In the background it then tests the new model, switching back if it can't answer, and has Claude Code (or Codex) update the same line in Notion, so bots and the Claude and ChatGPT apps follow within a minute or two. Notion keeps the stored copy, and an edit made in Notion still shows in the bar once the local copy refreshes. It doesn't show usage limits.

The app is also a command, `guava-bar`: `guava-bar show`, `guava-bar picks line-cook`, `guava-bar pairs`, `guava-bar set line-cook "<a line from picks>"` (or both slots at once, as `pairs` prints) and `guava-bar refresh`.

## Before you start
These only read, so they need no yes:
- **A Mac** on macOS 14 or later: `sw_vers -productVersion`. Anywhere else, say guava-bar is Mac only and stop.
- **Claude Code, Codex or Pi** installed and signed in on this Mac, with Notion connected: `claude --version`, `codex --version`, `pi mcp list`. guava-bar uses Claude Code when it's there, then Codex, then Pi, so it works on OpenRouter alone. With none of them, say guava-bar needs one to change anything and stop. On Google AI alone it isn't supported yet: Antigravity CLI didn't load Notion's tools when run in the background, so say "change my setup" in Antigravity instead. In the Claude or ChatGPT app, it runs from their Code or Codex tab set to Local.
- **The Model Router** is on: guava-stack settings has `head-chef` and `line-cook` lines. Without them, say guava-bar has nothing to show until the router is on ("turn on the router"), and stop.
- **Xcode Command Line Tools**, which build the app: `xcode-select -p`. If it fails, step 1 of the plan is `xcode-select --install`, which opens Apple's installer: the owner clicks **Install**, waits a few minutes and says done.
- **The local hub copy**: `~/.guava-hub/sync.md`. Missing is fine: **Refresh from Notion** in the menu builds it.

## Install
1. **Build it.** From a local copy of guava-stack, or a fresh one: `tmp=$(mktemp -d) && git clone --depth 1 https://github.com/romeodiaz/guava-stack "$tmp/guava-stack" && sh "$tmp/guava-stack/guava-bar/build.sh"`. The script builds the app, tests it, puts `GuavaBar.app` in `~/Applications`, links the `guava-bar` command into `~/.local/bin` and opens the app. It changes nothing else.
2. **Check it:** `~/.local/bin/guava-bar show` prints the same head-chef and line-cook lines as guava-stack settings, and the head-chef and line-cook icons, with short model names such as `Opus` and `Sol`, are in the menu bar. No icon: the menu bar may be full, or hidden by a menu bar manager; quit an app or two and look again.
3. **Offer Open at login:** the owner clicks **Open at login** in guava-bar's menu, so it's always there. It shows in System Settings > General > Login Items.

Confirm in two lines: where the app is, what `guava-bar show` printed, and how to change a slot (click the icon, **Change line-cook**, pick a model and an effort, then **Change**).

## Update
Use this when the owner says **"update guava-bar"**, or when the guava-hub skill's Update step sends you here. Run **Install** step 1 with the newest files: it replaces the app in place. Then **Install** step 2, and check **Open at login** is still ticked if the owner had it on. Update again whenever guava-router's `models.yaml` changes, since the picks are built into the app.

## Uninstall
Use this when the owner says **"uninstall guava-bar"**, or when the guava-hub skill's Uninstall step sends you here.
1. The owner turns off **Open at login** in guava-bar's menu, if it's on.
2. `pkill -f 'GuavaBar.app/Contents/MacOS/guava-bar'`, then delete `~/Applications/GuavaBar.app`, `~/.guava-hub/guava-bar-tested.txt`, and `~/.local/bin/guava-bar` if it's a link to that app (`readlink ~/.local/bin/guava-bar`).
3. Nothing in Notion or `~/.guava-hub` needs undoing: guava-bar only changed what the owner picked, through **Change your setup**.

## What a change runs
Show this to the owner when they ask what guava-bar can do on their computer. A pick runs, in this order:
1. **Switch it on this Mac:** guava-bar rewrites that slot's model line, or both for **Switch both**, in `~/.guava-hub/context.md` and nothing else. New hand-offs on this Mac use it right away.
2. **Test the new model**, only the first time that model and effort are picked on this Mac (guava-bar remembers each one that passed in `~/.guava-hub/guava-bar-tested.txt`): guava-router's `router-check.py`, bundled in the app, sends it a one-word prompt with its own tool's command, such as `python3 router-check.py --plan claude-and-chatgpt --slot line-cook --line-cook gpt-6.1-sol:medium`. With both slots, each is tested. If one fails, guava-bar puts the old lines back and says why. A tool that's installed but not on one of the owner's plans fails here.
3. **Update Notion**, from `~/.guava-hub`, with no input, stopped after 10 minutes:
   - `claude -p "<the change>" --allowedTools mcp__claude_ai_Notion__notion-fetch mcp__claude_ai_Notion__notion-search mcp__claude_ai_Notion__notion-update-page` (the same three for a Notion connection named `notion`) `Read "WebFetch(domain:github.com)" "WebFetch(domain:raw.githubusercontent.com)"`: read and update Notion pages and read this repo's steps; no file edits and no commands.
   - With no Claude Code: `codex exec --skip-git-repo-check --sandbox workspace-write "<the change>"`, which can only write inside `~/.guava-hub`.
   - With neither, on OpenRouter alone: `pi -p "<the change>" --tools codemode,read,mcp__notion__notion_fetch,mcp__notion__notion_search,mcp__notion__notion_update_page`: Notion's fetch, search and update-page through Pi's codemode, and no other tool. Pi asks no questions, so this list is the whole limit. **Refresh from Notion** swaps `notion_update_page` for `write` and `edit`, which Pi doesn't confine to `~/.guava-hub`, so its prompt names the only two files it may change.
   - The tool must exit cleanly and end with `done: …`. Otherwise the menu says the Mac is switched but Notion isn't yet; picking the same model again retries.

The prompt names the slot and the old and new model lines, and says the owner chose this one change in guava-bar, which already switched the local copy and tested the model. It tells the session to set only that model line in Notion, marking it "(own pick)" if it isn't today's pick for the owner's plans, as **Change your setup** says, to leave `~/.guava-hub`, `~/.claude/settings.json` and `~/.codex/config.toml` alone (this is the owner's own computer, not a bot's), to skip the test and the task log, and to change nothing else. **Refresh from Notion** gets Notion's fetch and search, and edits only in `~/.guava-hub`. Its prompt carries the steps itself, since Pi can't read the web: fetch the context page into `context.md` and set the sync time in `sync.md`, creating both if they're missing, which builds a first hub copy for an owner who has none.

## If something fails
- **The bar shows an old model:** the local copy refreshes when an AI session runs, or when the owner clicks **Refresh from Notion**.
- **The test failed:** guava-bar switched back, and the menu shows why, usually a tool that needs updating or signing in (guava-router's **Repair**).
- **Notion wasn't updated:** this Mac already uses the new model. Pick the same model again to retry, or run `guava-bar set <slot> "<line>"` in Terminal to see why, or say "change my setup" in Claude or ChatGPT instead.
- **"guava-bar needs Claude Code, Codex or Pi":** install one as guava-router's step 2 says, sign in, connect Notion, and try again.
