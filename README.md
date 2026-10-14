# Owner Mode

**23 working rules so your AI assistant works like it owns the result.** It handles the safe work on its own and always checks with you before anything that could cost you money or can't be undone.

For business owners and solo operators. (`guava-mode` is just the technical name for this repo.)

## Start here
**People:** paste this into your AI assistant: "Set me up by following the Start here steps in github.com/romeodiaz/guava-mode."

**AI assistants:** first check `assistants/<your assistant>.md` for steps to skip or change. If there's no file for you, do what your platform supports and tell the owner what you skipped.

1. Say in one line: I'll set up a shared AI Context & Skills Hub in Notion so your AI assistants share the same context and skills, and route work to Claude Opus 5.5 and GPT-6.1 Sol.
2. Ask one at a time, and save the answers:
   - What should I call you, and what's your business and audience in a sentence or two?
   - Is Notion connected here? If not, help connect it.
   - Do you have a Claude plan (Pro or Max) and a ChatGPT plan (Plus or Pro)?
3. Save these standing instructions to your memory, custom instructions or system prompt:
   - Model routing: Claude Opus 5.5 High via Claude CLI for orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems; GPT-6.1 Sol High via Codex CLI for bulk execution, coding, sub-agent tasks, worker threads, computer use and long-running jobs.
   - Before substantive work, load the owner's Agent Rules, Profile & Context and enabled Notion skills from their Notion AI Context Hub, and treat Notion as the source of truth.
   - When the owner says "update Owner Mode", follow owner-mode-rules.md from github.com/romeodiaz/guava-mode.
4. Follow [hub-setup.md](https://raw.githubusercontent.com/romeodiaz/guava-mode/main/hub-setup.md).
5. Offer Owner Mode: "Ready to turn on Owner Mode? Your AI assistant works like it owns the result: it handles the safe work on its own and always checks with you before anything that could cost you money or can't be undone. Or would you like to see the full list of rules first?" If they want the list, show the rules, then ask again. If yes, follow [owner-mode-rules.md](https://raw.githubusercontent.com/romeodiaz/guava-mode/main/owner-mode-rules.md). If not, tell them they can say "turn on Owner Mode" anytime.

## What's inside
- **Owner Mode rules**: [owner-mode-rules.md](owner-mode-rules.md)
- **AI Context & Skills Hub (Notion)**: one shared place where Grok Bot, Claude and ChatGPT read your context, rules and skills.
- **Model Router**: Claude Opus 5.5 for thinking work, GPT-6.1 Sol for doing work. Setup guide: [hub-setup.md](hub-setup.md)

## How to use it
- **Grok Bot**: install the Owner Mode template, which sets everything up for you.
- **Any other AI assistant**: paste the line under Start here, or "Install Owner Mode from github.com/romeodiaz/guava-mode" for the rules only.

## How to update
Tell your assistant: **"update Owner Mode from github.com/romeodiaz/guava-mode"**. It checks the version number and only updates if there's something newer, then tells you what changed.

## Want it for your whole team?
For a multiplayer version for your team or org, book a call: https://workwithguava.com/talk

## Credits
Adapted from [poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) in Cursor's pstack plugin, by poteto.
Two rules adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills).
Rule 17 uses the [humanizer skill](https://github.com/blader/humanizer) by blader.

By Romeo Diaz, Guava ([workwithguava.com](https://workwithguava.com)). Follow @romeodiazai on LinkedIn and X.

## License
MIT. See [LICENSE](LICENSE).
