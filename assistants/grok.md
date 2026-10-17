# Grok Bot adapter

- Where the owner works, on a $30 a month xAI or Cursor plan. They drive everything from here, on any device.
- **Connect your hub:** connect Notion in Grok Bot's own settings if it offers a Notion connector, and approve access to the guava-hub. If it doesn't, Grok Bot reads the hub through Claude Code and Codex on its computer, once step 3 of the router setup connects them to Notion.
- Install: paste the Start here line from the README.
- Grok Bot keeps the skills as files: it installs them with `npx skills add romeodiaz/guava-stack -g -y`.
- The standing instructions are saved as Grok Bot memories, and to shared user memory too, so every current and future bot follows them.
- Grok Bot runs Claude Code and Codex on its own computer, so every hub and router setup step applies, including the Model Router (guava-router).
- Grok Bot can't switch its own model; it routes head-chef work and line-cook jobs to the CLIs (<!-- models:default-pair -->Claude Opus 5.5 and GPT-6.1 Sol<!-- /models --> by default).
