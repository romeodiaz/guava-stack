---
name: guava-router
description: Sets up a Model Router that sends thinking work to a head-chef model through Claude Code and doing work to a line-cook model through Codex, on the owner's own Claude and ChatGPT plans, with the models in models.yaml. Also use when the owner says "check for newer models", "update guava-router" or "uninstall guava-router". Use when the owner asks for model routing or the CLIs, or when hub setup hands off to the router.
---

**Before every edit, install or setting change below, show the owner the exact command or change and wait for a yes.** Put it in your message text before you ask, never only inside a question or approval card, since some apps don't show what's in the card. Never ask for a yes to a change the owner hasn't seen.

# Model Router: setup

These steps send each kind of work to the model that's best at it, through the Claude and ChatGPT plans the owner already pays for: thinking and reviewing to a **head-chef** in Claude Code, and heavy lifting to a **line-cook** in Codex.

> Start with the **guava-hub** skill. It builds the hub first and sends you here at the right step.

## 1. The models
<!-- models:commands -->
| Slot | Model | Tool | Run it |
|---|---|---|---|
| head-chef | Claude Opus 5.5, effort high (`claude-opus-5-5`) | Claude Code | `claude -p --model claude-opus-5-5 --effort high "<task>" < /dev/null` |
| line-cook | GPT-6.1 Sol, effort high (`gpt-6.1-sol`) | Codex | `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |
<!-- /models -->

The picks come from [models.yaml](https://github.com/romeodiaz/guava-stack/blob/main/guava-router/models.yaml), the one place they're kept; don't edit the table by hand, since `scripts/sync-models.py` rewrites it. Add `< /dev/null` so neither CLI waits for input. The owner can pick their own: any Claude model as head-chef and any OpenAI model as line-cook, with the same commands and that model's ID and effort, marked "(own pick)" in guava-stack settings so "check for newer models" leaves it alone. Guava supports no other setup yet: if the owner asks for another plan, tool or agent, say it isn't supported.

## 2. Install the command-line tools
- Check first, without asking (these only read): `claude --version` and `codex --version`. Skip the install for any tool that answers with a version, and tell the owner it's already there.
- Install only what's missing: Claude Code `npm i -g @anthropic-ai/claude-code` (skip it in the Code tab, where it's built in) and Codex `npm i -g @openai/codex`.
- Check sign-in: `claude auth status` and `codex login status`. Skip any that's already signed in; otherwise sign in with the owner's own subscription: `claude auth login` and `codex login --device-auth`.
- Set each slot's model and effort as step 1 shows.
- **Claude desktop app's Code tab:** also install OpenAI's official [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc), so Claude hands jobs to Codex natively. Run `claude plugin marketplace add openai/codex-plugin-cc` and `claude plugin install codex@openai-codex` as shell commands in the session (with a yes), or add the marketplace that way and install from **+ > Plugins > Add plugin**. Then start a new session and run `/codex:setup` to check it. It uses the Codex CLI and ChatGPT sign-in from above. Leave its review gate off (it stays off unless someone runs `/codex:setup --enable-review-gate`): it can loop and drain usage limits, and it's the kind of unattended Claude loop step 6 rules out.
- **Code tab from the phone:** offer to turn on Remote Control for every new session: back up `~/.claude/settings.json` (see **Backups** below), then set `"remoteControlAtStartup": true` in it (or the owner turns on **Connect new sessions to Remote Control** in the desktop app's Settings, then Claude Code). The owner can then open any Code tab session from the Claude phone app (tap Code, then pick the session with the green dot) while the computer is on and the app is open. It needs a Pro or Max plan.
- **Local only:** Guava runs the Code tab and Codex on the owner's computer. Cloud sessions in the Code tab and Codex cloud tasks aren't supported, since they don't load the plugins or the owner's sign-ins. Tell the owner to pick **Local** when they start a Code tab session (the app has no setting to make it the default), and to use the Codex app or CLI on their computer. If you're running in a cloud session, say so in one line and ask the owner to start a Local one.

## 3. Connect them to Notion
Check what's already connected first (`claude mcp list`, `codex mcp list`) and skip anything that already shows Notion.
- Claude Code: if the owner already connected Notion in the Claude app, Claude Code picks it up automatically. Otherwise run `claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp`, then have the owner type `/mcp` in Claude Code and approve Notion's sign-in page.
- Codex: run `codex mcp add notion --url https://mcp.notion.com/mcp`, then `codex mcp login notion` and have the owner approve Notion's sign-in page.

Test each tool with a quick non-interactive run that reads the context page from the hub, for example `claude -p "..." < /dev/null` and `codex exec --skip-git-repo-check "..." < /dev/null`.

The guava-hub plugin's start-up hook tells every new Claude Code and Codex session to load the hub and follow guava-stack settings, so neither `~/.claude/CLAUDE.md` nor `~/.codex/AGENTS.md` needs a Guava line. If either tool doesn't have the guava-hub plugin, install it there rather than writing the instructions into that file.

<!-- guava-block: keep this paragraph the same in the guava-hub and guava-router skills -->
**Backups:** whenever a step says to back up a file, copy it to `<file>.bak-<local date and time>`, such as `settings.json.bak-2026-10-15-2122`. The first time Guava changes a file, also copy it to `<file>.pre-guava`, or create that copy empty if the file doesn't exist yet, and never overwrite it: uninstalling puts the file back from it. Entries the plugin commands wrote before it, such as `enabledPlugins`, can already be in it; the uninstall commands remove those themselves.
<!-- /guava-block -->

## 4. Never skip the hub (optional)
Only if the owner wants it. When nobody is at the keyboard, Claude Code skips tools that need approval, so the hub never loads. Fix it:
- Explain that this changes Claude Code's permission settings, show the exact lines you'll add, and get a yes.
- Back up `~/.claude/settings.json` first (see **Backups** above).
- Under `permissions.allow`, add only Notion's read-only tools, with the exact prefix `claude mcp list` shows: `notion-get-enabled-skills`, `notion-fetch`, `notion-search`, `notion-download-skill` (for example `mcp__claude_ai_Notion__notion-fetch`).
- Do the same for Codex if needed.
- Never pre-approve write or delete tools.
- Test it with a non-interactive run and confirm the skills load.

## 5. Model routing
- **head-chef**: orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems. For important work, it also checks the line-cook's result before anything is called done.
- **line-cook**: bulk execution, coding, sub-agent tasks, worker threads, long-running jobs.
- **Browser and desktop tasks**: keep using the assistant's own computer tools.
- **Hand-off rule**: if a tool can't reach the hub, the head-chef (or you) loads what the job needs from the hub and puts it in that tool's prompt.
- **If either fails**: do the task yourself and say so.
- **If you are the head-chef or the line-cook** (say, Claude Code on the head-chef's model), do that slot's work yourself and send only the other slot's work out.
- **Code tab with the Codex plugin:** hand line-cook jobs to the `codex:codex-rescue` subagent with the line-cook's model and effort from guava-stack settings (the owner can also type `/codex:rescue --model <line-cook model ID> --effort <its effort> ...`). Run long jobs in the background and check them with `/codex:status` and `/codex:result`. For a second opinion on important work, use `/codex:adversarial-review`.
- **Grok Bot and Muse:** run Claude Code and Codex on their own computers and hand each job to the CLI its slot names.
- **Skills with their own setup come first**: when a skill defines how it runs (its own engine, scripts, models or setup), follow it as designed and use this routing only for work it leaves open. Never change a skill's own setup to fit the routing.

Save these routing rules as a standing instruction if hub setup hasn't already, pointing at the head-chef and line-cook in guava-stack settings instead of naming models, so the owner can swap a model by editing guava-stack settings. On Grok Bot, save them to shared user memory too, so every current and future bot follows them.

The Claude and ChatGPT chat apps (web, desktop and phone) read the hub but don't route: each chat works on whatever model the owner picked.

## 6. Stay inside each provider's terms
For Claude Code on a Claude plan:
- Use the official Claude Code CLI with your own login only.
- Never share tokens or route other people's requests through your plan.
- Keep Claude work tied to tasks you start. No unattended loops or 24/7 jobs on the plan; send those to the line-cook.
- Stop when you hit usage limits.
- Never use outputs to train competing models.
- For heavy or always-on Claude automation, use an Anthropic API key, or do it by hand in Claude Desktop.

For Codex, follow OpenAI's current terms for the owner's plan.

## 7. Final checks
- Check the current terms for both providers.
- Test each slot with a quick prompt and tell the owner which model actually answered. Don't call setup done until both slots pass.
- Running this as part of hub setup? Go back to the hub setup skill's founder-mode step.

## Changing the setup later
To swap models, or apply a hand-edited guava-stack settings section, follow **Change your setup** in the guava-hub skill. "Check for newer models" goes there too.

## Update
Use this when the owner says **"update guava-router"**, or when the guava-hub skill's Update step sends you here. Show the whole plan first, in your message text, as one numbered list (each command, and each change as old, then new); the owner can approve it with one yes or pick numbers. Then apply it in order.

1. **Get the newest files** (skip this when the guava-hub Update step already did it):
<!-- update-steps: keep this list the same in the guava-hub, guava-router and founder-mode skills -->
Only for the Guava plugins the owner has (for "update guava-router", just guava-router):
- **Claude Code or the Claude desktop app's Code tab:** `claude plugin marketplace update guava`, then `claude plugin update <plugin>@guava` for each plugin. Updates apply in a new session.
- **Codex:** `codex plugin marketplace upgrade guava`, then `codex plugin add <plugin>@guava` for each plugin. Updates apply in a new chat.
- **Grok Bot:** `npx skills update -g -y`.
- **Muse:** no skill files, so nothing to download.
<!-- /update-steps -->
2. **Check for newer models:** follow **Change your setup** in the guava-hub skill with "check for newer models".
3. **Check the routing still runs:** both tools are installed and signed in (step 2 of setup, checking first), and in the Code tab the Codex plugin is installed and `/codex:setup` reports ready with the review gate off.
4. **Test** each slot with a quick prompt, as in step 7, and confirm in two or three lines: guava-router's version before and after, any model change, and anything left for the owner.

## Uninstall
Use this when the owner says **"uninstall guava-router"**, or when the guava-hub skill's Uninstall step sends you here. It stops the routing and puts back what router setup changed. Show the whole plan first, in your message text, as one numbered list (each command, each file change as old, then new, and each app step); the owner can approve it with one yes or pick numbers. Then apply it in order.

<!-- guava-restore: keep this paragraph the same in the guava-hub and guava-router skills -->
**Putting files back** (`~/.claude/settings.json` and `~/.codex/config.toml`): `<file>.pre-guava` next to each file shows how it was before Guava (see **Backups** in setup step 1 of the guava-hub skill). Run the plugin commands first, since they rewrite these files and remove their own entries. Then, for only the settings the Uninstall step lists, put each one back to its value in the `.pre-guava` copy, or remove it if that copy doesn't have it; if the owner has changed it since Guava set it, ask instead. Drop any section left empty that the copy doesn't have, such as an empty `enabledPlugins`. Never copy a backup over the file, since that would undo every change the owner made since, and never change anything else. With no `.pre-guava` copy, remove only what Guava added and ask about any value it may have replaced. Leave the `.pre-guava` and `.bak-` copies where they are and list them in the wrap-up, so the owner can delete them once they're happy.
<!-- /guava-restore -->

1. **Remove the plugin** (skip this when the guava-hub Uninstall step already did it). When uninstalling guava-router on its own, first check what's there without asking, as step 1 of the guava-hub Uninstall step says:
<!-- uninstall-steps: keep this list the same in the guava-hub, guava-router and founder-mode skills -->
Only for the Guava plugins the owner has (for "uninstall guava-router", just guava-router; for "uninstall guava-stack", every one installed):
- **Claude Code or the Claude desktop app's Code tab:** `claude plugin uninstall <plugin>@guava` for each plugin. Once no Guava plugin is left, `claude plugin marketplace remove guava`, then delete `~/.claude/plugins/cache/guava` if it's still there (if your safety check won't let you delete a folder in these steps, move it into `~/guava-uninstalled/` instead and list it in the wrap-up). It applies in a new session.
- **Codex:** `codex plugin remove <plugin>@guava` for each plugin. Once no Guava plugin is left, `codex plugin marketplace remove guava`, then delete `~/.codex/plugins/cache/guava` if it's still there, and each `~/.codex/.tmp/marketplaces/.staging/marketplace-upgrade-*` folder holding a copy of guava-stack, which marketplace upgrades leave behind. It applies in a new chat.
- **Grok Bot:** `npx skills remove -g -s <plugin> -y` for each skill, and check with `npx skills list -g`.
- **Muse:** no skill files, so nothing to delete.
<!-- /uninstall-steps -->
2. **Put the computer back**, following **Putting files back** above:
   - `~/.claude/settings.json`: `remoteControlAtStartup` and `model`, which is also the Code tab's model setting. Say which model new sessions will use instead. The hub's read-only tools under `permissions.allow` stay while the hub does: guava-hub's Uninstall step removes them.
   - `~/.codex/config.toml`: `model`, saying which model new chats will use instead.
   - The Codex plugin for Claude Code, if router setup installed it: `claude plugin list` shows `codex@openai-codex` and `~/.claude/settings.json.pre-guava` doesn't list it under `enabledPlugins` (if there's no such copy, ask): `claude plugin uninstall codex@openai-codex`, then `claude plugin marketplace remove openai-codex`, then delete `~/.claude/plugins/cache/openai-codex` if it's still there.
3. **Take routing out of Grok Bot and Muse:** on Grok Bot, delete the routing memories, shared user memory included; on Muse, delete the routing line at the end of SOUL.md. Show the exact text to delete and wait for done.
4. **Turn routing off in the hub** (skip this when uninstalling the whole stack, since the hub then stays as it is): in guava-stack settings, remove the guava-router heading, with the head-chef and line-cook lines, their model lines and sub-bullets and, in Notion, its images. With no head-chef or line-cook named, the guava-hub start-up hook and the standing instructions do the work in one place, with no hand-offs. Add a dated line to the hub's changelog page.
5. **Offer the rest as their own numbered items**, left out of a plain yes, since they're the owner's own tools and other work may use them: the Notion MCP servers router setup added (`claude mcp remove notion -s user`, `codex mcp remove notion`), and the CLIs it installed, with their sign-ins (`codex logout` and `npm rm -g @openai/codex`; `claude auth logout` and `npm rm -g @anthropic-ai/claude-code`). Never remove the tool this is running in.
6. **Check and wrap up:** `claude plugin list` and `codex plugin list` (or `npx skills list -g`) no longer show guava-router (or the Codex plugin, if it was removed), and nothing from step 2 is left in those files. With the hub kept (not for the whole stack), run `claude -p --permission-mode plan "Which head-chef and line-cook are in my guava-stack settings?" < /dev/null`: it should find none. Confirm in two or three lines what was removed and what stayed, with the backups' paths.
