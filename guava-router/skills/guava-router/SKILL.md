---
name: guava-router
description: Sets up a Model Router that sends thinking work to a head-chef model and doing work to a line-cook model through their command-line tools, or through instructions in the Claude and ChatGPT apps for owners without Grok Bot or Muse, on the owner's own plans. Supports Claude + ChatGPT (default), ChatGPT only and Claude only, with each setup's models in models.yaml. Also use when the owner says "check for newer models", "update guava-router" or "uninstall guava-router". Use when the owner asks for model routing or the CLIs, or when hub setup hands off to the router.
---

**Before every edit, install or setting change below, show the owner the exact command or change and wait for a yes.** Put it in your message text before you ask, never only inside a question or approval card, since some apps don't show what's in the card. Never ask for a yes to a change the owner hasn't seen.

# Model Router: setup

These steps send each kind of work to the model that's best at it, through the plans the owner already pays for: thinking and reviewing to a **head-chef**, and heavy lifting to a **line-cook**. Owners who want one model for everything put it in both slots.

> Setting up from scratch? Start with the **guava-hub** skill. It builds the hub first and sends you here at the right step. This skill works on its own too; skip step 3 if the owner has no guava-hub.

## 1. Pick the AI setup
If hub setup already saved one in the hub's guava-stack settings, use it. Otherwise ask which AI plans the owner pays for and offer these, with the default marked as recommended:

<!-- models:table first="They pay for" head="head-chef" line="line-cook" -->
| They pay for | head-chef | line-cook |
|---|---|---|
| **Claude + ChatGPT** (default) | Claude Opus 5.5 (High) via Claude Code | GPT-6.1 Sol (High) via Codex |
| ChatGPT only | GPT-6 Astra (High) via Codex | GPT-6.1 Sol (High) via Codex |
| Claude only | Claude Opus 5.5 (High) via Claude Code | Claude Sonnet 5.5 (High) via Claude Code |
| Local models on your own hardware (Ollama, LM Studio and others) | *Coming soon* | *Coming soon* |
<!-- /models -->

The picks for each setup come from [models.yaml](https://github.com/romeodiaz/guava-stack/blob/main/guava-router/models.yaml), the one place they're kept; [setups.md](setups.md) has the model IDs, commands and notes for each. The owner can also pick their own head-chef or line-cook: any model a tool in their setup can run (Claude Code runs Claude models, Codex runs OpenAI models), marked "(own pick)" in guava-stack settings. If the owner asks about local models on their own hardware, say support is coming soon. For other tools or another provider's models, say they aren't supported. Either way, set up the closest of the three for now. Save the choice to guava-stack settings on the context page if the owner has a hub.

**Same model in both slots:** install and sign in only that model's tool in step 2. Each slot keeps its own effort, so the same model can plan on High and build on Medium: line-cook jobs still go out through that tool at the line-cook's effort (for example `claude -p --model <id> --effort medium`). Only when the model and the effort both match is there nothing to route: then skip the hand-offs in step 5 and the App routing instruction (the hub instruction line is enough).

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
- **Claude desktop app's Code tab in the Claude-only setup:** no extra install. Set the model to the head-chef, and hand line-cook jobs to a subagent on the line-cook's model and effort from guava-stack settings (Claude Code's subagents take both).
- **Code tab from the phone:** offer to turn on Remote Control for every new session: back up `~/.claude/settings.json` (see **Backups** below), then set `"remoteControlAtStartup": true` in it (or the owner turns on **Connect new sessions to Remote Control** in the desktop app's Settings, then Claude Code). The owner can then open any Code tab session from the Claude phone app (tap Code, then pick the session with the green dot) while the computer is on and the app is open. It needs a Pro or Max plan, or an admin turning it on for Team and Enterprise.
- **Local only:** Guava runs the Code tab and Codex on the owner's computer. Cloud sessions in the Code tab and Codex cloud tasks aren't supported, since they don't load the plugins or the owner's sign-ins. Tell the owner to pick **Local** when they start a Code tab session (the app has no setting to make it the default), and to use the Codex app or CLI on their computer. If you're running in a cloud session, say so in one line and ask the owner to start a Local one.

## 3. Connect them to the hub
Check what's already connected first (`claude mcp list`, `codex mcp list`) and skip anything that already shows the hub.

- **Notion:**
  - Claude Code: if the owner already connected Notion in the Claude app, Claude Code picks it up automatically. Otherwise run `claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp`, then have the owner type `/mcp` in Claude Code and approve Notion's sign-in page.
  - Codex: run `codex mcp add notion --url https://mcp.notion.com/mcp`, then `codex mcp login notion` and have the owner approve Notion's sign-in page.
- **Google Drive or OneDrive/SharePoint:**
  - Claude Code picks up the Google Drive or Microsoft 365 connector from the Claude app when it's signed in with the same account. Check `claude mcp list` shows it.
  - Codex doesn't share the ChatGPT app's connectors. Add an official MCP server from Google or Microsoft if one exists for the tool; otherwise skip it and rely on the hand-off rule in step 5.
- **Local Markdown or Obsidian:** no connectors. Both tools read the folder directly; follow **Connect the apps** in the hub's [local-markdown.md](https://github.com/romeodiaz/guava-stack/blob/main/guava-hub/skills/guava-hub/backends/local-markdown.md) if hub setup hasn't already (it adds the folder to Claude Code's `permissions.additionalDirectories` and the hub instruction line, with the folder's path, to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`).

Test each tool with a quick non-interactive run that reads the context page from the hub, for example `claude -p "..." < /dev/null` and `codex exec --skip-git-repo-check "..." < /dev/null`.

Then add a short Guava block to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` telling each tool to load the enabled skills, the rules page and the context page from the hub at the start of each session, and to follow the model routing in guava-stack settings, following the rule below. Skip each file when the guava-hub plugin is installed in that tool (Claude Code, including the Claude desktop app's Code tab, or Codex): its start-up hook already tells every new session to load the hub and follow guava-stack settings. A local hub is the exception: keep its hub instruction line there, since only that line says where the folder is.

<!-- guava-block: keep this paragraph the same in the guava-hub and guava-router skills -->
**Local instruction files** (`~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, when they need Guava lines): keep everything Guava adds in one block between `<!-- guava-stack:start -->` and `<!-- guava-stack:end -->`. Back the file up first, as **Backups** below says, and create it if it doesn't exist. Replace only what's between the markers, or add the block at the end of the file if there are none yet. Never change anything else in the file. Show the owner the change to every file together and ask once.

**Backups:** whenever a step says to back up a file, copy it to `<file>.bak-<local date and time>`, such as `settings.json.bak-2026-10-15-2122`. The first time Guava changes a file, also copy it to `<file>.pre-guava`, or create that copy empty if the file doesn't exist yet, and never overwrite it: uninstalling puts the file back from it. Entries the plugin commands wrote before it, such as `enabledPlugins`, can already be in it; the uninstall commands remove those themselves.
<!-- /guava-block -->

## 4. Never skip the hub (optional)
Only if the owner wants it. When nobody is at the keyboard, Claude Code skips tools that need approval, so the hub never loads. Fix it:
- Explain that this changes Claude Code's permission settings, show the exact lines you'll add, and get a yes.
- Back up `~/.claude/settings.json` first (see **Backups** above).
- Under `permissions.allow`, add only the hub's read-only tools, with the exact prefix `claude mcp list` shows:
  - Notion: `notion-get-enabled-skills`, `notion-fetch`, `notion-search`, `notion-download-skill` (for example `mcp__claude_ai_Notion__notion-fetch`).
  - Google Drive or Microsoft 365: the connector's search, fetch and read tools.
  - Local Markdown or Obsidian: nothing to add. The folder in `permissions.additionalDirectories` is already readable without asking.
- Do the same for Codex if needed.
- Never pre-approve write or delete tools.
- Test it with a non-interactive run and confirm the skills load.

## 5. Model routing
- **head-chef**: orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems. For important work, it also checks the line-cook's result before anything is called done.
- **line-cook**: bulk execution, coding, sub-agent tasks, worker threads, long-running jobs.
- **Browser and desktop tasks**: keep using the assistant's own computer tools.
- **Hand-off rule**: if a tool can't reach the hub, the head-chef (or you) loads what the job needs from the hub and puts it in that tool's prompt.
- **If either fails**: do the task yourself and say so.
- **If you are the head-chef or the line-cook** (say, Claude Code in a Claude setup), do that slot's work yourself and send only the other slot's work out.
- **Code tab or Claude Code with a Claude line-cook:** hand line-cook jobs to a subagent on the line-cook's model and effort from guava-stack settings (Claude Code's subagents take both), like any other hand-off.
- **Code tab with the Codex plugin:** hand line-cook jobs to the `codex:codex-rescue` subagent with the line-cook's model and effort from guava-stack settings (the owner can also type `/codex:rescue --model <line-cook model ID> --effort <its effort> ...`). Run long jobs in the background and check them with `/codex:status` and `/codex:result`. For a second opinion on important work, use `/codex:adversarial-review`.
- **Skills with their own setup come first**: when a skill defines how it runs (its own engine, scripts, models or setup), follow it as designed and use this routing only for work it leaves open. Never change a skill's own setup to fit the routing.

Save these routing rules as a standing instruction if hub setup hasn't already. With a hub, point it at the head-chef and line-cook in guava-stack settings instead of naming models, so the owner can swap a model by editing guava-stack settings; without one, name the models. If your platform has memory shared across all of the owner's assistants (on Grok Bot, shared user memory), save them there so every current and future bot follows them.

## App routing (no CLIs)
An app can't hand work to another model by itself, so the app's instructions do the routing before any work starts: every new chat sizes up the first request, and if it belongs on the other model, the app names that model and gives a ready-to-paste prompt instead of starting.

1. Map the head-chef and line-cook to apps, using the **In the apps** line for the owner's setup in [setups.md](setups.md). In each app, pick the highest thinking or effort option it offers.
2. Show the owner the instruction below. With a hub, use the first line as written, so it reads the models from guava-stack settings and a swap there needs no new paste; without a hub, replace it with the models' names. It names models only, never apps: the owner knows where each model lives, so the same text works in every app. Walk them through adding a copy to each app they use (each copy can then be tweaked on its own), under the hub instruction line, in the same place the hub setup used (Claude: Settings, then Account, then Instructions for Claude; ChatGPT: [Personalization](https://chatgpt.com/settings/personalization), then Custom Instructions). Add to what's there; never replace it. Send one small step per message and wait for done. These instructions follow the owner's account onto the desktop and phone apps; check them on the phone too.
   ```
   Model routing: plan with the head-chef in my guava-stack settings and hand the doing to the line-cook. Read them from my guava-hub at the start of each chat; if you can't, ask me which model to use.
   head-chef work is research, planning, brainstorming, writing, review, checking work and hard problems. line-cook work is drafting at volume, coding, data work, and bulk or long jobs.
   Route first. At the start of every new chat, before doing anything else, decide whether my request is head-chef work or line-cook work.
   - Right model, or a quick question: go ahead.
   - Wrong model or effort: don't start. Reply with one line naming the model and effort to use, then my request rewritten as a ready-to-paste prompt for a new chat on it, with the hub skills it should load.
   - If I say "stay here", do it on this model.
   When a plan is ready, end with a hand-off I can paste into a new chat with the line-cook: the goal, the steps, what done looks like, and which hub skills to load.
   For important work, remind me to bring the result back to the head-chef for a check.
   ```
   Without a hub, with the default setup, the first line reads: "<!-- models:app-routing-example -->Model routing: plan with Claude Opus 5.5. Execute with GPT-6.1 Sol.<!-- /models -->"
3. Test it in a new chat on the head-chef: ask for something to execute. It passes if the app doesn't start, names the line-cook, and gives a ready-to-paste prompt. Then, in another new chat, ask for something to plan. It passes if it does the work and ends with a hand-off. If the line-cook is in a different app, check that app routes planning requests back the same way.
4. Save the routing to guava-stack settings, noting which app holds each model.

## 6. Stay inside each provider's terms
For Claude Code on a Claude plan:
- Use the official Claude Code CLI with your own login only.
- Never share tokens or route other people's requests through your plan.
- Keep Claude work tied to tasks you start. No unattended loops or 24/7 jobs on the plan; send those to a non-Claude line-cook, or in the Claude-only setup use an Anthropic API key or do them by hand.
- Stop when you hit usage limits.
- Never use outputs to train competing models.
- For heavy or always-on Claude automation, use an Anthropic API key, or do it by hand in Claude Desktop.

For Codex and every other tool, follow that provider's current terms for its plan.

## 7. Final checks
- Check the current terms for each provider in the setup.
- CLI routing: test each slot with a quick prompt and tell the owner which model actually answered. App routing: the App routing test above. Don't call setup done until both slots pass.
- Running this as part of hub setup? Go back to the hub setup skill's founder-mode step.

## Changing the setup later
To swap models, use one model in both slots, or apply a hand-edited guava-stack settings section, follow **Change your setup** in the guava-hub skill. "Check for newer models" goes there too.

Without a hub, do the same by hand: compare the head-chef and line-cook with [models.yaml](https://github.com/romeodiaz/guava-stack/blob/main/guava-router/models.yaml), show each change as old, then new, and on a yes update the routing lines in the Guava block of `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` and the routing instruction in each app. Then test each changed slot as in step 7.

## Update
Use this when the owner says **"update guava-router"**, or when the guava-hub skill's Update step sends you here. Show the whole plan first, in your message text, as one numbered list (each command, and each change as old, then new); the owner can approve it with one yes or pick numbers. Then apply it in order.

1. **Get the newest files** (skip this when the guava-hub Update step already did it):
<!-- update-steps: keep this list the same in the guava-hub, guava-router and founder-mode skills -->
Only for the Guava plugins the owner has (for "update guava-router", just guava-router):
- **Claude Code or the Claude desktop app's Code tab:** `claude plugin marketplace update guava`, then `claude plugin update <plugin>@guava` for each plugin. Updates apply in a new session.
- **Codex:** `codex plugin marketplace upgrade guava`, then `codex plugin add <plugin>@guava` for each plugin. Updates apply in a new chat.
- **Claude chat (web, desktop and phone):** replace each uploaded Guava skill with the new copy from `<plugin>/skills/<plugin>/` in the repo.
- **ChatGPT and ChatGPT Dots:** rebuild the plugin with Plugin Creator from the skill folders, since a published plugin is a snapshot.
- **Grok Bot, and any other assistant that keeps the skills as files:** `npx skills update -g -y`.
- **Muse:** no skill files, so nothing to download.
<!-- /update-steps -->
2. **Check for newer models:** follow **Change your setup** in the guava-hub skill with "check for newer models". Without a hub, follow the by-hand steps under **Changing the setup later** above.
3. **Check the routing still runs:** each tool in guava-stack settings is installed and signed in (step 2 of setup, checking first). In the Code tab with Claude + ChatGPT, the Codex plugin is installed and `/codex:setup` reports ready with the review gate off.
4. **Test** each slot with a quick prompt, as in step 7, and confirm in two or three lines: guava-router's version before and after, any model change, and anything left for the owner.

## Uninstall
Use this when the owner says **"uninstall guava-router"**, or when the guava-hub skill's Uninstall step sends you here. It stops the routing and puts back what router setup changed. Show the whole plan first, in your message text, as one numbered list (each command, each file change as old, then new, and each app step); the owner can approve it with one yes or pick numbers. Then apply it in order.

<!-- guava-restore: keep this paragraph the same in the guava-hub and guava-router skills -->
**Putting files back** (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, `~/.claude/settings.json` and `~/.codex/config.toml`): `<file>.pre-guava` next to each file shows how it was before Guava (see **Backups** in setup step 1 of the guava-hub skill). In the instruction files, remove only the lines you're taking off from the block between `<!-- guava-stack:start -->` and `<!-- guava-stack:end -->`; once the block is empty, remove it with its markers. If the file is then empty, put back what its `.pre-guava` copy holds, or delete the file when that copy is empty. Run the plugin commands first, since they rewrite these files and remove their own entries. Then, for only the settings the Uninstall step lists, put each one back to its value in the `.pre-guava` copy, or remove it if that copy doesn't have it; if the owner has changed it since Guava set it, ask instead. Drop any section left empty that the copy doesn't have, such as an empty `enabledPlugins`. Never copy a backup over the file, since that would undo every change the owner made since, and never change anything else. With no `.pre-guava` copy, remove only what Guava added and ask about any value it may have replaced. Leave the `.pre-guava` and `.bak-` copies where they are and list them in the wrap-up, so the owner can delete them once they're happy.
<!-- /guava-restore -->

1. **Remove the plugin** (skip this when the guava-hub Uninstall step already did it). When uninstalling guava-router on its own, first check what's there without asking, as step 1 of the guava-hub Uninstall step says:
<!-- uninstall-steps: keep this list the same in the guava-hub, guava-router and founder-mode skills -->
Only for the Guava plugins the owner has (for "uninstall guava-router", just guava-router; for "uninstall guava-stack", every one installed):
- **Claude Code or the Claude desktop app's Code tab:** `claude plugin uninstall <plugin>@guava` for each plugin. Once no Guava plugin is left, `claude plugin marketplace remove guava`, then delete `~/.claude/plugins/cache/guava` if it's still there (if your safety check won't let you delete a folder in these steps, move it into `~/guava-uninstalled/` instead and list it in the wrap-up). It applies in a new session.
- **Codex:** `codex plugin remove <plugin>@guava` for each plugin. Once no Guava plugin is left, `codex plugin marketplace remove guava`, then delete `~/.codex/plugins/cache/guava` if it's still there, and each `~/.codex/.tmp/marketplaces/.staging/marketplace-upgrade-*` folder holding a copy of guava-stack, which marketplace upgrades leave behind. It applies in a new chat.
- **Claude chat (web, desktop and phone):** ask the owner whether they uploaded the Guava skills there, and if so, have them delete each one.
- **ChatGPT and ChatGPT Dots:** delete the Guava plugin made with Plugin Creator, or rebuild it without the skills being removed.
- **Grok Bot, and any other assistant that keeps the skills as files:** `npx skills remove -g -s <plugin> -y` for each skill, and check with `npx skills list -g`.
- **Muse:** no skill files, so nothing to delete.
<!-- /uninstall-steps -->
2. **Put the computer back**, following **Putting files back** above:
   - `~/.claude/settings.json`: `remoteControlAtStartup` and `model`, which is also the Code tab's model setting. Say which model new sessions will use instead. The hub's read-only tools under `permissions.allow` stay while the hub does: guava-hub's Uninstall step removes them.
   - `~/.codex/config.toml`: `model`, saying which model new chats will use instead.
   - The Guava blocks in `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`: the routing line.
   - The Codex plugin for Claude Code, if router setup installed it: `claude plugin list` shows `codex@openai-codex` and `~/.claude/settings.json.pre-guava` doesn't list it under `enabledPlugins` (if there's no such copy, ask): `claude plugin uninstall codex@openai-codex`, then `claude plugin marketplace remove openai-codex`, then delete `~/.claude/plugins/cache/openai-codex` if it's still there.
3. **Take routing out of the apps:** wherever setup added them, remove the app routing instruction from Claude's Instructions for Claude and ChatGPT's Custom Instructions (both the ChatGPT box and the Codex box), the routing preference from ChatGPT Dots, the routing line from Muse's SOUL.md and the routing memories from Grok Bot, shared user memory included. Show the exact text to delete, one app per message, and wait for done.
4. **Turn routing off in the hub** (skip this when uninstalling the whole stack, since the hub then stays as it is): in guava-stack settings, remove the AI setup line and the head-chef and line-cook heading, with its two lines, their sub-bullets and, in Notion, its images. With no head-chef or line-cook named, the guava-hub start-up hook and the standing instructions do the work in one place, with no hand-offs. If the hub has a changelog page, add a dated line there.
5. **Offer the rest as their own numbered items**, left out of a plain yes, since they're the owner's own tools and other work may use them: the Notion MCP servers router setup added (`claude mcp remove notion -s user`, `codex mcp remove notion`), and the CLIs it installed, with their sign-ins (`codex logout` and `npm rm -g @openai/codex`; `claude auth logout` and `npm rm -g @anthropic-ai/claude-code`). Never remove the tool this is running in.
6. **Check and wrap up:** `claude plugin list` and `codex plugin list` (or `npx skills list -g`) no longer show guava-router (or the Codex plugin, if it was removed), and nothing from step 2 is left in those files. With the hub kept (not for the whole stack), run `claude -p --permission-mode plan "Which head-chef and line-cook are in my guava-stack settings?" < /dev/null`: it should find none. Confirm in two or three lines what was removed and what stayed, with the backups' paths.
