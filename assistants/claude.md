# Claude adapter

- **Claude Code:** type `/plugin`, add the `romeodiaz/guava-stack` marketplace (it shows up as **guava**) and install **guava-hub**, **guava-router** and **founder-mode** from the list. Updates come through the same menu. Or just paste the Start here line.
- The standing instructions in the README go in a short section added to the end of `~/.claude/CLAUDE.md`. Never replace what's already there.
- Claude Code runs on the owner's computer, so every hub and router setup step applies. The router's "Never skip the hub" step is optional.
- Claude is the planner in the default and Claude-only setups, so do planner work yourself and send worker jobs out: to Codex in the default setup, through OpenAI's [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc) (the router setup installs it), or to Claude Sonnet 5.5 (`claude -p --model claude-sonnet-5-5`) in Claude only.
- To import existing context, ask the owner to paste or export it. Don't read Claude memories or chat history yourself.
- **Claude apps (web and desktop):** connect the hub's connector (Notion by default), add the hub instruction line from the backend's file, such as "Load my Notion AI Context Hub first.", and upload the skills from `guava-hub/skills/`, `guava-router/skills/` and `founder-mode/skills/` if the owner wants them there. The apps can't install CLIs, so set up the Model Router's **App routing** step instead: it adds instructions that tell Claude which model plans and which executes.
