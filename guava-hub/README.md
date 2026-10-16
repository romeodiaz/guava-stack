<p align="center"><img src="assets/logo.png" alt="Pixel-art brain" width="120"></p>

# guava-hub: AI Context & Skills Hub

Part of the [Guava Stack](../README.md). Sets up one shared place for your profile, rules and skills, so all your AI assistants work from the same context. It's also where full Guava setup starts: once the hub works, it hands off to [guava-router](../guava-router/) and offers [founder-mode](../founder-mode/).

Pick where your hub lives:

| Hub | Steps |
|---|---|
| **Notion** (default) | [backends/notion.md](skills/guava-hub/backends/notion.md) |
| Google Drive | [backends/google-drive.md](skills/guava-hub/backends/google-drive.md) |
| OneDrive / SharePoint | [backends/onedrive-sharepoint.md](skills/guava-hub/backends/onedrive-sharepoint.md) |
| Local Markdown / Obsidian | [backends/local-markdown.md](skills/guava-hub/backends/local-markdown.md) |

Every hub has the same three parts (Profile & Context, Agent Rules and Skills), so you can switch backends later without changing anything else.

- Start-up hook: in Claude Code and the Claude desktop app's Code tab, the plugin reminds every new session to load your hub and follow your Stack settings ([hooks/load-hub.md](hooks/load-hub.md)), so there's no `CLAUDE.md` line to add.
- Skill: [guava-hub](skills/guava-hub/SKILL.md)
- Claude Code: `/plugin install guava-hub --marketplace romeodiaz/guava-stack`
- Update: say "update guava-hub", or "update guava-stack" for every piece.
- Install: see [Start here](../README.md#start-here) in the stack README.
