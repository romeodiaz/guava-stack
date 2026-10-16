# Grok Bot adapter

- Install: the [AI Context & Skills Hub template](https://x.ai/bot/rAhhI5cD__CnejfWqf3wH), which uses the defaults (a Notion hub, Claude + ChatGPT). For another hub or AI setup, paste the Start here line instead.
- The standing instructions in the README are saved as Grok Bot memories.
- Grok Bot runs Claude Code and Codex on its own computer, so every hub and router setup step applies, including the Model Router (guava-router).
- Grok Bot can't switch its own model; it routes planner work and builder jobs to the CLIs in the owner's AI setup (<!-- models:default-pair -->Claude Opus 5.5 and GPT-6.1 Sol<!-- /models --> by default).
- Save the standing instructions to shared user memory too, so every current and future bot follows them.
- A local Markdown or Obsidian hub doesn't work with Grok Bot, since it can't reach a folder on the owner's computer. Owners who want one use the Claude desktop app's Code tab instead (see `guava-hub/skills/guava-hub/backends/local-markdown.md`).
