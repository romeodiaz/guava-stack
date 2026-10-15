<p align="center"><img src="assets/logo.png" alt="Guava logo" width="120"></p>

# Guava Stack: AI Context & Skills Hub, Model Router and founder-mode

<p align="center"><a href="https://skills.sh/romeodiaz/guava-stack"><img src="https://skills.sh/b/romeodiaz/guava-stack" alt="skills.sh"></a></p>

The setup I use every day to run Guava, so all my AI assistants share one brain and work like humans do.

For business owners and solo operators. The stack has three pieces that live together in this repo:

| Piece | What it does | Setup |
|---|---|---|
| **[guava-hub](guava-hub/)** | A shared AI Context & Skills Hub in Notion, so Grok Bot, Claude and ChatGPT share your context, rules and skills. | [context-skills-hub-setup](guava-hub/skills/context-skills-hub-setup/SKILL.md) |
| **[guava-router](guava-router/)** | Routes hard thinking to Claude Opus 5.5 and heavy lifting to GPT-6.1 Sol through their CLIs, on the plans you already pay for. | [model-router-setup](guava-router/skills/model-router-setup/SKILL.md) |
| **[founder-mode](founder-mode/)** (optional) | 26 working rules so your AI assistant works like humans do. It handles the safe work on its own and always checks with you before anything that could cost you money or can't be undone. | [founder-mode-rules](founder-mode/skills/founder-mode-rules/SKILL.md) |

Setup starts with the hub, then the router, then offers founder-mode. You can turn on founder-mode at the end of setup or anytime later.

## Why install it
**Every AI tool starts from scratch.** You explain your business again in each one, and switching tools means starting over.

**The fix:** one shared brain for your AI context. Your profile, rules and skills live in your own Notion, and Grok Bot, Claude, ChatGPT and other tools all read from it.

**You're paying for AI plans you don't fully use.**

**The fix:** hard thinking goes to Claude Opus 5.5 and heavy lifting goes to GPT-6.1 Sol, through the Claude and ChatGPT plans you already pay for.

**Skills from strangers can be risky.**

**The fix:** third-party skills get scanned with [Cisco Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner) before they're installed, and you see anything it flags.

**AI writing sounds like AI slop.**

**The fix:** founder-mode checks final copy against the [humanizer's principles](https://github.com/blader/humanizer), so posts and emails lose the usual AI writing tells.

**Setup tools can overwrite your stuff.**

**The fix:** nothing gets wiped. Your existing instructions and files are only added to, and the assistant shows you each change before making it.

## Zero lock-in
Your context and skills live in your own Notion, not inside one AI company's app. A neutral assistant like Grok Bot or Muse drives both your Claude and ChatGPT plans, so each job goes to the best model. Switch or drop any of them anytime and you keep everything: just connect the new one to your hub.

## Start here
**People:** paste this into your AI assistant:

```
Set me up by following the Start here steps in github.com/romeodiaz/guava-stack.
```

**AI assistants:** first check `assistants/<your assistant>.md` for steps to skip or change. If there's no file for you, do what your platform supports and tell the owner what you skipped. Then follow [guava-hub/skills/context-skills-hub-setup/SKILL.md](guava-hub/skills/context-skills-hub-setup/SKILL.md) from step 1. It builds the hub, hands off to the router, offers founder-mode and wraps up.

## What's inside
- **[guava-hub](guava-hub/)**: one shared place in Notion where Grok Bot, Claude and ChatGPT read your context, rules and skills.
- **[guava-router](guava-router/)**: Claude Opus 5.5 for thinking work, GPT-6.1 Sol for execution work.
- **[founder-mode](founder-mode/)**: the founder-mode rules and their [changelog](founder-mode/CHANGELOG.md).
- **[assistants/](assistants/)**: per-assistant notes on what to skip or change.

## How to use it
Pick your assistant.

<details>
<summary><strong>Grok Bot</strong></summary>

1-Click install the [AI Context & Skills Hub template](https://x.ai/bot/rAhhI5cD__CnejfWqf3wH), which sets everything up for you. The Grok Bot and Cursor plugin marketplace listing is pending review.

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

- **Files edited:** appends a short section to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` (never replaces what's there). The router's optional "Never skip Notion" step backs up `~/.claude/settings.json` and adds four read-only Notion tools to `permissions.allow`.
- **Commands run:** `npm i -g @anthropic-ai/claude-code`, `npm i -g @openai/codex`, `claude auth login`, `codex login --device-auth`, a quick test prompt in each, and optionally Cisco Skill Scanner on third-party skills.
- **Files read:** only the local instruction, skill or notes files you approve. It never reads your Claude or ChatGPT memories or chats; you paste or export what you want.
- **Saved:** pages and a Skills database in your Notion, and standing instructions in your assistant's memory.
- **External services:** Notion, Anthropic (Claude Code), OpenAI (Codex), GitHub (this repo). Your profile and business details go only to your own Notion, and routed work goes to Anthropic or OpenAI under your own plans. Nothing is sent to Guava, and the plugin fetches no remote instructions. See [Privacy](https://workwithguava.com/privacy).

</details>

## Example prompts
1. "Set me up by following the Start here steps in the Guava Stack."
2. "Turn on founder-mode."
3. "Import my existing CLAUDE.md and skills into my AI Context Hub."

## Support & privacy
- Support: [romeo@workwithguava.com](mailto:romeo@workwithguava.com)
- Privacy: https://workwithguava.com/privacy. Guava collects no data; everything stays in your own Notion, computer and AI accounts.

## Want it for your whole team?
For a multiplayer version for your team or org, book a call: https://workwithguava.com/talk

## Credits
Adapted from [poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) in Cursor's pstack plugin, by poteto, from [Matt Pocock's skills](https://github.com/mattpocock/skills) and the [humanizer skill](https://github.com/blader/humanizer) by blader.

By Romeo Diaz, Guava ([workwithguava.com](https://workwithguava.com)). Follow @romeodiazai on LinkedIn and X.

## License
MIT. See [LICENSE](LICENSE).
