# ChatGPT adapter

- **ChatGPT and ChatGPT Dots:** build the plugin with Plugin Creator (Plugins, then Add, then Create Plugin) from the three skills in `guava-hub/skills/`, `guava-router/skills/` and `guava-mode/skills/`. Rebuild it when the repo changes, since a published plugin is a snapshot.
- The standing instructions in the README go in ChatGPT's custom instructions. Add to what's there; never replace it.
- Connect Notion and add the custom instruction "Load my Notion AI Context Hub first."
- **ChatGPT Dots doesn't read custom instructions.** After Notion is connected, have the owner send their Dot this once: "From now on, before any substantive task, load my Notion AI Context Hub first (Profile & Context, Agent Rules and Skills) and treat it as the source of truth. Save this as a standing preference." Approve the save if a card shows. To verify, ask the Dot "What preferences do you remember about me?" and then "Write a short intro about my business."; it passes if the intro uses details from the hub.
- ChatGPT can't install CLIs, so skip the Model Router setup (guava-router) and tell the owner what you skipped.
- To import existing context, ask the owner to paste or export it.
- **Codex:** ask Codex "Install the skills from github.com/romeodiaz/guava-stack" and it installs them with its built-in skill installer. Then start a new chat, since installing doesn't turn anything on, and paste the Start here line. Add the standing instructions to the end of `~/.codex/AGENTS.md`. Codex is the execution model here, so send judgment work to Claude Opus 5.5 through the Claude CLI, if it's installed.
