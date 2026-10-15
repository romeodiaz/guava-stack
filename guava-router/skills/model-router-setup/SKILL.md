---
name: model-router-setup
description: Sets up a Model Router that sends thinking work to Claude Opus 5.5 through the Claude Code CLI and execution work to GPT-6.1 Sol through the Codex CLI, using the owner's own Claude and ChatGPT plans. Use when the owner asks for model routing or the CLIs, or when hub setup hands off to the router.
---

**Before every edit, install or setting change below, show the owner the exact command or change and wait for a yes.**

# Model Router: setup

These steps send each kind of work to the model that's best at it: hard thinking to Claude Opus 5.5 and heavy lifting to GPT-6.1 Sol, through the Claude and ChatGPT plans the owner already pays for.

> Setting up from scratch? Start with the **context-skills-hub-setup** skill from guava-hub. It builds the Notion hub first and sends you here at the right step. This skill works on its own too; skip step 2 if the owner has no AI Context Hub.

## 1. Install the command-line tools
- Check first, without asking (these only read): `claude --version` and `codex --version`. Skip the install for any tool that answers with a version, and tell the owner it's already there.
- Install only what's missing: Claude Code `npm i -g @anthropic-ai/claude-code`; Codex `npm i -g @openai/codex`.
- Check sign-in: `claude auth status` and `codex login status`. Skip any that's already signed in; otherwise sign in with the owner's own subscription: `claude auth login` and `codex login --device-auth`.
- Defaults: Claude `claude-opus-5-5` with effort high; Codex `gpt-6.1-sol` with `model_reasoning_effort` high.

## 2. Connect both to the hub
- Connect both to Notion. Run `claude mcp list` and `codex mcp list` first and skip any that already show Notion.
  - **Claude Code:** if the owner already connected Notion in the Claude app, Claude Code picks it up automatically. Otherwise run `claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp`, then have the owner type `/mcp` in Claude Code and approve Notion's sign-in page.
  - **Codex:** run `codex mcp add notion --url https://mcp.notion.com/mcp`, then `codex mcp login notion` and have the owner approve Notion's sign-in page.
  - Test each with a quick non-interactive run that searches Notion for "AI Context Hub", for example `claude -p "..." < /dev/null` and `codex exec --skip-git-repo-check "..." < /dev/null`. Add `< /dev/null` so neither waits for input.
- Add a short section to the end of `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` (create them if they don't exist) telling them to load your enabled Notion skills, Agent Rules and Profile & Context at the start of each session. Never replace or delete what's already in those files.

## 3. Never skip Notion (optional)
Only if the owner wants it. When nobody is at the keyboard, Claude skips tools that need approval, so your hub never loads. Fix it:
- Explain that this changes Claude Code's permission settings, show the exact lines you'll add, and get a yes.
- Back up `~/.claude/settings.json` first.
- Under `permissions.allow`, add the Notion read-only tools: `notion-get-enabled-skills`, `notion-fetch`, `notion-search`, `notion-download-skill`. Use the exact prefix shown by `claude mcp list` (for example `mcp__claude_ai_Notion__notion-fetch`).
- Do the same for Codex if needed.
- Never pre-approve write or delete tools.
- Test it with a non-interactive run and confirm your skills load.

## 4. Model routing
- **Claude Opus 5.5 (High)**: orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems.
- **GPT-6.1 Sol (High) via Codex**: bulk execution, coding, sub-agent tasks, worker threads, long-running jobs.
- **Browser and desktop tasks**: keep using the assistant's own computer tools.
- **If either CLI fails**: do the task yourself and say so.
- **Skills with their own setup come first**: when a skill defines how it runs (its own engine, scripts, models or setup), follow it as designed and use this routing only for work it leaves open. Never change a skill's own setup to fit the routing.

Save these routing rules as a standing instruction if hub setup hasn't already. If your platform has memory shared across all of the owner's assistants (on Grok Bot, shared user memory), save them there so every current and future bot follows them.

## 5. Stay inside Anthropic's terms
- Use the official Claude Code CLI with your own login only.
- Never share tokens or route other people's requests through your plan.
- Keep Claude work tied to tasks you start. No unattended loops or 24/7 jobs; send those to Codex.
- Stop when you hit usage limits.
- Never use outputs to train competing models.
- For heavy or always-on Claude automation, use an Anthropic API key, or do it by hand in Claude Desktop.

## 6. Final checks
- Check the current Anthropic and OpenAI terms.
- Test each CLI with a quick prompt and tell the owner which model actually answered in each. Don't call setup done until both pass.
- Running this as part of hub setup? Go back to the hub setup skill's guava-mode step.
