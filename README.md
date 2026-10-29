# guava-stack

Notion as the shared memory and workspace for Claude and ChatGPT, in their desktop apps and in Claude Code and Codex. Built on Notion's official setup guide for agents, [Set up Notion for your agent](https://developers.notion.com/prompts/setup).

## Start here
Paste this into the Claude or ChatGPT desktop app, or into Claude Code or Codex:

```
Follow the Start here steps in github.com/romeodiaz/guava-stack
```

You'll need a Claude or ChatGPT plan and Notion (the free plan is enough).

**AI assistants:** follow [skills/guava-stack/SKILL.md](skills/guava-stack/SKILL.md).

## What it does
Notion's guide does the setup: it connects Notion, makes your private Agent Operating Guide (where your things live, your preferences and a version history), gives every app the same custom instructions, offers a daily memory and setup check, and brings in the memories, documents and skills you already have.

guava-stack adds what Notion's guide leaves to each app: connecting Claude Code and Codex to Notion, saving the same custom instructions where they read them, and adding your other apps, so all four read the same Notion.

Then Guava's parts, each with your yes:
- **guava-hub:** a context page (who you are, your business, your voice) and a rules page, next to Notion's Skills library.
- **[founder-mode](skills/founder-mode/SKILL.md):** 16 working rules. Your AI does the safe work itself, checks the real result and asks before anything costly or permanent.
- **[guava-router](skills/guava-router/SKILL.md):** in Claude Code or Codex, the head-chef (Claude Opus 5.5) plans, writes and reviews, and the line-cook (GPT-6.1 Sol) does the bulk work and coding.
- **Starter skills** in Notion's Skills library: [workflow-review](skills/workflow-review/SKILL.md), [design-cook-off](skills/design-cook-off/SKILL.md), [humanizer-writing](https://github.com/blader/humanizer) and [ponytail-coding](https://github.com/DietrichGebert/ponytail).

## What it changes
- **In Notion:** what Notion's guide makes, plus the guava-hub pages, the skills you pick and a guava-stack settings section in your Agent Operating Guide, each with your yes.
- **On your computer:** the custom instructions at the end of `~/.claude/CLAUDE.md` and Codex's global `AGENTS.md` (in `~/.codex`), and a Notion connection in Claude Code or Codex if there isn't one yet.
- **In the desktop apps:** the custom instructions you paste into Claude's or ChatGPT's settings.

## Update and uninstall
Say **"update guava-stack"** or **"uninstall guava-stack"**. Each shows the change first and waits for your yes. Uninstalling removes the custom instructions from your computer and leaves everything in your Notion as it is.

## Credits
Built on Notion's [Set up Notion for your agent](https://developers.notion.com/prompts/setup). guava-stack isn't made or endorsed by Notion. Notion is a trademark of Notion Labs, Inc.

Built by Romeo Diaz ([workwithguava.com](https://workwithguava.com)).

## License
MIT. See [LICENSE](LICENSE).
