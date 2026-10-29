<p align="center"><img src="assets/logo.png" alt="Pixel-art brain" width="120"></p>

# guava-hub: one home for your AI context and skills

Part of the [Guava Stack](../README.md). Sets up one shared place for your context, rules, skills and memories, so all your AI assistants work from the same context. It's also where full Guava setup starts: once the hub works, it hands off to [guava-router](../guava-router/) and offers [founder-mode](../founder-mode/).

The hub lives in Notion ([steps](skills/guava-hub/backends/notion.md)); the free plan is enough. It's built on Notion's official [setup guide for agents](https://developers.notion.com/prompts/setup): setup runs Notion's steps (your Agent Operating Guide, the custom instructions every app shares and a daily memory check), then adds the hub, Tasks and Guava's own instructions, [guava-instructions](skills/guava-instructions/SKILL.md), as a skill every app loads. *Coming soon:* Google Drive and OneDrive hubs.

It has three parts, plus your Tasks database and Notion Memory:

<table>
<tr>
<td align="center" width="33%"><img src="../assets/logo.png" width="80" alt="Guava logo"><br><strong>context</strong><br><sub>Who you are, your business, your tools</sub></td>
<td align="center" width="33%"><img src="../assets/founder-mode.png" width="80" alt="Pixel-art speaker at a microphone"><br><strong>rules</strong><br><sub>How your AI should work for you</sub></td>
<td align="center" width="33%"><img src="../assets/skills.png" width="80" alt="Pixel-art stack of books"><br><strong>skills</strong><br><sub>Step-by-step instructions your AI reuses</sub></td>
</tr>
</table>

- Tasks: your own Notion Tasks database becomes one list for your to-dos and your AI's work. Each bigger piece of work you'd track, such as a project, event or feature, gets a row with an ID such as TASK-12, its goal, status and links. The ID goes in commits, PRs, hand-offs and memories, so one search finds the whole trail. Small changes you only approve, such as new icons or a renamed skill, skip the list; their commit or PR is the record. Setup adopts the Tasks database you have, or makes one, and lists it with your other databases in your Agent Operating Guide's **Workspace and destinations**, so assistants file deals, call notes and docs in your own databases.
- Notion Memory: assistants save what they learn (decisions, corrections, preferences) to Notion's own memory, outside your hub, and look it up when a task needs it. Say "forget" anything to remove it, or "pause memory" to stop saving for a while ([Notion Memory](skills/guava-hub/backends/notion.md#notion-memory)).
- Skill: [guava-hub](skills/guava-hub/SKILL.md)
- Update: say "update guava-hub", or "update guava-stack" for every piece.
- Uninstall: say "uninstall guava-hub", or "uninstall guava-stack" for every piece.
- Install: see [Start here](../README.md#start-here) in the stack README.
