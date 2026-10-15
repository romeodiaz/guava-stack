# Claude adapter

- **Claude Code:** type `/plugin`, add the `romeodiaz/guava-stack` marketplace (it shows up as **guava**) and install **guava-hub**, **guava-router** and **guava-mode** from the list. Updates come through the same menu. Or just paste the Start here line.
- The standing instructions in the README go in a short section added to the end of `~/.claude/CLAUDE.md`. Never replace what's already there.
- Claude Code runs on the owner's computer, so every hub and router setup step applies. The router's "Never skip Notion" step is optional.
- Claude is the thinking model here, so do judgment work yourself and send bulk execution and coding to Codex through the Codex CLI, if it's installed.
- To import existing context, ask the owner to paste or export it. Don't read Claude memories or chat history yourself.
- **Claude apps (web and desktop):** connect Notion, add the custom instruction "Load my Notion AI Context Hub first." and upload the skills from `guava-hub/skills/` and `guava-mode/skills/` if the owner wants them there. The apps can't install CLIs, so skip the Model Router setup (guava-router) and tell the owner what you skipped.
