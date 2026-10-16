---
name: guava-router
description: Sets up a Model Router that sends thinking work to a planner model and doing work to a builder model through their command-line tools, or through instructions in the Claude and ChatGPT apps for owners without Grok Bot or Muse, on the owner's own plans. Supports Claude + ChatGPT (default), ChatGPT only and Claude only, with each setup's models in models.yaml. Also use when the owner says "check for newer models" or "update guava-router". Use when the owner asks for model routing or the CLIs, or when hub setup hands off to the router.
---

**Before every edit, install or setting change below, show the owner the exact command or change and wait for a yes.**

# Model Router: setup

These steps send each kind of work to the model that's best at it, through the plans the owner already pays for: thinking and reviewing to a **planner + reviewer**, and heavy lifting to a **builder**. Owners who want one do-it-all model don't need this skill.

> Setting up from scratch? Start with the **guava-hub** skill. It builds the hub first and sends you here at the right step. This skill works on its own too; skip step 3 if the owner has no AI Context Hub.

## 1. Pick the AI setup
If hub setup already saved one in the hub's Stack settings, use it. Otherwise ask which AI plans the owner pays for and offer these, with the default marked as recommended:

<!-- models:table first="They pay for" head="Planner + reviewer" line="Builder" -->
| They pay for | Planner + reviewer | Builder |
|---|---|---|
| **Claude + ChatGPT** (default) | Claude Opus 5.5 (High) via Claude Code | GPT-6.1 Sol (High) via Codex |
| ChatGPT only | GPT-6 Astra (High) via Codex | GPT-6.1 Sol (High) via Codex |
| Claude only | Claude Opus 5.5 (High) via Claude Code | Claude Sonnet 5.5 (High) via Claude Code |
| Local models on your own hardware (Ollama, LM Studio and others) | Coming soon | Coming soon |
<!-- /models -->

The picks for each setup come from [models.yaml](../../models.yaml), the one place they're kept; [setups.md](setups.md) has the model IDs, commands and notes for each. The owner can also pick their own planner or builder: any model a tool in their setup can run (Claude Code runs Claude models, Codex runs OpenAI models), marked "(own pick)" in Stack settings. If the owner asks about local models on their own hardware, say support is coming soon. For other tools or another provider's models, say they aren't supported. Either way, set up the closest of the three for now. Save the choice to Stack settings in Profile & Context if the owner has a hub.

Then pick how it routes, from the owner's day-to-day assistant:
- **CLI routing:** Grok Bot, Muse, or the Claude desktop app's Code tab. Follow steps 2 to 7. For the Code tab, also do the **App routing** step, so Claude and ChatGPT chat on the owner's phone route the same way when they're away from the computer.
- **App routing:** the owner works in Claude or ChatGPT chat (web, desktop or mobile) and doesn't have or want Grok Bot or Muse. Skip steps 2 to 4, follow the **App routing** step below, then steps 6 and 7.

## 2. Install the command-line tools
Only the tools the setup uses.
- Check first, without asking (these only read): `claude --version` and `codex --version`. Skip the install for any tool that answers with a version, and tell the owner it's already there.
- Install only what's missing: Claude Code `npm i -g @anthropic-ai/claude-code` (skip it in the Code tab, where it's built in); Codex `npm i -g @openai/codex`.
- Check sign-in: `claude auth status` and `codex login status`. Skip any that's already signed in; otherwise sign in with the owner's own subscription: `claude auth login` and `codex login --device-auth`.
- Set each slot's model and effort as [setups.md](setups.md) shows.
- **Claude desktop app's Code tab as the day-to-day assistant (Claude + ChatGPT setup):** also install OpenAI's official [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc), so Claude hands jobs to Codex natively. Use a local session. Run `claude plugin marketplace add openai/codex-plugin-cc` and `claude plugin install codex@openai-codex` as shell commands in the session (with a yes), or add the marketplace that way and install from **+ > Plugins > Add plugin**. Then start a new session and run `/codex:setup` to check it. It uses the Codex CLI and ChatGPT sign-in from above. Leave its review gate off (it stays off unless someone runs `/codex:setup --enable-review-gate`): it can loop and drain usage limits, and it's the kind of unattended Claude loop step 6 rules out.
- **Claude desktop app's Code tab in the Claude-only setup:** no extra install. Set the model to `opusplan` as [setups.md](setups.md) shows, so Opus plans in Plan mode and Sonnet builds after the owner approves the plan.
- **Code tab from the phone:** offer to turn on **Connect new sessions to Remote Control** in the desktop app's Settings, then Claude Code. The owner can then open any Code tab session from the Claude phone app (tap Code, then pick the session with the green dot) while the computer is on and the app is open. It needs a Pro or Max plan, or an admin turning it on for Team and Enterprise.
- **Code tab cloud sessions:** they reach the hub through the owner's connectors but have no Codex plugin or ChatGPT sign-in. There, follow the App routing hand-off instead: Claude plans, then gives a ready-to-paste prompt for a new chat with the builder.

## 3. Connect them to the hub
Check what's already connected first (`claude mcp list`, `codex mcp list`) and skip anything that already shows the hub.

- **Notion:**
  - Claude Code: if the owner already connected Notion in the Claude app, Claude Code picks it up automatically. Otherwise run `claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp`, then have the owner type `/mcp` in Claude Code and approve Notion's sign-in page.
  - Codex: run `codex mcp add notion --url https://mcp.notion.com/mcp`, then `codex mcp login notion` and have the owner approve Notion's sign-in page.
- **Google Drive or OneDrive/SharePoint:**
  - Claude Code picks up the Google Drive or Microsoft 365 connector from the Claude app when it's signed in with the same account. Check `claude mcp list` shows it.
  - Codex doesn't share the ChatGPT app's connectors. Add an official MCP server from Google or Microsoft if one exists for the tool; otherwise skip it and rely on the hand-off rule in step 5.
- **Local Markdown or Obsidian:** no connectors. Both tools read the folder directly; follow **Connect the apps** in the hub's [local-markdown.md](../../../guava-hub/skills/guava-hub/backends/local-markdown.md) if hub setup hasn't already (it adds the folder to Claude Code's `permissions.additionalDirectories` and the hub instruction line, with the folder's path, to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`).

Test each tool with a quick non-interactive run that reads the Agent Rules from the hub, for example `claude -p "..." < /dev/null` and `codex exec --skip-git-repo-check "..." < /dev/null`.

Then add a short section to the end of `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` telling it to load the enabled skills, Agent Rules and Profile & Context from the hub at the start of each session, and to follow the model routing in Stack settings. Create the files if they don't exist. Never replace or delete what's already in them. Skip `~/.claude/CLAUDE.md` when the guava-hub plugin is installed in Claude Code (including the Claude desktop app's Code tab): its start-up hook already tells every new session to load the hub and follow Stack settings. A local hub is the exception: keep its hub instruction line there, since only that line says where the folder is.

## 4. Never skip the hub (optional)
Only if the owner wants it. When nobody is at the keyboard, Claude Code skips tools that need approval, so the hub never loads. Fix it:
- Explain that this changes Claude Code's permission settings, show the exact lines you'll add, and get a yes.
- Back up `~/.claude/settings.json` first.
- Under `permissions.allow`, add only the hub's read-only tools, with the exact prefix `claude mcp list` shows:
  - Notion: `notion-get-enabled-skills`, `notion-fetch`, `notion-search`, `notion-download-skill` (for example `mcp__claude_ai_Notion__notion-fetch`).
  - Google Drive or Microsoft 365: the connector's search, fetch and read tools.
  - Local Markdown or Obsidian: nothing to add. The folder in `permissions.additionalDirectories` is already readable without asking.
- Do the same for Codex if needed.
- Never pre-approve write or delete tools.
- Test it with a non-interactive run and confirm the skills load.

## 5. Model routing
- **Planner + reviewer**: orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems. For important work, it also checks the builder's result before anything is called done.
- **Builder**: bulk execution, coding, sub-agent tasks, worker threads, long-running jobs.
- **Browser and desktop tasks**: keep using the assistant's own computer tools.
- **Hand-off rule**: if a tool can't reach the hub, the planner (or you) loads what the job needs from the hub and puts it in that tool's prompt.
- **If either fails**: do the task yourself and say so.
- **If you are the planner or the builder** (say, Claude Code in a Claude setup), do that slot's work yourself and send only the other slot's work out.
- **Code tab with the Codex plugin:** hand builder jobs to the `codex:codex-rescue` subagent with the builder's model and effort from Stack settings (the owner can also type `/codex:rescue --model <builder model ID> --effort <its effort> ...`). Run long jobs in the background and check them with `/codex:status` and `/codex:result`. For a second opinion on important work, use `/codex:adversarial-review`.
- **Skills with their own setup come first**: when a skill defines how it runs (its own engine, scripts, models or setup), follow it as designed and use this routing only for work it leaves open. Never change a skill's own setup to fit the routing.

Save these routing rules as a standing instruction if hub setup hasn't already. With a hub, point it at the Planner and Builder in Stack settings instead of naming models, so the owner can swap a model by editing Stack settings; without one, name the models. If your platform has memory shared across all of the owner's assistants (on Grok Bot, shared user memory), save them there so every current and future bot follows them.

## App routing (no CLIs)
An app can't hand work to another model by itself, so the app's instructions do the routing before any work starts: every new chat sizes up the first request, and if it belongs on the other model, the app names that model and gives a ready-to-paste prompt instead of starting.

1. Map the planner and builder to apps, using the **In the apps** line for the owner's setup in [setups.md](setups.md). In each app, pick the highest thinking or effort option it offers.
2. Show the owner the instruction below. With a hub, use the first line as written, so it reads the models from Stack settings and a swap there needs no new paste; without a hub, replace it with the models' names. It names models only, never apps: the owner knows where each model lives, so the same text works in every app. Walk them through adding a copy to each app they use (each copy can then be tweaked on its own), under the hub instruction line, in the same place the hub setup used (Claude: Settings, then Account, then Instructions for Claude; ChatGPT: [Personalization](https://chatgpt.com/settings/personalization), then Custom Instructions). Add to what's there; never replace it. Send one small step per message and wait for done. These instructions follow the owner's account onto the desktop and phone apps; check them on the phone too.
   ```
   Model routing: plan with the Planner in my Stack settings and execute with the Builder. Read them from my AI Context Hub at the start of each chat; if you can't, ask me which model to use.
   Planning is research, planning, brainstorming, writing, review, checking work and hard problems. Execution is drafting at volume, coding, data work, and bulk or long jobs.
   Route first. At the start of every new chat, before doing anything else, decide whether my request is planning or execution.
   - Right model, or a quick question: go ahead.
   - Wrong model: don't start. Reply with one line naming the model to use, then my request rewritten as a ready-to-paste prompt for a new chat on it, with the hub skills it should load.
   - If I say "stay here", do it on this model.
   When a plan is ready, end with a hand-off I can paste into a new chat with the builder: the goal, the steps, what done looks like, and which hub skills to load.
   For important work, remind me to bring the result back to the planner for a check.
   ```
   Without a hub, with the default setup, the first line reads: "<!-- models:app-routing-example -->Model routing: plan with Claude Opus 5.5. Execute with GPT-6.1 Sol.<!-- /models -->"
3. Test it in a new chat on the planner: ask for something to execute. It passes if the app doesn't start, names the builder, and gives a ready-to-paste prompt. Then, in another new chat, ask for something to plan. It passes if it does the work and ends with a hand-off. If the builder is in a different app, check that app routes planning requests back the same way.
4. Save the routing to Stack settings, noting which app holds each model.

## 6. Stay inside each provider's terms
For Claude Code on a Claude plan:
- Use the official Claude Code CLI with your own login only.
- Never share tokens or route other people's requests through your plan.
- Keep Claude work tied to tasks you start. No unattended loops or 24/7 jobs on the plan; send those to a non-Claude builder, or in the Claude-only setup use an Anthropic API key or do them by hand.
- Stop when you hit usage limits.
- Never use outputs to train competing models.
- For heavy or always-on Claude automation, use an Anthropic API key, or do it by hand in Claude Desktop.

For Codex and every other tool, follow that provider's current terms for its plan.

## 7. Final checks
- Check the current terms for each provider in the setup.
- CLI routing: test each slot with a quick prompt and tell the owner which model actually answered. App routing: the App routing test above. Don't call setup done until both slots pass.
- Running this as part of hub setup? Go back to the hub setup skill's founder-mode step.

## Changing the setup later
To swap models, switch between one and two models, or apply a hand-edited Stack settings section, follow **Change your setup** in the guava-hub skill. "Check for newer models" goes there too.

Without a hub, do the same by hand: compare the planner and builder with [models.yaml](../../models.yaml), show each change as old, then new, and on a yes update the routing section in `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` and the routing instruction in each app. Then test each changed slot as in step 7.

## Update
Use this when the owner says **"update guava-router"**, or when the guava-hub skill's Update step sends you here. Show the whole plan first as one numbered list (each command, and each change as old, then new); the owner can approve it with one yes or pick numbers. Then apply it in order.

1. **Get the newest files** (skip this when the guava-hub Update step already did it):
<!-- update-steps: keep this list the same in the guava-hub, guava-router and founder-mode skills -->
Only for the Guava plugins the owner has (for "update guava-router", just guava-router):
- **Claude Code or the Claude desktop app's Code tab:** `claude plugin marketplace update guava`, then `claude plugin update <plugin>@guava` for each plugin. Updates apply in a new session. A Code tab **cloud** session can't update plugins: say so, and ask the owner to say the same thing in a Local session.
- **Codex:** `codex plugin marketplace upgrade guava`, then `codex plugin add <plugin>@guava` for each plugin. If the skills were installed with Codex's skill installer instead, install them again from github.com/romeodiaz/guava-stack, replacing the old folders. Updates apply in a new chat.
- **Claude chat (web, desktop and phone):** replace each uploaded Guava skill with the new copy from `<plugin>/skills/<plugin>/` in the repo.
- **ChatGPT and ChatGPT Dots:** rebuild the plugin with Plugin Creator from the skill folders, since a published plugin is a snapshot.
- **Grok Bot, and any assistant that keeps the skills as files:** replace them with the newest copies from the repo.
- **Muse:** no skill files, so nothing to download.
- **Older copies:** look for Guava pieces under their old names: the `guava-mode` plugin (`claude plugin list`) and skill folders named `owner-mode-rules`, `founder-mode-rules`, `context-skills-hub-setup`, `context-skills-hub-model-router-setup` or `model-router-setup` in `~/.claude/skills`, `~/.agents/skills` and `~/.codex/skills`. They run old instructions next to the new ones. Offer to uninstall the old plugin (`claude plugin uninstall guava-mode@guava`) and move the old folders into a dated backup folder. Never delete them.
<!-- /update-steps -->
2. **Check for newer models:** follow **Change your setup** in the guava-hub skill with "check for newer models". Without a hub, follow the by-hand steps under **Changing the setup later** above.
3. **Check the routing still runs:** each tool in Stack settings is installed and signed in (step 2 of setup, checking first). In the Code tab with Claude + ChatGPT, the Codex plugin is installed and `/codex:setup` reports ready with the review gate off. Routing instructions that still name models or old paths get the replacement offer from step 2 of the guava-hub Update step.
4. **Test** each slot with a quick prompt, as in step 7, and confirm in two or three lines: guava-router's version before and after, any model change, and anything left for the owner.
