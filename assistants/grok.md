# Grok Bot adapter

- A recommended addition on a $30 a month xAI or Cursor plan: a bot with its own computer that the owner hands whole jobs to, from any device. Setting it up runs **Add a bot** in the setup skill.
- **Fastest start: Guava's Grok Bot template**, https://x.ai/bot/bp8zbSkrzoJo6wKrv9Eny. The owner opens it and clicks **Add to Grok Bot**. The new bot, guava-bot, already has the standing instructions in its description and two skills (guava-stack and getting-started); its first chat connects Notion, makes or finds the hub and sets up the Model Router, so they say "set me up" in it next.
- **Connect your hub:** walk the owner through it one step per message: "Click **Connect Apps** in the bottom left." "Search for Notion and click **Add**." (Show them the screenshot: ![Grok Bot Connect Apps with Notion and its Add button](https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/setup/grok-connect-apps.png)) "Sign in to Notion and approve access to the workspace with your guava-hub."
- Install: paste the Start here line from the README.
- Grok Bot keeps the skills as files: it installs them with `npx skills add romeodiaz/guava-stack -g -y`. Check with `npx skills list -g`. "Failed" lines for other AI tools, such as PromptScript, are harmless: the installer tries every tool it knows.
- The standing instructions are saved as Grok Bot memories, and to shared user memory too, so every current and future bot follows them.
- Grok Bot runs Claude Code and Codex on its own computer, so every hub and router setup step applies, including the Model Router (guava-router).
- Grok Bot's computer pauses between its turns, and one command can wait at most 13 minutes, so CLI runs that may take longer follow **Long jobs** in the guava-router skill.
- Grok Bot can't switch its own model; it routes head-chef work and line-cook jobs to the CLIs (<!-- models:default-pair -->Claude Opus 5.5 and GPT-6.1 Sol<!-- /models --> by default).
