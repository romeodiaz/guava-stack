---
name: model-router-setup
description: Sets up a Model Router that sends thinking work to a planner model and doing work to a worker model through their command-line tools, on the owner's own plans. Defaults to Claude Opus 5.5 (Claude Code) as planner and GPT-6.1 Sol (Codex) as worker, and also supports ChatGPT only, Claude only, and other tools like Cursor, Devin, Droid and Amp. Use when the owner asks for model routing or the CLIs, or when hub setup hands off to the router.
---

**Before every edit, install or setting change below, show the owner the exact command or change and wait for a yes.**

# Model Router: setup

These steps send each kind of work to the model that's best at it, through the plans the owner already pays for: thinking work to a **planner** and heavy lifting to a **worker**.

> Setting up from scratch? Start with the **context-skills-hub-setup** skill from guava-hub. It builds the hub first and sends you here at the right step. This skill works on its own too; skip step 3 if the owner has no AI Context Hub.

## 1. Pick the AI setup
If hub setup already saved one in the hub's Stack settings, use it. Otherwise ask which AI plans the owner pays for and offer these, with the default marked as recommended:

| They pay for | Planner | Worker |
|---|---|---|
| **Claude + ChatGPT** (default) | Claude Opus 5.5 (High) via Claude Code | GPT-6.1 Sol (High) via Codex |
| ChatGPT only | Astra (High) via Codex | GPT-6.1 Sol (High) via Codex |
| Claude only | Claude Opus 5.5 (High) via Claude Code | Claude Sonnet 5.5 (High) via Claude Code |
| Other tools or a custom mix (Cursor, Devin, Droid, Amp and others) | The owner's pick | The owner's pick |

[setups.md](setups.md) has the model IDs, commands and notes for each. Save the choice to Stack settings in Profile & Context if the owner has a hub.

## 2. Install the command-line tools
Only the tools the setup uses.
- Check first, without asking (these only read): `claude --version`, `codex --version`, or the other tool's version command. Skip the install for any tool that answers with a version, and tell the owner it's already there.
- Install only what's missing: Claude Code `npm i -g @anthropic-ai/claude-code`; Codex `npm i -g @openai/codex`; other tools as their docs say.
- Check sign-in: `claude auth status` and `codex login status`. Skip any that's already signed in; otherwise sign in with the owner's own subscription: `claude auth login` and `codex login --device-auth`.
- Set each slot's model and effort as [setups.md](setups.md) shows.

## 3. Connect them to the hub
Check what's already connected first (`claude mcp list`, `codex mcp list`) and skip anything that already shows the hub.

- **Notion:**
  - Claude Code: if the owner already connected Notion in the Claude app, Claude Code picks it up automatically. Otherwise run `claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp`, then have the owner type `/mcp` in Claude Code and approve Notion's sign-in page.
  - Codex: run `codex mcp add notion --url https://mcp.notion.com/mcp`, then `codex mcp login notion` and have the owner approve Notion's sign-in page.
- **Google Drive or OneDrive/SharePoint:**
  - Claude Code picks up the Google Drive or Microsoft 365 connector from the Claude app when it's signed in with the same account. Check `claude mcp list` shows it.
  - Codex and other tools don't share the ChatGPT app's connectors. Add an official MCP server from Google or Microsoft if one exists for the tool; otherwise skip it and rely on the hand-off rule in step 5.
- **Obsidian or local Markdown:** nothing to connect. Put the hub folder's full path in the instructions below; for non-interactive Claude runs, see step 4.

Test each tool with a quick non-interactive run that reads the Agent Rules from the hub, for example `claude -p "..." < /dev/null` and `codex exec --skip-git-repo-check "..." < /dev/null`.

Then add a short section to the end of `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` (or the other tool's instructions file) telling it to load the enabled skills, Agent Rules and Profile & Context from the hub at the start of each session. Create the files if they don't exist. Never replace or delete what's already in them.

## 4. Never skip the hub (optional)
Only if the owner wants it. When nobody is at the keyboard, Claude Code skips tools that need approval, so the hub never loads. Fix it:
- Explain that this changes Claude Code's permission settings, show the exact lines you'll add, and get a yes.
- Back up `~/.claude/settings.json` first.
- Under `permissions.allow`, add only the hub's read-only tools, with the exact prefix `claude mcp list` shows:
  - Notion: `notion-get-enabled-skills`, `notion-fetch`, `notion-search`, `notion-download-skill` (for example `mcp__claude_ai_Notion__notion-fetch`).
  - Google Drive or Microsoft 365: the connector's search, fetch and read tools.
  - Local Markdown: add the hub folder to `permissions.additionalDirectories` and allow `Read(<hub folder>/**)`.
- Do the same for Codex or other tools if needed.
- Never pre-approve write or delete tools.
- Test it with a non-interactive run and confirm the skills load.

## 5. Model routing
- **Planner**: orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems.
- **Worker**: bulk execution, coding, sub-agent tasks, worker threads, long-running jobs.
- **Browser and desktop tasks**: keep using the assistant's own computer tools.
- **Hand-off rule**: if a tool can't reach the hub, the planner (or you) loads what the job needs from the hub and puts it in that tool's prompt.
- **If either fails**: do the task yourself and say so.
- **If you are the planner or the worker** (say, Claude Code in a Claude setup), do that slot's work yourself and send only the other slot's work out.
- **Skills with their own setup come first**: when a skill defines how it runs (its own engine, scripts, models or setup), follow it as designed and use this routing only for work it leaves open. Never change a skill's own setup to fit the routing.

Save these routing rules as a standing instruction, with the owner's planner and worker named, if hub setup hasn't already. If your platform has memory shared across all of the owner's assistants (on Grok Bot, shared user memory), save them there so every current and future bot follows them.

## 6. Stay inside each provider's terms
For Claude Code on a Claude plan:
- Use the official Claude Code CLI with your own login only.
- Never share tokens or route other people's requests through your plan.
- Keep Claude work tied to tasks you start. No unattended loops or 24/7 jobs on the plan; send those to a non-Claude worker, or in the Claude-only setup use an Anthropic API key or do them by hand.
- Stop when you hit usage limits.
- Never use outputs to train competing models.
- For heavy or always-on Claude automation, use an Anthropic API key, or do it by hand in Claude Desktop.

For Codex and every other tool, follow that provider's current terms for its plan.

## 7. Final checks
- Check the current terms for each provider in the setup.
- Test each slot with a quick prompt and tell the owner which model actually answered. Don't call setup done until both pass.
- Running this as part of hub setup? Go back to the hub setup skill's founder-mode step.
