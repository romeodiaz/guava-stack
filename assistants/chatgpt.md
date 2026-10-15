# ChatGPT adapter

- **ChatGPT and ChatGPT Dots:** build the plugin with Plugin Creator (Plugins, then Add, then Create Plugin) from the two skills in `skills/`. Rebuild it when the repo changes, since a published plugin is a snapshot.
- The standing instructions in the README go in ChatGPT's custom instructions. Add to what's there; never replace it.
- Connect Notion and add the custom instruction "Load my Notion AI Context Hub first."
- ChatGPT can't install CLIs, so skip steps 2 and 2b and tell the owner what you skipped.
- To import existing context, ask the owner to paste or export it.
- **Codex:** ask Codex "Install the skills from github.com/romeodiaz/guava-mode" and it installs them with its built-in skill installer. Add the standing instructions to the end of `~/.codex/AGENTS.md`. Codex is the execution model here, so send judgment work to Claude Opus 5.5 through the Claude CLI, if it's installed.
