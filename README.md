# guava-stack

Notion as the shared memory and workspace for Claude and ChatGPT, in their desktop apps and in Claude Code and Codex. Built on Notion's official setup guide for agents, [Set up Notion for your agent](https://developers.notion.com/prompts/setup).

## Start here
Paste this into the Claude or ChatGPT desktop app, or into Claude Code or Codex:

```
Follow the Start here steps in github.com/romeodiaz/guava-stack
```

You'll need a Claude or ChatGPT plan and Notion. Notion's free plan works for one person. A team needs a paid Notion plan, since a Free workspace with more than one member stops at 1,000 blocks for good.

**AI assistants:** follow [skills/guava-stack/SKILL.md](skills/guava-stack/SKILL.md).

## What it does
Notion's guide does the setup: it connects Notion, makes your private Agent Operating Guide (where your things live, your preferences and a version history), gives every app the same custom instructions, offers a daily memory and setup check, and brings in the memories, documents and skills you already have.

guava-stack adds what Notion's guide leaves to each app: connecting Claude Code and Codex to Notion, saving the same custom instructions where they read them, and adding your other apps, so all four read the same Notion.

Then Guava's parts, each with your yes:
- **guava-hub:** one page in your sidebar holding your context (who you are, your business, your voice), your rules, Notion's Skills library and your Tasks.
- **Your workspace:** your Tasks, Projects, Meetings and Docs in Notion. It uses the ones you have and makes Notion's own for any that are missing, so every app files work where you keep it. Optionally, your AI logs the bigger work you'd track as tasks, with each task's ID in commits, PRs and hand-offs.
- **Routines:** the scheduled tasks in your Claude and ChatGPT apps, recorded in Notion's Skills library next to the skill each one runs: when it runs, where, what you approved ahead of time and when it last ran. Say "check my routines" anytime.
- **[founder-mode](skills/founder-mode/SKILL.md):** 16 working rules. Your AI does the safe work itself, checks the real result and asks before anything costly or permanent.
- **Starter skills** in Notion's Skills library:
  1. [workflow-review](skills/workflow-review/SKILL.md): ranks which of your workflows are worth automating, as a report that stays on your computer.
  2. [design-cook-off](skills/design-cook-off/SKILL.md): for a page people judge by its look, your AI builds it twice with two design skills, and you pick one.
  3. [humanizer-writing](https://github.com/blader/humanizer): so anything your AI writes doesn't sound like AI.
  4. [ponytail-coding](https://github.com/DietrichGebert/ponytail): your AI writes the least code that does the whole job.
  5. [oracle-council](skills/oracle-council/SKILL.md): three top AIs from three companies answer one hard question at once, merged into one verdict. Gemini 4 Argon runs on OpenRouter, billed per use.
  6. [guava-router](skills/guava-router/SKILL.md): in Claude Code or Codex, the head-chef (Claude Opus 5.5) plans, writes and reviews, and the line-cook (GPT-6.1 Sol) does the bulk work and coding.

## What it changes
- **In Notion:** what Notion's guide makes, plus the guava-hub pages, any Tasks, Projects, Meetings or Docs database you're missing, the Routines columns and view in the Skills library, the skills you pick, and a few preference lines and a guava-stack settings section in your Agent Operating Guide, each with your yes.
- **On your computer:** the custom instructions at the end of `~/.claude/CLAUDE.md` and Codex's global `AGENTS.md` (in `~/.codex`), a Notion connection in Claude Code or Codex if there isn't one yet, and with oracle-council, the OpenRouter key its browser sign-in makes, in `~/.config/guava-stack/openrouter-key`.
- **In the desktop apps:** the custom instructions you paste into Claude's or ChatGPT's settings.

## Update and uninstall
Say **"update guava-stack"** or **"uninstall guava-stack"**. Each shows the change first and waits for your yes. Uninstalling removes the custom instructions from your computer and leaves everything in your Notion as it is.

## For teams
Want it for your whole team? Guava sets up an Enterprise version for teams and companies: one shared setup in Notion, with everyone's assistants on the same rules and skills. Not on Notion? Guava also builds custom guava-stacks on Microsoft 365 (SharePoint and OneDrive), Google Workspace (Google Drive), Obsidian or your own private AWS or Azure VPC. [Book a call](https://workwithguava.com/talk).

## Credits
Built on Notion's [Set up Notion for your agent](https://developers.notion.com/prompts/setup). guava-stack isn't made or endorsed by Notion. Notion is a trademark of Notion Labs, Inc.

Built by Romeo Diaz ([workwithguava.com](https://workwithguava.com)).

## License
MIT. See [LICENSE](LICENSE).
