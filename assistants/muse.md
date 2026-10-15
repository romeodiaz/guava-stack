# Meta Muse Bot adapter

- **Connect Notion:** tell Muse "Connect my Notion" and approve access to your AI Context Hub. Start with just the hub pages, not your whole workspace.
- Muse doesn't let you upload your own skills, so don't install them as files. Keep the skills in the Notion hub and have Muse read the matching one from there when a task needs it.
- **Add the standing instructions:** click the bot's avatar, open the Fingerprint tab, and open SOUL.md. Add these lines at the end, then save. Add to what's there; never replace or delete anything. Leave out the README's model-routing instruction, since Muse does the work itself:
  ```
  Before any substantive task, load my Notion AI Context Hub first (Profile & Context, Agent Rules and Skills) and treat it as the source of truth.
  When I say "update Owner Mode", follow skills/owner-mode-rules/SKILL.md from github.com/romeodiaz/guava-mode.
  ```
  Leave IDENTITY.md alone. Use MEMORY.md only for facts about the owner, never for passwords, keys or other secrets.
- **Verify:** start a new chat and ask "Write a short intro about my business." It passes if the intro uses details from the hub.
- Skip the CLI steps (2 and 2b) and the model router, and tell the owner what you skipped. Muse does the work itself.
- Muse asks before important actions like sending email. Keep those approvals on.
