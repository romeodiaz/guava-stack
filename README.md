<p align="center"><img src="assets/logo.png" alt="Guava logo" width="120"></p>

# Guava Stack: AI Context & Skills Hub, Model Router and founder-mode

<p align="center"><a href="https://skills.sh/romeodiaz/guava-stack"><img src="https://skills.sh/b/romeodiaz/guava-stack" alt="skills.sh"></a></p>

The setup I use every day to run Guava, so all my AI assistants share one brain and work like humans do.

For business owners and solo operators. The stack has three pieces that live together in this repo:

| Piece | What it does | Setup |
|---|---|---|
| **[guava-hub](guava-hub/)** | A shared AI Context & Skills Hub, so all your AI assistants share your context, rules and skills. Notion by default, or Google Drive or OneDrive/SharePoint. | [context-skills-hub-setup](guava-hub/skills/context-skills-hub-setup/SKILL.md) |
| **[guava-router](guava-router/)** | Routes hard thinking to a planner model and heavy lifting to a builder model, through their CLIs or right in your Claude and ChatGPT apps, on the plans you already pay for. Claude Opus 5.5 + GPT-6.1 Sol by default. | [model-router-setup](guava-router/skills/model-router-setup/SKILL.md) |
| **[founder-mode](founder-mode/)** (optional) | 27 working rules so your AI assistant works like humans do. It handles the safe work on its own and always checks with you before anything that could cost you money or can't be undone. | [founder-mode-rules](founder-mode/skills/founder-mode-rules/SKILL.md) |

Setup starts with the hub, then the router, then offers founder-mode. You can turn on founder-mode at the end of setup or anytime later.

## Pick your setup
Three choices, each with a default. Say "use the defaults" and you get a Notion hub, Grok Bot or Muse as your assistant, and Claude Opus 5.5 planning with GPT-6.1 Sol doing the work.

**Where your hub lives**

| Hub | Best for |
|---|---|
| **Notion** (default) | Most owners. Every assistant here connects to it. |
| Google Drive | Owners on Google Workspace or Gmail |
| OneDrive / SharePoint | Owners on Microsoft 365 |
| Obsidian / local Markdown | Coming soon |

**Your day-to-day assistant:** Grok Bot or Muse by default, since they run both CLIs on their own computer and route each job for you. Don't have or want them? Use your normal Claude or ChatGPT app on web, desktop or mobile: setup adds instructions so every new chat first checks whether your request is planning or execution, and if it's on the wrong model, hands you a ready-to-paste prompt for the right one. Have both plans but don't want Grok Bot or Muse? The Claude desktop app's Code tab can be your assistant, no terminal needed: Claude plans, and OpenAI's [Codex plugin for Claude Code](https://github.com/openai/codex-plugin-cc) hands execution to Codex. Only pay for Claude? The Code tab's built-in `opusplan` mode plans on Opus and builds on Sonnet for you. Third-party tools like Cursor are coming soon. See [How to use it](#how-to-use-it).

**Your AI models:** two by default, run like a kitchen. Your strongest model is the **head chef**: it plans, researches, writes and tastes every plate at the pass before it goes out. Your faster, cheaper model is the **line cook**: it does the prep and the cooking, from bulk tasks and coding to long jobs. Your plans decide the pair. Prefer one do-it-all model? Pick it and skip routing; the hub and founder-mode work the same.

| You pay for | Planner + reviewer | Builder |
|---|---|---|
| **Claude + ChatGPT** (default) | Claude Opus 5.5 (High) | GPT-6.1 Sol (High) |
| ChatGPT only | Astra (High) | GPT-6.1 Sol (High) |
| Claude only | Claude Opus 5.5 (High) | Claude Sonnet 5.5 (High) |
| Third-party tools (Cursor, Devin, Droid, Amp and others) | Coming soon | Coming soon |

Setup saves your choices in your hub, so every assistant follows the same setup. Change any of them later by telling your assistant.

**Every setup works on your computer, laptop and phone.** Your hub and instructions live in your own accounts, not on one device. Grok Bot and Muse run in the cloud, so you can message them from your phone. The Claude and ChatGPT phone apps pick up your hub and routing instructions automatically. And with Remote Control, the Claude phone app opens your Code tab sessions while your computer is on.

## Why install it
**Every AI tool starts from scratch.** You explain your business again in each one, and switching tools means starting over.

**The fix:** one shared brain for your AI context. Your profile, rules and skills live in your own Notion, Google Drive or OneDrive/SharePoint, and Grok Bot, Claude, ChatGPT and other tools all read from it.

**Your AI setup is stuck on one device.**

**The fix:** your hub and instructions live in your own accounts, so the same assistant, context and routing go with you from your desk to your laptop to your phone.

**You're paying for AI plans you don't fully use.**

**The fix:** hard thinking goes to your best planner model and heavy lifting goes to a fast builder model, through the plans you already pay for. With Claude and ChatGPT, that's Claude Opus 5.5 and GPT-6.1 Sol.

**Skills from strangers can be risky.**

**The fix:** third-party skills get scanned with [Cisco Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner) before they're installed, and you see anything it flags.

**AI writing sounds like AI slop.**

**The fix:** founder-mode checks final copy against the [humanizer's principles](https://github.com/blader/humanizer), so posts and emails lose the usual AI writing tells.

**Setup tools can overwrite your stuff.**

**The fix:** nothing gets wiped. Your existing instructions and files are only added to, and the assistant shows you each change before making it.

## Zero lock-in
Your context and skills live in your own hub, not inside one AI company's app, and the hub itself can move: Notion, Google Drive and OneDrive/SharePoint all hold the same three parts. A neutral assistant like Grok Bot or Muse drives whichever AI plans you have, so each job goes to the best model. Switch or drop any of them anytime and you keep everything: just connect the new one to your hub.

## Start here
**People:** paste this into your AI assistant:

```
Set me up by following the Start here steps in github.com/romeodiaz/guava-stack.
```

**AI assistants:** first check `assistants/<your assistant>.md` for steps to skip or change. If there's no file for you, do what your platform supports and tell the owner what you skipped. Then follow [guava-hub/skills/context-skills-hub-setup/SKILL.md](guava-hub/skills/context-skills-hub-setup/SKILL.md) from step 1. It builds the hub, hands off to the router, offers founder-mode and wraps up.

## What's inside
- **[guava-hub](guava-hub/)**: one shared place where all your AI assistants read your context, rules and skills, with setup steps for each [hub backend](guava-hub/skills/context-skills-hub-setup/backends/).
- **[guava-router](guava-router/)**: a planner model for thinking work and a builder model for execution work, with details for each [AI setup](guava-router/skills/model-router-setup/setups.md).
- **[founder-mode](founder-mode/)**: the founder-mode rules and their [changelog](founder-mode/CHANGELOG.md).
- **[assistants/](assistants/)**: per-assistant notes on what to skip or change.

## How to use it
Pick your assistant.

<details>
<summary><strong>Grok Bot</strong></summary>

1-Click install the [AI Context & Skills Hub template](https://x.ai/bot/rAhhI5cD__CnejfWqf3wH), which sets everything up for you with the defaults. For another hub or AI setup, paste the Start here line instead. The Grok Bot and Cursor plugin marketplace listing is pending review.

</details>

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

For the rules only:

```
Install founder-mode from github.com/romeodiaz/guava-stack
```

</details>

That's it, you're ready. Try one of the example prompts below to see it work.

## How to update
Tell your assistant **"update founder-mode"**. It checks the version number, only updates if there's something newer, and tells you what changed. See [founder-mode/CHANGELOG.md](founder-mode/CHANGELOG.md).

## What this changes
Setup asks for a yes before each of these:

<details>
<summary><strong>See exactly what setup touches</strong></summary>

- **Files edited:** appends a short section to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md`, or the instructions file of the tools in your AI setup (never replaces what's there). The router's optional "Never skip the hub" step backs up `~/.claude/settings.json` and adds only your hub's read-only tools to its permissions.
- **Commands run:** only for the tools your AI setup uses: `npm i -g @anthropic-ai/claude-code`, `npm i -g @openai/codex`, `claude auth login`, `codex login --device-auth`, the Codex plugin for Claude Code if the Claude desktop app's Code tab is your assistant, a quick test prompt in each, and optionally Cisco Skill Scanner on third-party skills.
- **Files read:** only the local instruction, skill or notes files you approve. It never reads your Claude or ChatGPT memories or chats; you paste or export what you want.
- **Saved:** your hub (pages and a Skills database in Notion, or documents in Google Drive or OneDrive/SharePoint), and standing instructions in your assistant's memory or your Claude and ChatGPT app instructions.
- **External services:** your hub's service (Notion, Google or Microsoft), the AI providers in your setup (Anthropic for Claude, OpenAI for ChatGPT and Codex), GitHub (this repo). Your profile and business details go only to your own hub, and routed work goes to those providers under your own plans. Nothing is sent to Guava, and the plugin fetches no remote instructions. See [Privacy](https://workwithguava.com/privacy).

</details>

## Example prompts
1. "Set me up by following the Start here steps in the Guava Stack."
2. "Set me up with a Google Drive hub. I only pay for Claude."
3. "Turn on founder-mode."
4. "Import my existing CLAUDE.md and skills into my AI Context Hub."

## Support & privacy
- Support: [romeo@workwithguava.com](mailto:romeo@workwithguava.com)
- Privacy: https://workwithguava.com/privacy. Guava collects no data; everything stays in your own hub, computer and AI accounts.

## Want it for your whole team?
For a multiplayer version for your team or org, book a call: https://workwithguava.com/talk

## Credits
Adapted from [poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) in Cursor's pstack plugin, by poteto, from [Matt Pocock's skills](https://github.com/mattpocock/skills) and the [humanizer skill](https://github.com/blader/humanizer) by blader.

By Romeo Diaz, Guava ([workwithguava.com](https://workwithguava.com)). Follow @romeodiazai on LinkedIn and X.

## License
MIT. See [LICENSE](LICENSE).
