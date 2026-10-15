<p align="center"><img src="assets/logo.png" alt="Guava logo" width="120"></p>

# guava-stack: AI brain + router + rules

<p align="center"><a href="https://skills.sh/romeodiaz/guava-stack"><img src="https://skills.sh/b/romeodiaz/guava-stack" alt="skills.sh"></a></p>

**Free, open source, and yours to keep.**

Guava Stack keeps your business context, rules and skills in one place you already own, like Notion, Google Drive or OneDrive. Every AI assistant you use reads from that one place, on your computer, your laptop and your phone. Switch assistants or AI plans whenever you like, and nothing gets lost.

You don't need to code or open a terminal. Paste one line into the AI assistant you already use, and it walks you through the rest.

## Why people use it
- **Explain your business once.** No more re-introducing yourself to every AI app.
- **Use what you already have.** Claude, ChatGPT, Grok Bot, Muse and others, on the AI plans you already pay for. Nothing new to buy.
- **Take it everywhere.** The same assistant, context and rules on your desk, laptop and phone.
- **No lock-in.** Your stuff lives in your own account, not inside one AI company's app. Change your hub, your assistant or your AI plan anytime and keep everything.
- **Free and open source.** MIT licensed. Read every line, change anything, share it with anyone.
- **Private.** Guava never sees your data. It goes only to your own hub and the AI services you already use.
- **Safe by default.** Setup shows you each change before making it, never overwrites what you have, and scans skills from strangers before installing them.

## Start here
Paste this into your AI assistant:

```
Set me up by following the Start here steps in github.com/romeodiaz/guava-stack.
```

It asks a few simple questions, explains each step before doing it, and checks that everything works at the end. Not sure what to pick? Say "use the defaults" and it chooses a setup that works for most people.

**AI assistants:** first check `assistants/<your assistant>.md` for steps to skip or change. If there's no file for you, do what your platform supports and tell the owner what you skipped. Then follow [guava-hub/skills/guava-hub/SKILL.md](guava-hub/skills/guava-hub/SKILL.md) from step 1. It builds the hub, hands off to the router, offers founder-mode and wraps up.

## What you get
Three pieces that work together. Start with the hub; the other two are optional.

<table>
<tr>
<td align="center" width="33%"><a href="guava-hub/"><img src="assets/brain-hub.png" width="120" alt="Pixel-art brain"></a><br><strong>AI brain</strong><br><sub>guava-hub</sub></td>
<td align="center" width="33%"><a href="guava-router/"><img src="assets/model-router.png" width="120" alt="Pixel-art router"></a><br><strong>Router</strong><br><sub>guava-router (optional)</sub></td>
<td align="center" width="33%"><a href="founder-mode/"><img src="assets/founder-mode.png" width="120" alt="Pixel-art speaker at a microphone"></a><br><strong>Rules</strong><br><sub>founder-mode (optional)</sub></td>
</tr>
</table>

1. **[A shared hub](guava-hub/)**: one home for your profile, your rules for how AI should work for you, and your skills (step-by-step instructions your AI can reuse). Every assistant you connect reads from it.
2. **[Model routing](guava-router/)** (optional): sends each job to the AI model that's best at it, using the plans you already have.
3. **[founder-mode](founder-mode/)** (optional): 27 working rules so your AI works like a thoughtful teammate. It handles the safe work on its own, writes like a human instead of a robot, and always checks with you before anything that could cost you money or can't be undone.

## Make it yours
Every part is swappable. Pick what fits you today and change it later by telling your assistant.

**Where your hub lives**

| Hub | Good if you |
|---|---|
| Notion | Want the easiest start. Works with every assistant here. |
| Google Drive | Use Google Workspace or Gmail |
| OneDrive / SharePoint | Use Microsoft 365 |
| Obsidian / local Markdown | Coming soon |

**Which assistant you talk to**
- **The Claude or ChatGPT app you already use**, on web, desktop or phone. Setup adds a few instructions so each new chat checks it's on the right model, and if not, hands you a ready-to-paste prompt for the right one.
- **Grok Bot or Muse**, assistants that run in the cloud and hand each job to the right AI for you, even from your phone.
- **The Claude desktop app's Code tab**, if you want Claude to hand work off for you without a separate assistant. No terminal needed.
- **Cursor and other tools**: coming soon.

**One AI model or two**

Keep it simple with one do-it-all model, or split the work like a kitchen:

<table>
<tr>
<td align="center" width="50%"><img src="assets/head-chef.png" width="120" alt="Pixel-art head chef"><br><strong>Head chef</strong><br><sub>Today's best: Claude Opus 5.5</sub></td>
<td align="center" width="50%"><img src="assets/line-cook.png" width="120" alt="Pixel-art line cook"><br><strong>Line cook</strong><br><sub>Today's best: GPT-6.1 Sol</sub></td>
</tr>
<tr>
<td>Orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems.</td>
<td>Bulk execution, coding, sub-agent tasks, worker threads, long-running jobs.</td>
</tr>
</table>

The plans you pay for decide who's in the kitchen:

| You pay for | Head chef | Line cook |
|---|---|---|
| Claude and ChatGPT | Claude Opus 5.5 | GPT-6.1 Sol |
| ChatGPT only | GPT-6 Astra | GPT-6.1 Sol |
| Claude only | Claude Opus 5.5 | Claude Sonnet 5.5 |
| Cursor, Devin, Droid, Amp and others | Coming soon | Coming soon |

AI models change fast. When a better one comes out, tell your assistant to swap it in. Your hub stays the same.

**On every device.** Your hub and instructions live in your own accounts, not on one computer, so everything follows you. The Claude and ChatGPT phone apps pick up your hub automatically, Grok Bot and Muse answer from your phone, and the Claude phone app can open your Code tab sessions while your computer is on.

## How to use it
Pick the assistant you use.

<details>
<summary><strong>Claude</strong></summary>

Paste this. Your assistant follows the [Claude guide](assistants/claude.md) automatically.

```
Set me up by following the Start here steps in github.com/romeodiaz/guava-stack.
```

</details>

<details>
<summary><strong>ChatGPT Dots</strong></summary>

Paste this. Your assistant follows the [ChatGPT guide](assistants/chatgpt.md) automatically.

```
Set me up by following the Start here steps in github.com/romeodiaz/guava-stack.
```

</details>

<details>
<summary><strong>Grok Bot</strong></summary>

Install the [AI Context & Skills Hub template](https://x.ai/bot/rAhhI5cD__CnejfWqf3wH) in one click. It sets everything up with the recommended choices. Want a different hub or AI plan? Paste the Start here line instead. The Grok Bot and Cursor plugin marketplace listing is pending review.

</details>

<details>
<summary><strong>Meta Muse Bot</strong></summary>

Paste this. Your assistant follows the [Muse Bot guide](assistants/muse.md) automatically.

```
Set me up by following the Start here steps in github.com/romeodiaz/guava-stack.
```

</details>

<details>
<summary><strong>Any other AI assistant</strong></summary>

Paste this:

```
Set me up by following the Start here steps in github.com/romeodiaz/guava-stack.
```

Just want the founder-mode rules?

```
Install founder-mode from github.com/romeodiaz/guava-stack
```

</details>

That's it. Try one of these to see it work:
1. "Set me up with a Google Drive hub. I only pay for Claude."
2. "Import my existing instructions and skills into my AI Context Hub."
3. "Turn on founder-mode."
4. "Write this week's LinkedIn post in my voice."

## How to update
Tell your assistant **"update founder-mode"**. It checks for a newer version, updates only if there is one, and tells you what changed. See the [changelog](founder-mode/CHANGELOG.md).

## Your data stays yours
Guava collects nothing. Your profile and business details go only to your own hub, and your AI work goes only to the AI services you already use, under your own plans. Setup asks for a yes before every change.

<details>
<summary><strong>See exactly what setup touches</strong></summary>

- **Files edited:** appends a short section to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, or the instructions file of the tools in your AI setup (never replaces what's there). The router's optional "Never skip the hub" step backs up `~/.claude/settings.json` and adds only your hub's read-only tools to its permissions.
- **Commands run:** only for the tools your AI setup uses: `npm i -g @anthropic-ai/claude-code`, `npm i -g @openai/codex`, `claude auth login`, `codex login --device-auth`, the [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc) if the Claude desktop app's Code tab is your assistant, a quick test prompt in each, and optionally [Cisco Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner) on third-party skills.
- **Files read:** only the local instruction, skill or notes files you approve. It never reads your Claude or ChatGPT memories or chats; you paste or export what you want.
- **Saved:** your hub (pages and a Skills database in Notion, or documents in Google Drive or OneDrive/SharePoint), and standing instructions in your assistant's memory or your Claude and ChatGPT app instructions.
- **External services:** your hub's service (Notion, Google or Microsoft), the AI providers in your setup (Anthropic for Claude, OpenAI for ChatGPT and Codex), GitHub (this repo). Nothing is sent to Guava, and the plugin fetches no remote instructions. See [Privacy](https://workwithguava.com/privacy).

</details>

## What's inside
For the curious:
- **[guava-hub](guava-hub/)**: hub setup, with steps for each [hub type](guava-hub/skills/guava-hub/backends/).
- **[guava-router](guava-router/)**: model routing, with details for each [AI setup](guava-router/skills/guava-router/setups.md).
- **[founder-mode](founder-mode/)**: the rules and their [changelog](founder-mode/CHANGELOG.md).
- **[assistants/](assistants/)**: notes for each assistant on what to skip or change.

## Support & privacy
- Support: [romeo@workwithguava.com](mailto:romeo@workwithguava.com)
- Privacy: https://workwithguava.com/privacy. Guava collects no data; everything stays in your own hub, computer and AI accounts.

## Want it for your whole team?
For a multiplayer version for your team or org, book a call: https://workwithguava.com/talk

## Credits
Adapted from [poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) in Cursor's pstack plugin, by poteto, from [Matt Pocock's skills](https://github.com/mattpocock/skills) and the [humanizer skill](https://github.com/blader/humanizer) by blader.

Built by Romeo Diaz to run Guava ([workwithguava.com](https://workwithguava.com)). Follow @romeodiazai on LinkedIn and X.

## License
MIT. Free to use, change and share. See [LICENSE](LICENSE).
