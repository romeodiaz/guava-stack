<p align="center"><img src="assets/logo.png" alt="Guava logo" width="120"></p>

# AI Context & Skills Hub + Model Router, with optional Owner Mode

For business owners and solo operators. Setup happens in two steps:

1. **AI Context & Skills Hub and Model Router.** Sets up a shared AI Context & Skills Hub in Notion so Grok Bot, Claude and ChatGPT share your context and skills, and routes work to Claude Opus 5.5 and GPT-6.1 Sol through their CLIs.
2. **Owner Mode (optional).** 23 working rules so your AI assistant works like it owns the result. It handles the safe work on its own and always checks with you before anything that could cost you money or can't be undone. You can turn it on at the end of setup or anytime later.

## Start here
**People:** paste this into your AI assistant: "Set me up by following the Start here steps in github.com/romeodiaz/guava-mode."

**AI assistants:** first check `assistants/<your assistant>.md` for steps to skip or change. If there's no file for you, do what your platform supports and tell the owner what you skipped.

1. Say in one line: I'll set up a shared AI Context & Skills Hub in Notion so your AI assistants share the same context and skills, and route work to Claude Opus 5.5 and GPT-6.1 Sol.
2. Ask one at a time, and save the answers:
   - What should I call you, and what's your business and audience in a sentence or two?
   - Is Notion connected here? If not, help connect it.
   - Do you have a Claude plan (Pro or Max) and a ChatGPT plan (Plus or Pro)?
3. Show the owner these standing instructions and, once they say yes, save them to your memory, custom instructions or system prompt (to shared memory across all the owner's assistants if your platform has it):
   - Model routing: Claude Opus 5.5 High via Claude CLI for orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems; GPT-6.1 Sol High via Codex CLI for bulk execution, coding, sub-agent tasks, worker threads and long-running jobs; browser and desktop tasks stay with your own computer tools; if either CLI fails, do the task yourself and say so; when a skill defines how it runs, follow the skill and use routing only for work it leaves open.
   - Before substantive work, load the owner's Agent Rules, Profile & Context and enabled Notion skills from their Notion AI Context Hub, and treat Notion as the source of truth.
   - When the owner says "update Owner Mode", follow skills/owner-mode/SKILL.md from github.com/romeodiaz/guava-mode.
4. Follow [skills/hub-setup/SKILL.md](skills/hub-setup/SKILL.md).
5. Offer Owner Mode: "Ready to turn on Owner Mode? Your AI assistant works like it owns the result: it handles the safe work on its own and always checks with you before anything that could cost you money or can't be undone. Or would you like to see the full list of rules first?" If they want the list, show the rules, then ask again. If yes, follow [skills/owner-mode/SKILL.md](skills/owner-mode/SKILL.md). If not, tell them they can say "turn on Owner Mode" anytime.

## What's inside
- **AI Context & Skills Hub (Notion)**: one shared place where Grok Bot, Claude and ChatGPT read your context, rules and skills.
- **Model Router**: Claude Opus 5.5 for thinking work, GPT-6.1 Sol for execution work. Setup guide: [skills/hub-setup/SKILL.md](skills/hub-setup/SKILL.md)
- **Owner Mode rules**: [skills/owner-mode/SKILL.md](skills/owner-mode/SKILL.md)

## How to use it
- **Grok Bot**: install the [AI Context & Skills Hub template](https://x.ai/bot/rAhhI5cD__CnejfWqf3wH), which sets everything up for you.
- **Claude Code**: `/plugin marketplace add romeodiaz/guava-mode`, then `/plugin install guava-mode@guava`.
- **Grok Bot and Cursor plugin marketplace**: listing pending review.
- **Any other AI assistant**: paste the line under Start here, or "Install Owner Mode from github.com/romeodiaz/guava-mode" for the rules only.

## How to update
Update the plugin with `/plugin update` (or reinstall it), then tell your assistant **"update Owner Mode"**. It checks the version number, only updates if there's something newer, and tells you what changed. See [CHANGELOG.md](CHANGELOG.md).

## What this changes
Setup asks for a yes before each of these:
- **Files edited:** appends a short section to `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` (never replaces what's there). Optional step 2b backs up `~/.claude/settings.json` and adds four read-only Notion tools to `permissions.allow`.
- **Commands run:** `npm i -g @anthropic-ai/claude-code`, `npm i -g @openai/codex`, `claude auth login`, `codex login --device-auth`, a quick test prompt in each, and optionally Cisco Skill Scanner on third-party skills.
- **Files read:** only the local instruction, skill or notes files you approve. It never reads your Claude or ChatGPT memories or chats; you paste or export what you want.
- **Saved:** pages and a Skills database in your Notion, and standing instructions in your assistant's memory.
- **External services:** Notion, Anthropic (Claude Code), OpenAI (Codex), GitHub (this repo). Nothing is sent to Guava, and the plugin fetches no remote instructions.

## Example prompts
1. "Set me up by following the Start here steps in the guava-mode plugin."
2. "Turn on Owner Mode."
3. "Import my existing CLAUDE.md and skills into my AI Context Hub."

## Support & privacy
- Support: https://workwithguava.com/talk, or open an issue on GitHub.
- Privacy: https://workwithguava.com/privacy. Guava collects no data; everything stays in your own Notion, computer and AI accounts.

## Want it for your whole team?
For a multiplayer version for your team or org, book a call: https://workwithguava.com/talk

## Credits
Adapted from [poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md) in Cursor's pstack plugin, by poteto, from [Matt Pocock's skills](https://github.com/mattpocock/skills) and the [humanizer skill](https://github.com/blader/humanizer) by blader.

By Romeo Diaz, Guava ([workwithguava.com](https://workwithguava.com)). Follow @romeodiazai on LinkedIn and X.

## License
MIT. See [LICENSE](LICENSE).
