---
name: hub-setup
description: Sets up the owner's shared AI Context & Skills Hub in Notion and a Model Router that sends thinking work to Claude Code and execution work to Codex. Use when the owner says "set me up", asks for the AI Context Hub or model routing, or starts Guava setup.
---

> Running this as setup? First follow the **Start here** steps in the README at the root of this plugin, then come back here.

**Before every edit, install or setting change below, show the owner the exact command or change and wait for a yes.**

# AI Context & Skills Hub + Model Router: setup

These steps give Grok Bot, Claude and ChatGPT one shared place for your context, rules and skills, and send each kind of work to the model that's best at it.

## 1. Build the Notion hub
Create a page called **AI Context Hub** with:
- **Profile & Context**: answer a short interview about you and your business. No passwords, keys or other secrets.
- **Agent Rules**: never send, post or email without explicit approval; never store secrets; read-only by default on external accounts; keep a change log.
- **Skills**: a database for Notion's skill upload, including a model-routing skill. Ask the owner before enabling these skills for external agents and Notion AI.

## 2. Install the command-line tools
- Install Claude Code: `npm i -g @anthropic-ai/claude-code`
- Install Codex: `npm i -g @openai/codex`
- Sign in with your own subscriptions: `claude auth login` and `codex login --device-auth`
- Defaults: Claude `claude-opus-5-5` with effort high; Codex `gpt-6.1-sol` with `model_reasoning_effort` high.
- Connect both to Notion. Run `claude mcp list` and `codex mcp list` first and skip any that already show Notion.
  - **Claude Code:** if the owner already connected Notion in the Claude app, Claude Code picks it up automatically. Otherwise run `claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp`, then have the owner type `/mcp` in Claude Code and approve Notion's sign-in page.
  - **Codex:** run `codex mcp add notion --url https://mcp.notion.com/mcp`, then `codex mcp login notion` and have the owner approve Notion's sign-in page.
  - Test each with a quick non-interactive run that searches Notion for "AI Context Hub", for example `claude -p "..." < /dev/null` and `codex exec --skip-git-repo-check "..." < /dev/null`. Add `< /dev/null` so neither waits for input.
- Add a short section to the end of `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` (create them if they don't exist) telling them to load your enabled Notion skills, Agent Rules and Profile & Context at the start of each session. Never replace or delete what's already in those files.

## 2b. Never skip Notion (optional)
Only if the owner wants it. When nobody is at the keyboard, Claude skips tools that need approval, so your hub never loads. Fix it:
- Explain that this changes Claude Code's permission settings, show the exact lines you'll add, and get a yes.
- Back up `~/.claude/settings.json` first.
- Under `permissions.allow`, add the Notion read-only tools: `notion-get-enabled-skills`, `notion-fetch`, `notion-search`, `notion-download-skill`. Use the exact prefix shown by `claude mcp list` (for example `mcp__claude_ai_Notion__notion-fetch`).
- Do the same for Codex if needed.
- Never pre-approve write or delete tools.
- Test it with a non-interactive run and confirm your skills load.

## 2c. Bring in what they already have
Many owners already keep context and skills in other AI tools. Gather it into the hub so nothing is lost:
- Ask where it lives. Don't read Claude or ChatGPT memories, chat history, custom instructions or Projects yourself; ask the owner to paste or export what they want imported.
- For local files (`~/.claude/CLAUDE.md`, `~/.claude/skills/`, `~/.codex/AGENTS.md`, prompt or notes folders, other AI tools such as Cursor, Devin or Droid), first say exactly which paths you'll read, and read them only after a yes.
- Show a short list of what you found and where each piece would go (Profile & Context, Agent Rules or Skills). Import only what they approve.
- Before importing or installing any third-party skill, scan it with [Cisco Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner) and show the owner anything it flags. A clean scan doesn't prove a skill is safe.
- Merge duplicates and ask when two sources conflict. Leave out passwords, keys and other secrets.
- Copy, never move: leave the originals untouched. Only after they say yes, add a one-line pointer in the old place, such as "Load my Notion AI Context Hub first."

## 3. Model routing
- **Claude Opus 5.5 (High)**: orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems.
- **GPT-6.1 Sol (High) via Codex**: bulk execution, coding, sub-agent tasks, worker threads, long-running jobs.
- **Browser and desktop tasks**: keep using the assistant's own computer tools.
- **If either CLI fails**: do the task yourself and say so.
- **Skills with their own setup come first**: when a skill defines how it runs (its own engine, scripts, models or setup), follow it as designed and use this routing only for work it leaves open. Never change a skill's own setup to fit the routing.

## 3b. Stay inside Anthropic's terms
- Use the official Claude Code CLI with your own login only.
- Never share tokens or route other people's requests through your plan.
- Keep Claude work tied to tasks you start. No unattended loops or 24/7 jobs; send those to Codex.
- Stop when you hit usage limits.
- Never use outputs to train competing models.
- For heavy or always-on Claude automation, use an Anthropic API key, or do it by hand in Claude Desktop.

## 4. Standing instructions
Save a standing instruction for your assistant to load the hub before any real work. Save the model routing rules too. If your platform has memory shared across all of the owner's assistants (on Grok Bot, shared user memory), save both there so every current and future bot follows them.

## 5. Final checks
- Check the current Anthropic and OpenAI terms.
- Test each CLI with a quick prompt and tell the owner which model actually answered in each. Don't call setup done until both pass.
- Add the Notion connector in the Claude and ChatGPT apps, with a custom instruction: "Load my Notion AI Context Hub first."
