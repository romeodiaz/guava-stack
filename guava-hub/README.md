<p align="center"><img src="assets/logo.png" alt="Pixel-art brain" width="120"></p>

# guava-hub: one home for your AI context and skills

Part of the [Guava Stack](../README.md). Sets up one shared place for your context, rules and skills, so all your AI assistants work from the same context. It's also where full Guava setup starts: once the hub works, it hands off to [guava-router](../guava-router/) and offers [founder-mode](../founder-mode/).

Pick where your hub lives:

| Hub | Steps |
|---|---|
| **Notion** (default) | [backends/notion.md](skills/guava-hub/backends/notion.md) |
| Google Drive | [backends/google-drive.md](skills/guava-hub/backends/google-drive.md) |
| OneDrive / SharePoint | [backends/onedrive-sharepoint.md](skills/guava-hub/backends/onedrive-sharepoint.md) |
| Local Markdown / Obsidian | [backends/local-markdown.md](skills/guava-hub/backends/local-markdown.md) |

Every hub has the same three parts, so you can switch backends later without changing anything else:

<table>
<tr>
<td align="center" width="33%"><img src="../assets/logo.png" width="80" alt="Guava logo"><br><strong>context</strong><br><sub>Who you are, your business, your tools</sub></td>
<td align="center" width="33%"><img src="../assets/founder-mode.png" width="80" alt="Pixel-art speaker at a microphone"><br><strong>rules</strong><br><sub>How your AI should work for you</sub></td>
<td align="center" width="33%"><img src="../assets/skills.png" width="80" alt="Pixel-art stack of books"><br><strong>skills</strong><br><sub>Step-by-step instructions your AI reuses</sub></td>
</tr>
</table>

- Start-up hook: in Claude Code, the Claude desktop app's Code tab and Codex, the plugin reminds every new session to load your hub and follow your guava-stack settings ([hooks/load-hub.md](hooks/load-hub.md)), so there's no `CLAUDE.md` line to add. With a Notion hub, it also hands each session your context, rules and skill list from a local copy in `~/.guava-hub`, so sessions start without waiting on Notion ([Local copy](skills/guava-hub/backends/notion.md#local-copy)).
- Skill: [guava-hub](skills/guava-hub/SKILL.md)
- Claude Code: `/plugin install guava-hub --marketplace romeodiaz/guava-stack`
- Update: say "update guava-hub", or "update guava-stack" for every piece.
- Install: see [Start here](../README.md#start-here) in the stack README.
