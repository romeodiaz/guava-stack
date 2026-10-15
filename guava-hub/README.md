<p align="center"><img src="assets/logo.png" alt="Guava logo" width="120"></p>

# guava-hub: AI Context & Skills Hub

Part of the [Guava Stack](../README.md). Sets up one shared place for your profile, rules and skills, so all your AI assistants work from the same context. It's also where full Guava setup starts: once the hub works, it hands off to [guava-router](../guava-router/) and offers [founder-mode](../founder-mode/).

Pick where your hub lives:

| Hub | Steps |
|---|---|
| **Notion** (default) | [backends/notion.md](skills/context-skills-hub-setup/backends/notion.md) |
| Google Drive | [backends/google-drive.md](skills/context-skills-hub-setup/backends/google-drive.md) |
| OneDrive / SharePoint | [backends/onedrive-sharepoint.md](skills/context-skills-hub-setup/backends/onedrive-sharepoint.md) |
| Obsidian / local Markdown | Coming soon |

Every hub has the same three parts (Profile & Context, Agent Rules and Skills), so you can switch backends later without changing anything else.

- Skill: [context-skills-hub-setup](skills/context-skills-hub-setup/SKILL.md)
- Claude Code: `/plugin install guava-hub --marketplace romeodiaz/guava-stack`
- Install: see [Start here](../README.md#start-here) in the stack README.
