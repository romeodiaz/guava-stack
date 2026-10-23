---
name: guava-router
description: Sets up a Model Router that sends thinking work to a head-chef model and doing work to a line-cook model, through Claude Code on the owner's Claude plan and Codex on their ChatGPT plan, or both slots on whichever one plan they have, or through Google's Antigravity CLI on Google AI Pro or Ultra alone, with the models in models.yaml. Also use when the owner says "check for newer models", "update guava-router" or "uninstall guava-router". Use when the owner asks for model routing or the CLIs, or when hub setup hands off to the router.
---

**One yes per step.** Before each numbered step below, show its whole plan in your message text: every command, edit, install and setting change, word for word. Wait for one yes, then do the whole step and report what you did. Put the plan in your message text, never only inside a question or approval card, since some apps don't show what's in the card. Never ask for a yes to a change the owner hasn't seen.

# Model Router: setup

These steps send each kind of work to the model that's best at it, through the Claude plan, ChatGPT plan or both that the owner already pays for, or their Google AI Pro or Ultra plan when they have neither: thinking and reviewing to a **head-chef**, and heavy lifting to a **line-cook**. With both plans, the head-chef runs in Claude Code and the line-cook in Codex; with one, both run in that plan's tool. On Google AI alone, both run in Google's Antigravity CLI (`agy`), which serves Claude models on that plan, and each slot falls back to a Gemini model when its Claude usage runs out.

> Start with the **guava-hub** skill. It builds the hub first and sends you here from **Add a bot**. The router needs a computer to run Claude Code, Codex or Antigravity CLI, so it runs on a bot such as Grok Bot or Muse. In the Claude or ChatGPT app, tell the owner the router comes with adding a bot, and stop.

## 1. The models
Pick the row for the plans the owner pays for (hub setup asks; otherwise ask). Google AI Pro or Ultra counts only when the owner has neither a Claude nor a ChatGPT plan:

<!-- models:plans -->
| You pay for | head-chef | line-cook |
|---|---|---|
| Claude and ChatGPT (best) | Claude Opus 5.5 (High) via Claude Code | GPT-6.1 Sol (High) via Codex |
| Claude only | Claude Opus 5.5 (High) via Claude Code | Claude Sonnet 5.5 (High) via Claude Code |
| ChatGPT only | GPT-6 Astra (High) via Codex | GPT-6.1 Sol (High) via Codex |
| Google AI Pro or Ultra only | Claude Opus 5.5 (High) via Antigravity CLI, falling back to Gemini 4 Argon (High) when its usage runs out | Claude Sonnet 5.5 (High) via Antigravity CLI, falling back to Gemini 3.8 Flash (High) when its usage runs out |
<!-- /models -->

<!-- models:commands -->
| Slot | Model | Tool | Run it |
|---|---|---|---|
| head-chef | Claude Opus 5.5, effort high (`claude-opus-5-5`) | Claude Code | `claude -p --model claude-opus-5-5 --effort high "<task>" < /dev/null` |
| line-cook | GPT-6.1 Sol, effort high (`gpt-6.1-sol`) | Codex | `codex exec -m gpt-6.1-sol -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |
| head-chef, ChatGPT only | GPT-6 Astra, effort high (`gpt-6-astra`) | Codex | `codex exec -m gpt-6-astra -c model_reasoning_effort=high --skip-git-repo-check "<task>" < /dev/null` |
| line-cook, Claude only | Claude Sonnet 5.5, effort high (`claude-sonnet-5-5`) | Claude Code | `claude -p --model claude-sonnet-5-5 --effort high "<task>" < /dev/null` |
| head-chef, Google AI only | Claude Opus 5.5, effort high (`claude-opus-5-5-high`) | Antigravity CLI | `agy -p "<task>" --model claude-opus-5-5-high --effort high --mode accept-edits < /dev/null` |
| head-chef fallback, Google AI only | Gemini 4 Argon, effort high (`gemini-4-argon-high`) | Antigravity CLI | `agy -p "<task>" --model gemini-4-argon-high --effort high --mode accept-edits < /dev/null` |
| line-cook, Google AI only | Claude Sonnet 5.5, effort high (`claude-sonnet-5-5-high`) | Antigravity CLI | `agy -p "<task>" --model claude-sonnet-5-5-high --effort high --mode accept-edits < /dev/null` |
| line-cook fallback, Google AI only | Gemini 3.8 Flash, effort high (`gemini-3.8-flash-high`) | Antigravity CLI | `agy -p "<task>" --model gemini-3.8-flash-high --effort high --mode accept-edits < /dev/null` |
<!-- /models -->

The picks come from [models.yaml](https://github.com/romeodiaz/guava-stack/blob/main/guava-router/models.yaml), the one place they're kept; don't edit the table by hand, since `scripts/sync-models.py` rewrites it. Add `< /dev/null` so no CLI waits for input. The owner can pick their own for head-chef or line-cook: any Claude model through Claude Code, any OpenAI model through Codex, or on Google AI alone any model `agy models` lists, on a plan they have, with the same commands and that model's ID and effort, marked "(own pick)" in guava-stack settings so "check for newer models" leaves it alone. Guava supports no other setup yet: if the owner asks for another provider, tool or agent, say it isn't supported.

**Google AI alone:** each slot's model line names its Claude model and its Gemini fallback, as the plans table shows. Every hand-off runs the Claude model first. If agy answers that its usage, quota or rate limit has run out (rather than another error), run the same hand-off on the slot's fallback with the fallback row's command and say so in one line. The next hand-off tries the Claude model again, since Google's usage refills. If the fallback has run out too, stop and tell the owner when their usage refills, if agy said.

Add the **guava-router** heading to guava-stack settings above **Rules**, with `head-chef` and `line-cook` label lines, each followed by its model line and job sub-bullet, as the guava-hub skill's settings example shows. Use the owner's row of the plans table for both slots; on Google AI alone, each model line is that row's cell, fallback included.

## 2. Install the command-line tools
Only the tools the owner's plans need: Claude Code for a Claude plan, Codex for a ChatGPT plan, and Antigravity CLI on Google AI alone.
- Check first, without asking (these only read): `claude --version`, `codex --version` and `agy --version`. Skip the install for any tool that answers with a version, and tell the owner it's already there.
- Install only what's missing: Claude Code `npm i -g @anthropic-ai/claude-code` and Codex `npm i -g @openai/codex`. Then bring both up to date, even when they were already installed: `claude update` and `npm i -g @openai/codex@latest`. An older Claude Code or Codex rejects the newest models (Codex 0.149 answered that GPT-6.1 Sol "is not supported when using Codex with a ChatGPT account"; 0.163 runs it). Check both versions again, and if one didn't change, follow step 2 of **Repair** for an older copy that comes first on PATH. Antigravity CLI installs and updates with `curl -fsSL https://antigravity.google/cli/install.sh | bash`, which puts `agy` in `~/.local/bin`.
- Put the tools on the computer's PATH, so `claude`, `codex` and `agy` also work in its desktop terminal if the owner ever signs in there: find their folder with `dirname "$(command -v claude)"` (or `codex`, or `agy`), often `~/.local/bin`. If `~/.bashrc` or `~/.profile` doesn't already add that folder, back the file up (see **Backups** below) and add `export PATH="<folder>:$PATH"` at the end. Until a new terminal picks it up, give the owner the full path, such as `~/.local/bin/claude auth login`.
- Check sign-in: `claude auth status`, `codex login status`, and for Antigravity CLI `agy models`, which lists the plan's models only when signed in (it has no status command). Skip any that's already signed in; otherwise run the sign-in yourself, on the owner's own subscription, so they only open a link and send you back what it shows:
  - Codex: run `codex login --device-auth` in the background, send the owner its link and one-time code, and check `codex login status` once they say they've approved it.
  - Claude Code: `claude auth login` waits for a code typed into its own terminal, so start it in a tmux session: `tmux new-session -d -s claude-login 'claude auth login'`. Read its link with `tmux capture-pane -p -J -t claude-login`, send it to the owner, and when they paste the code back to you, type it in with `tmux send-keys -t claude-login '<code>' Enter`. Check `claude auth status`, then `tmux kill-session -t claude-login`. Without tmux, give the owner the command with its full path to run in the computer's desktop terminal instead.
  - Antigravity CLI: running `agy` starts its Google sign-in, so start it the same way, `tmux new-session -d -s agy-login 'agy'`, send the owner the link `tmux capture-pane -p -J -t agy-login` shows, type back anything they paste with `tmux send-keys`, and have them sign in with the Google account that has Google AI Pro or Ultra. Check `agy models` lists the four Google AI rows' model IDs, then `tmux kill-session -t agy-login`. Run agy without `GEMINI_API_KEY` or `GOOGLE_API_KEY` set, so it uses the plan's sign-in.
- Set each slot's model and effort as step 1 shows.
- **On the bot's own computer:** run every step here in Grok Bot's or Muse's own terminal, following the bot's adapter file. The owner opens each sign-in link and signs in with their own account, then pastes any code straight back into the bot.

## 3. Connect them to Notion
On Google AI alone, skip this step and step 4: the bot loads what each job needs from the hub and puts it in agy's prompt (the hand-off rule in step 5). Otherwise, for each tool step 2 set up, check what's already connected first (`claude mcp list`, `codex mcp list`) and skip anything that already shows Notion.
- Claude Code: run `claude mcp add --transport http --scope user notion https://mcp.notion.com/mcp`, then have the owner type `/mcp` in Claude Code and approve Notion's sign-in page.
- Codex: run `codex mcp add notion --url https://mcp.notion.com/mcp`, then `codex mcp login notion` and have the owner approve Notion's sign-in page. On a bot's computer, the owner's browser then lands on an error page at `127.0.0.1:<port>`, because that address belongs to the bot's computer: tell them so before they approve, and ask them to paste the whole address from the address bar back to you so you can finish the sign-in.

Test each tool with a quick non-interactive run that reads the context page from the hub, for example `claude -p "..." < /dev/null` and `codex exec --skip-git-repo-check "..." < /dev/null`.

The bot loads the hub and puts what each job needs into the tool's prompt (the hand-off rule in step 5), so neither `~/.claude/CLAUDE.md` nor `~/.codex/AGENTS.md` needs a Guava line.

<!-- guava-block: keep this paragraph the same in the guava-hub and guava-router skills -->
**Backups:** whenever a step says to back up a file, copy it to `<file>.bak-<local date and time>`, such as `settings.json.bak-2026-10-15-2122`. The first time Guava changes a file, also copy it to `<file>.pre-guava`, or create that copy empty if the file doesn't exist yet, and never overwrite it: uninstalling puts the file back from it. Entries the plugin commands wrote before it, such as `enabledPlugins`, can already be in it; the uninstall commands remove those themselves.
<!-- /guava-block -->

## 4. Let the tools read the hub
The bot runs Claude Code and Codex with nobody at the keyboard, and Claude Code then skips any tool that needs approval, so it can't read the hub. Pre-approve Notion's read-only tools, as part of the plan the owner says yes to:
- Back up `~/.claude/settings.json` first (see **Backups** above).
- Under `permissions.allow`, add only `notion-get-enabled-skills`, `notion-fetch`, `notion-search` and `notion-download-skill`, with the exact prefix `claude mcp list` shows (for example `mcp__claude_ai_Notion__notion-fetch`). Never pre-approve write or delete tools.
- If Codex's test run in step 3 couldn't read the hub, approve the same four tools for Codex.
- Test it with a non-interactive run that reads the context page.

## 5. Model routing
- **head-chef**: orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems. For important work, it also checks the line-cook's result before anything is called done.
- **line-cook**: bulk execution, coding, computer use, sub-agent tasks, worker threads, long-running jobs. For computer use, it uses browser tools first whenever a browser can do the job (its tool's own browser, such as Codex's browser plugin), in the browser where the owner is already signed in, since that's faster and more reliable than driving the screen and nobody has to hand over a login. It drives the screen only for apps outside the browser, with its tool's computer tools. If its tool has none, use your own.
- **Hand-off rule**: if a tool can't reach the hub, the head-chef (or you) loads what the job needs from the hub and puts it in that tool's prompt.
- **If a hand-off fails**: follow **Repair** below and retry once. If it still fails, do the task yourself and say so.
- **If you are running a slot's work** (head-chef or line-cook), do that work yourself on its named model and effort; hand off work for the other slots to their named tools. Include the slot name in each hand-off so the child knows its job and doesn't hand the same job off again. On one plan, head-chef and line-cook share a tool.
- **Grok Bot and Muse:** run Claude Code, Codex or both, or Antigravity CLI on Google AI alone, on their own computers and hand each job to the CLI its slot names.
- **Usage runs out on Google AI alone:** run that hand-off on the slot's Gemini fallback, as step 1 says. That's not a failure, so skip **Repair**.
- **Long jobs on Grok Bot**: any hand-off that may take more than a few minutes runs in the background, as **Long jobs** below says.
- **Skills with their own setup come first**: when a skill defines how it runs (its own engine, scripts, models or setup), follow it as designed and use this routing only for work it leaves open. Never change a skill's own setup to fit the routing.

Save these routing rules as a standing instruction if hub setup hasn't already, pointing at the head-chef and line-cook slots in guava-stack settings instead of naming models, so the owner can swap a model by editing guava-stack settings. On Grok Bot, save them to shared user memory only, so every current and future bot follows one copy.

### Long jobs
On Grok Bot, one command can wait at most 13 minutes, and the computer pauses between the bot's turns, so a CLI still running when the turn ends stops until the next one. For any hand-off that may take more than a few minutes:
1. **Start it in the background**, with its answer and log under `/workspace/guava-runs/` (`/workspace` survives a computer recovery). Pick a short job name, and for Claude Code a new session ID (`cat /proc/sys/kernel/random/uuid`):
   - Codex: `mkdir -p /workspace/guava-runs && nohup codex exec -m <id> -c model_reasoning_effort=<effort> --skip-git-repo-check -o /workspace/guava-runs/<job>.md "<task>" < /dev/null > /workspace/guava-runs/<job>.log 2>&1 &`
   - Claude Code: `mkdir -p /workspace/guava-runs && nohup claude -p --model <id> --effort <effort> --session-id <uuid> "<task>" < /dev/null > /workspace/guava-runs/<job>.md 2> /workspace/guava-runs/<job>.log &`
   - Antigravity CLI: `mkdir -p /workspace/guava-runs && nohup agy -p "<task>" --model <id> --effort <effort> --mode accept-edits < /dev/null > /workspace/guava-runs/<job>.md 2> /workspace/guava-runs/<job>.log &`
2. **Stay in your turn until it finishes.** Check every few minutes with short commands, such as `sleep 240; tail -n 20 /workspace/guava-runs/<job>.log`, each well under the command limit. Tell the owner it's still running, but never end your turn while a job runs.
3. **If it stopped without an answer, resume it instead of starting over**, in the background the same way: Codex `codex exec resume <session id> -o /workspace/guava-runs/<job>.md "Continue where you left off." < /dev/null`, with the session ID from the top of `<job>.log`; Claude Code `claude -p --resume <uuid> "Continue where you left off." < /dev/null`; Antigravity CLI has no resume Guava has checked, so start the job again with what's already done in its prompt. If it fails again, do the task yourself and say so.
4. **Split big jobs.** The head-chef breaks work that could run for hours into steps the line-cook can finish one at a time, and checks each before the next starts.

### Repair
A bot's computer can be replaced or reset (Muse and Grok Bot both do this), which wipes the tools, their sign-ins, Codex's Notion connection and Claude Code's settings. When a hand-off fails, or a tool says it's missing, unsigned, expired or doesn't support the model, check these in order on that tool and fix only what's broken, using the setup step named:
1. **Installed?** `command -v claude`, `command -v codex` or `command -v agy`. Missing: reinstall as step 2 says.
2. **Up to date?** Always run `claude update`, `npm i -g @openai/codex@latest` or Antigravity CLI's install script: an old version rejects new models. Then check `claude --version`, `codex --version` or `agy --version` again. If the version didn't change, an older copy comes first on PATH (Muse's image ships its own Codex in `/opt/hatch-image/bin`): use the updated one by its full path, `$(npm prefix -g)/bin/codex`, for every hand-off, and look it up again after each reset rather than remembering a fixed path.
3. **Signed in?** `claude auth status`, `codex login status` or `agy models`, then the tool's tiny test from step 1's commands table, since a status can say signed in while the token has expired (a 401 or `token_expired`). Not working: start the sign-in as step 2 says and send the owner the link.
4. **Connected to Notion?** `claude mcp list` or `codex mcp list` (not for Antigravity CLI, which gets the hub through its prompt). Missing: reconnect as step 3 says.
5. **Allowed to read the hub?** Claude Code's `~/.claude/settings.json` still approves Notion's four read-only tools. Missing: restore them as step 4 says, backing up first.

Restoring what setup already installed needs no new yes, since the owner approved it at setup: tell them in one line what was reset and what you fixed, for example "Your bot's computer was reset, so I reinstalled Codex and need you to approve its sign-in." Anything beyond restoring setup needs a yes as usual. Then retry the hand-off once.

## 6. Stay inside each provider's terms
For Claude Code on a Claude plan:
- Use the official Claude Code CLI with your own login only.
- Never share tokens or route other people's requests through your plan.
- Keep Claude work tied to tasks you start. No unattended loops or 24/7 jobs on the plan; send those to the line-cook in Codex, or on Claude only, to an Anthropic API key.
- Stop when you hit usage limits.
- Never use outputs to train competing models.
- For heavy or always-on Claude automation, use an Anthropic API key.

For Codex, follow OpenAI's current terms for the owner's plan.

For Antigravity CLI on Google AI Pro or Ultra, follow Google's current terms for the owner's plan, signed in as the owner. Falling back to Gemini when Claude's usage runs out stays on the same plan; when Gemini's runs out too, stop.

## 7. Final checks
- Check the current terms for each provider the owner uses.
- Test head-chef and line-cook with a quick prompt and tell the owner which model actually answered. Don't call setup done until both pass.
- Running this as part of hub setup? Go back to the hub setup skill's founder-mode step.

## Changing the setup later
To change head-chef or line-cook, or apply a hand-edited guava-stack settings section, follow **Change your setup** in the guava-hub skill. "Check for newer models" checks both slots there too.

## Update
Use this when the owner says **"update guava-router"**, or when the guava-hub skill's Update step sends you here. Show the whole plan first, in your message text, as one numbered list (each command, and each change as old, then new); the owner can approve it with one yes or pick numbers. Then apply it in order.

1. **Get the newest files** (skip this when the guava-hub Update step already did it):
<!-- update-steps: keep this list the same in the guava-hub, guava-router and founder-mode skills -->
Only for the Guava plugins the owner has (for "update guava-router", just guava-router):
- **Claude Code:** `claude plugin marketplace update guava`, then `claude plugin update <plugin>@guava` for each plugin. Updates apply in a new session.
- **Codex:** `codex plugin marketplace upgrade guava`, then `codex plugin add <plugin>@guava` for each plugin. Updates apply in a new chat.
- **Grok Bot:** `npx skills update -g -y`.
- **Muse, and the Claude and ChatGPT apps:** no skill files, so nothing to download.
<!-- /update-steps -->
2. **Check for newer models:** follow **Change your setup** in the guava-hub skill with "check for newer models".
3. **Check the routing still runs:** each tool the owner's plans need is installed and signed in on the bot's computer (step 2 of setup, checking first).
4. **Test** head-chef and line-cook as in step 7, and confirm in two or three lines: guava-router's version before and after, any model change, and anything left for the owner.

## Uninstall
Use this when the owner says **"uninstall guava-router"**, or when the guava-hub skill's Uninstall step sends you here. It stops the routing and puts back what router setup changed. Show the whole plan first, in your message text, as one numbered list (each command, each file change as old, then new, and each app step); the owner can approve it with one yes or pick numbers. Then apply it in order.

<!-- guava-restore: keep this paragraph the same in the guava-hub and guava-router skills -->
**Putting files back** (`~/.claude/settings.json` and `~/.codex/config.toml`): `<file>.pre-guava` next to each file shows how it was before Guava (see **Backups** in setup step 2 of the guava-hub skill). Run the plugin commands first, since they rewrite these files and remove their own entries. Then, for only the settings the Uninstall step lists, put each one back to its value in the `.pre-guava` copy, or remove it if that copy doesn't have it; if the owner has changed it since Guava set it, ask instead. Drop any section left empty that the copy doesn't have, such as an empty `enabledPlugins`. Never copy a backup over the file, since that would undo every change the owner made since, and never change anything else. With no `.pre-guava` copy, remove only what Guava added and ask about any value it may have replaced. Leave the `.pre-guava` and `.bak-` copies where they are and list them in the wrap-up, so the owner can delete them once they're happy.
<!-- /guava-restore -->

1. **Remove the plugin** (skip this when the guava-hub Uninstall step already did it). When uninstalling guava-router on its own, first check what's there without asking, as step 1 of the guava-hub Uninstall step says:
<!-- uninstall-steps: keep this list the same in the guava-hub, guava-router and founder-mode skills -->
Only for the Guava plugins the owner has (for "uninstall guava-router", just guava-router; for "uninstall guava-stack", every one installed):
- **Claude Code:** `claude plugin uninstall <plugin>@guava` for each plugin. Once no Guava plugin is left, `claude plugin marketplace remove guava`, then delete `~/.claude/plugins/cache/guava` if it's still there (if your safety check won't let you delete a folder in these steps, move it into `~/guava-uninstalled/` instead and list it in the wrap-up). It applies in a new session.
- **Codex:** `codex plugin remove <plugin>@guava` for each plugin. Once no Guava plugin is left, `codex plugin marketplace remove guava`, then delete `~/.codex/plugins/cache/guava` if it's still there, and each `~/.codex/.tmp/marketplaces/.staging/marketplace-upgrade-*` folder holding a copy of guava-stack, which marketplace upgrades leave behind. It applies in a new chat.
- **Grok Bot:** `npx skills remove -g -s <plugin> -y` for each skill, and check with `npx skills list -g`.
- **Muse, and the Claude and ChatGPT apps:** no skill files, so nothing to delete.
<!-- /uninstall-steps -->
2. **Put the computer back**, following **Putting files back** above:
   - `~/.claude/settings.json`: `model`, if router setup set it. Say which model new sessions will use instead. The hub's read-only tools under `permissions.allow` stay while the hub does: guava-hub's Uninstall step removes them.
   - `~/.codex/config.toml`: `model`, if router setup set it, saying which model new chats will use instead.
3. **Take routing out of Grok Bot and Muse:** on Grok Bot, delete the routing memories, shared user memory included; on Muse, delete the routing line at the end of SOUL.md. Show the exact text to delete and wait for done.
4. **Turn routing off in the hub** (skip this when uninstalling the whole stack, since the hub then stays as it is): in guava-stack settings, remove the guava-router heading, with the head-chef and line-cook lines, their model lines and sub-bullets and, in Notion, its images. With neither slot named, the guava-hub start-up hook and the standing instructions do the work in one place, with no hand-offs. Log the hub edit on this work's task in the hub's tasks database.
5. **Offer the rest as their own numbered items**, left out of a plain yes, since they're the owner's own tools and other work may use them: the Notion MCP servers router setup added (`claude mcp remove notion -s user`, `codex mcp remove notion`), and the CLIs it installed, with their sign-ins (`codex logout` and `npm rm -g @openai/codex`; `claude auth logout` and `npm rm -g @anthropic-ai/claude-code`; Antigravity CLI, signing out with `/logout` in `agy` and removing it as Google's docs say), together with the `export PATH` line router setup added to `~/.bashrc` and `~/.profile`. Never remove the tool this is running in.
6. **Check and wrap up:** `claude plugin list` and `codex plugin list` (or `npx skills list -g`) no longer show guava-router, and nothing from step 2 is left in those files. With the hub kept (not for the whole stack), run `claude -p --permission-mode plan "Which head-chef and line-cook slots are in my guava-stack settings?" < /dev/null`: it should find none. Confirm in two or three lines what was removed and what stayed, with the backups' paths.
