# Claude adapter

- **Claude Code:** install the plugin with `/plugin marketplace add romeodiaz/guava-mode`, then `/plugin install guava-mode@guava`. Update with `/plugin update`.
- The standing instructions in the README go in a short section added to the end of `~/.claude/CLAUDE.md`. Never replace what's already there.
- Claude Code runs on the owner's computer, so all hub-setup skill steps apply. Step 2b is optional.
- Claude is the thinking model here, so do judgment work yourself and send bulk execution and coding to Codex through the Codex CLI, if it's installed.
- To import existing context, ask the owner to paste or export it. Don't read Claude memories or chat history yourself.
- **Claude apps (web and desktop):** connect Notion, add the custom instruction "Load my Notion AI Context Hub first." and upload the two skills from `skills/` if the owner wants them there. The apps can't install CLIs, so skip steps 2 and 2b and tell the owner what you skipped.
