# Meta Muse Bot adapter

- **Connect your hub:** tell Muse "Connect my Notion" (or the app your hub lives in, if Muse offers it) and approve access to your AI Context Hub. Start with just the hub, not your whole workspace. Muse can't see a folder on your computer, so a local Markdown hub needs one of the options in its backend file.
- Muse doesn't let you upload your own skills, so don't install them as files. Keep the skills in the hub and have Muse read the matching one from there when a task needs it.
- **Add the standing instructions:** click the bot's avatar, open the Fingerprint tab, and open SOUL.md. Add these lines at the end, then save. Add to what's there; never replace or delete anything. These are the default lines; swap in the owner's hub, planner and worker from Stack settings if they picked something else:
  ```
  Before any substantive task, load my Notion AI Context Hub first (Profile & Context, Agent Rules and Skills) and treat it as the source of truth.
  Model routing: Claude Opus 5.5 High via Claude CLI (`claude -p`) for orchestration, research, planning, brainstorming, copywriting, validation, review, verification, fuzzy and hard problems; GPT-6.1 Sol High via Codex CLI (`codex exec`) for bulk execution, coding, sub-agent tasks, worker threads and long-running jobs; quick replies and connector lookups stay with you; if either CLI fails, do the task yourself and say so; when a skill defines how it runs, follow the skill and use routing only for work it leaves open. Run routed work through the CLI without being asked, and mention which one you used.
  When I say "update founder-mode", follow founder-mode/skills/founder-mode-rules/SKILL.md from github.com/romeodiaz/guava-stack.
  ```
  Leave IDENTITY.md alone. Use MEMORY.md only for facts about the owner, never for passwords, keys or other secrets.
- **Verify:** start a new chat and ask "Write a short intro about my business." It passes if the intro uses details from the hub.
- **Run the CLI steps and model router in Muse's own terminal.** Muse can install Claude Code with npm and usually has Codex already; follow step 1 of the Model Router setup in guava-router (it checks and skips what's installed). For sign-in, the owner opens the link and signs in with their own account, then pastes any code straight into Muse, never anywhere else. When Muse asks to share information with anthropic.com or openai.com, choose Allow once, not Always allow.
- Muse asks before important actions like sending email. Keep those approvals on.
