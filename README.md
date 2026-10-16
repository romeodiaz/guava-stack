<p align="center"><img src="assets/logo.png" alt="Guava logo" width="120"></p>

# guava-stack: AI brain + router + rules

<p align="center"><a href="https://skills.sh/romeodiaz/guava-stack"><img src="https://skills.sh/b/romeodiaz/guava-stack" alt="skills.sh"></a></p>

**Free, open source, and yours to keep.**

Your business context, rules and skills in one place you already own. Every AI assistant reads from it, on every device. No code needed: paste one line and your assistant sets it up.

## What you get
Start with the hub. The other two are optional.

<table>
<tr>
<td align="center" width="33%"><a href="guava-hub/"><img src="assets/brain-hub.png" width="120" alt="Pixel-art brain"></a><br><strong>AI brain</strong><br><sub>guava-hub</sub></td>
<td align="center" width="33%"><a href="guava-router/"><img src="assets/model-router.png" width="120" alt="Pixel-art router"></a><br><strong>Router</strong><br><sub>guava-router (optional)</sub></td>
<td align="center" width="33%"><a href="founder-mode/"><img src="assets/founder-mode.png" width="120" alt="Pixel-art speaker at a microphone"></a><br><strong>Rules</strong><br><sub>founder-mode (optional)</sub></td>
</tr>
<tr>
<td>One home for your context, rules and skills. Every assistant you connect reads it.</td>
<td>Sends each job to the best AI model on the plans you already pay for.</td>
<td>27 working rules. Your AI does the safe work itself, writes like a human, and asks before anything costly or permanent.</td>
</tr>
</table>

Your hub has three parts:

<table>
<tr>
<td align="center" width="33%"><img src="assets/logo.png" width="80" alt="Guava logo"><br><strong>context</strong><br><sub>Who you are, your business, your tools</sub></td>
<td align="center" width="33%"><img src="assets/founder-mode.png" width="80" alt="Pixel-art speaker at a microphone"><br><strong>rules</strong><br><sub>How your AI should work for you</sub></td>
<td align="center" width="33%"><img src="assets/skills.png" width="80" alt="Pixel-art stack of books"><br><strong>skills</strong><br><sub>Step-by-step instructions your AI reuses</sub></td>
</tr>
</table>

## Why people use it
- 🗣️ **Explain your business once.** Every assistant already knows it.
- 💳 **Nothing new to buy.** Claude, ChatGPT, Grok Bot, Muse and more, on the plans you already have.
- 📱 **Everywhere.** The same context and rules on your desk, laptop and phone.
- 🔓 **No lock-in.** It lives in your own account. Switch hub, assistant or plan anytime.
- 🆓 **Free and open source.** MIT licensed.
- 🔒 **Private.** Guava never sees your data.
- 🛡️ **Safe for your AI accounts.** No shared or proxied logins. Each AI runs in its official app, signed in as you.
- ✅ **Safe by default.** Shows every change first, never overwrites, and scans outside skills before installing.

## Start here
Paste this into any AI assistant:

```
Set me up by following the Start here steps in github.com/romeodiaz/guava-stack.
```

It asks a few questions, explains each step, and checks that everything works. Unsure? Say "use the defaults".

Each assistant follows its own guide: [Claude](assistants/claude.md) · [ChatGPT](assistants/chatgpt.md) · [Grok Bot](assistants/grok.md) · [Muse](assistants/muse.md).

**AI assistants:** first check `assistants/<your assistant>.md` for steps to skip or change. If there's no file for you, do what your platform supports and tell the owner what you skipped. Then follow [guava-hub/skills/guava-hub/SKILL.md](guava-hub/skills/guava-hub/SKILL.md) from step 1. It builds the hub, hands off to the router, offers founder-mode and wraps up.

**🧩 Just want one piece?** Each works on its own:

```
Install guava-hub from github.com/romeodiaz/guava-stack
```

```
Install guava-router from github.com/romeodiaz/guava-stack
```

```
Install founder-mode from github.com/romeodiaz/guava-stack
```

As Claude Code plugins: `claude plugin marketplace add romeodiaz/guava-stack`, then `/plugin install <name>@guava`.

**▶️ Try it:**
1. "Set me up with a Google Drive hub. I only pay for Claude."
2. "Import my existing instructions and skills into my guava-hub."
3. "Turn on founder-mode."
4. "Write this week's LinkedIn post in my voice."

## Make it yours
Every part is swappable. Your choices live in a short **guava-stack settings** section in your hub. Edit anything in your hub, from a model to a rule, and every assistant picks it up within 15 minutes, even in a chat that's already open. Typos get caught with a suggested fix. For bigger changes, say "change my setup".

**🗂️ Where your hub lives**

| Hub | Good if you |
|---|---|
| Notion | Want the easiest start. Works with every assistant, with a local copy for speed. |
| Google Drive | Use Google Workspace or Gmail |
| OneDrive / SharePoint | Use Microsoft 365 |
| Local Markdown / Obsidian | Want it on your computer only, such as for private client work. Code tab, Claude Code and Codex. |

**💬 Who you talk to**

On your computer, your assistant keeps a copy of your hub, so it starts instantly and passes work between Claude and ChatGPT for you. Everywhere else (your phone, the web, Grok Bot, Muse), it reads the same hub straight from Notion, so a chat's first reply takes a few seconds longer.

- **Claude or ChatGPT app** (web, desktop, phone): each new chat checks it's on the right model, or hands you a prompt for the right one.
- **Grok Bot or Muse**: cloud assistants that hand each job to the right AI, even from your phone.
- **Claude desktop app, Code tab** (Local sessions): Claude hands off work itself. No terminal needed.
- **Local models**: *coming soon*.

**👩‍🍳 head-chef and line-cook**

Split the work like a kitchen. One model for everything? Put it in both spots.

<!-- models:kitchen -->
<table>
<tr>
<td align="center" width="50%"><img src="assets/head-chef.png" width="120" alt="Pixel-art head chef"><br><strong>head-chef</strong><br><sub>Today's best: Claude Opus 5.5</sub></td>
<td align="center" width="50%"><img src="assets/line-cook.png" width="120" alt="Pixel-art line cook"><br><strong>line-cook</strong><br><sub>Today's best: GPT-6.1 Sol</sub></td>
</tr>
<tr>
<td>Orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems.</td>
<td>Bulk execution, coding, sub-agent tasks, worker threads, long-running jobs.</td>
</tr>
</table>
<!-- /models -->

Today's picks for the plans you pay for:

<!-- models:table style=simple -->
| You pay for | head-chef | line-cook |
|---|---|---|
| Claude and ChatGPT | Claude Opus 5.5 | GPT-6.1 Sol |
| ChatGPT only | GPT-6 Astra | GPT-6.1 Sol |
| Claude only | Claude Opus 5.5 | Claude Sonnet 5.5 |
| Local models on your own computer | *Coming soon* | *Coming soon* |
<!-- /models -->

Any model your plans can run works. Say "check for newer models" to swap in better ones as they come out.

## How to update
Say **"update guava-stack"**. It updates every piece and your hub, offers newer models, and shows the plan first. For one piece, say **"update guava-hub"**, **"update guava-router"** or **"update founder-mode"**. In the Claude desktop app, use a Local Code tab session. 📜 [Changelog](founder-mode/CHANGELOG.md)

## Your data stays yours
🔒 Guava collects nothing. Your details go only to your own hub, and your AI work only to the AI services you already use. Setup asks before every change.

<details>
<summary><strong>See exactly what setup touches</strong></summary>

- **Files edited:** a short block between `<!-- guava-stack:start -->` and `<!-- guava-stack:end -->` in `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`, only if the guava-hub plugin isn't installed in that tool or your hub is a local folder (or your AI tools' own instructions files). Each file is backed up first, and nothing outside the markers changes. The optional "Never skip the hub" step, and a local hub, back up `~/.claude/settings.json` and add only your hub's read-only tools or folder.
- **Start-up hook:** the guava-hub plugin adds a short "load my hub" note to each new Claude Code and Codex session. It changes nothing. Codex asks you once to approve its three start-up hooks.
- **Commands run:** only for your AI setup: `npm i -g @anthropic-ai/claude-code`, `npm i -g @openai/codex`, `claude auth login`, `codex login --device-auth`, the [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc) if the Code tab is your assistant, and a quick test prompt in each.
- **Files read:** only the instruction, skill or notes files you approve. Never your Claude or ChatGPT memories or chats.
- **Saved:** your hub, plus standing instructions in your assistant's memory or app instructions.
- **External services:** your hub's service (none for a local hub), your AI providers, and GitHub. Nothing goes to Guava, and the plugin fetches no remote instructions. [Privacy](https://workwithguava.com/privacy)

</details>

## What's inside
- 🧠 **[guava-hub](guava-hub/)**: hub setup for each [hub type](guava-hub/skills/guava-hub/backends/).
- 🔀 **[guava-router](guava-router/)**: model routing for each [AI setup](guava-router/skills/guava-router/setups.md).
- 🎤 **[founder-mode](founder-mode/)**: the rules and their [changelog](founder-mode/CHANGELOG.md).
- 🤖 **[assistants/](assistants/)**: what each assistant skips or changes.
- 🛠️ **Know agent files?** context ≈ USER.md + TOOLS.md. rules ≈ the rules in AGENTS.md or CLAUDE.md, shared by every assistant. skills = the `skills/` folder. Setup does BOOTSTRAP.md's job, once. No SOUL.md, IDENTITY.md, MEMORY.md or HEARTBEAT.md: each assistant keeps its own persona, memory and check-ins.

## Support
- ✉️ [romeo@workwithguava.com](mailto:romeo@workwithguava.com)
- 🔒 [Privacy](https://workwithguava.com/privacy)
- 👥 Want it for your whole team? [Book a call](https://workwithguava.com/talk)

## Credits
Adapted from [poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) in Cursor's pstack plugin, by poteto, from [Matt Pocock's skills](https://github.com/mattpocock/skills) and the [humanizer skill](https://github.com/blader/humanizer) by blader.

Built by Romeo Diaz to run Guava ([workwithguava.com](https://workwithguava.com)). Follow @romeodiazai on LinkedIn and X.

## License
MIT. Free to use, change and share. See [LICENSE](LICENSE).
