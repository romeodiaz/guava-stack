# Owner Mode

**22 working rules so your AI assistant works like it owns the result.** It handles the safe work on its own and always checks with you before anything that could cost you money or can't be undone.

For business owners and solo operators. (`guava-mode` is just the technical name for this repo.)

## Start here
Any AI assistant can set this up by following [START.md](START.md). Platform notes live in `assistants/<name>/ADAPTER.md`.

## What's inside
- **Owner Mode rules**: [owner-mode/RULES.md](owner-mode/RULES.md)
- **AI Context & Skills Hub (Notion)**: one shared place where Grok Bot, Claude and ChatGPT read your context, rules and skills.
- **Model Router**: Claude Opus 5.5 for thinking work, GPT-6.1 Sol for doing work. Setup guide: [hub-setup/SETUP.md](hub-setup/SETUP.md)

## How to use it
- **Grok Bot**: install the Owner Mode template, which sets everything up for you.
- **Any other AI assistant**: copy the prompt in [owner-mode/PROMPT.md](owner-mode/PROMPT.md) and paste it in.

## How to update
Tell your assistant: **"update Owner Mode from github.com/romeodiaz/guava-mode"**. It checks the version number and only updates if there's something newer, then tells you what changed. See [CHANGELOG.md](CHANGELOG.md).

## Want it for your whole team?
For a multiplayer version for your team or org, book a call: https://workwithguava.com/talk

## Credits
Adapted from poteto mode in Cursor's pstack plugin, by poteto.

By Romeo Diaz, Guava ([workwithguava.com](https://workwithguava.com)). Follow @romeodiazai on LinkedIn and X.

## License
MIT. See [LICENSE](LICENSE).
