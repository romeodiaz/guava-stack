# Meta Muse Bot adapter

- **Connect Notion:** tell Muse "Connect my Notion" and approve access to your AI Context Hub. Start with just the hub pages, not your whole workspace.
- Muse doesn't let you upload your own skills, so don't install them as files. Keep the skills in the Notion hub and have Muse read the matching one from there when a task needs it.
- **Add the standing instructions:** click the bot's avatar, open the Fingerprint tab, and open SOUL.md. Add these lines at the end, then save. Add to what's there; never replace or delete anything. Also save the README's model-routing instruction there:
  ```
  Before any substantive task, load my Notion AI Context Hub first (Profile & Context, Agent Rules and Skills) and treat it as the source of truth.
  Route work per the model routing in my Notion hub: Claude Code CLI for thinking work, Codex CLI for execution work; if a CLI fails, do it yourself and say so.
  When I say "update Owner Mode", follow skills/owner-mode-rules/SKILL.md from github.com/romeodiaz/guava-mode.
  ```
  Leave IDENTITY.md alone. Use MEMORY.md only for facts about the owner, never for passwords, keys or other secrets.
- **Verify:** start a new chat and ask "Write a short intro about my business." It passes if the intro uses details from the hub.
- **Run the CLI steps and model router in Muse's own terminal.** Muse can install Claude Code with npm and usually has Codex already; follow setup step 2 (it checks and skips what's installed). For sign-in, the owner opens the link and signs in with their own account, then pastes any code straight into Muse, never anywhere else. When Muse asks to share information with anthropic.com or openai.com, choose Allow once, not Always allow.
- Muse asks before important actions like sending email. Keep those approvals on.
