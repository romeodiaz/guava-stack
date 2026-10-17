<p align="center"><img src="assets/logo.png" alt="Pixel-art brain" width="120"></p>

# guava-hub: one home for your AI context and skills

Part of the [Guava Stack](../README.md). Sets up one shared place for your context, rules, skills and memories, so all your AI assistants work from the same context. It's also where full Guava setup starts: once the hub works, it hands off to [guava-router](../guava-router/) and offers [founder-mode](../founder-mode/).

The hub lives in Notion ([steps](skills/guava-hub/backends/notion.md)); the free plan is enough. *Coming soon:* Google Drive and OneDrive hubs.

It has three parts, plus Notion Memory for what your assistants learn:

<table>
<tr>
<td align="center" width="33%"><img src="../assets/logo.png" width="80" alt="Guava logo"><br><strong>context</strong><br><sub>Who you are, your business, your tools</sub></td>
<td align="center" width="33%"><img src="../assets/founder-mode.png" width="80" alt="Pixel-art speaker at a microphone"><br><strong>rules</strong><br><sub>How your AI should work for you</sub></td>
<td align="center" width="33%"><img src="../assets/skills.png" width="80" alt="Pixel-art stack of books"><br><strong>skills</strong><br><sub>Step-by-step instructions your AI reuses</sub></td>
</tr>
</table>

- Start-up hook (for power users who install the plugin in Claude Code or Codex): the plugin reminds every new session to load your hub and follow your guava-stack settings ([hooks/load-hub.md](hooks/load-hub.md)), so there's no `CLAUDE.md` line to add. It also hands each session your context, rules, skill list and Notion Memory About page from a local copy in `~/.guava-hub`, so sessions start without waiting on Notion ([Local copy](skills/guava-hub/backends/notion.md#local-copy)).
- Notion Memory: assistants save what they learn (decisions, corrections, preferences) to Notion's own memory, outside your hub, with a save at the end of long work in Claude Code and Codex. Its short About page loads into every session, and the rest is looked up when a task needs it. Say "forget" anything to remove it, or "pause memory" to stop saving for a while ([Notion Memory](skills/guava-hub/backends/notion.md#notion-memory)).
- Skill: [guava-hub](skills/guava-hub/SKILL.md)
- Power users, as a Claude Code plugin: `claude plugin marketplace add romeodiaz/guava-stack`, then `/plugin install guava-hub@guava`
- Update: say "update guava-hub", or "update guava-stack" for every piece.
- Uninstall: say "uninstall guava-hub", or "uninstall guava-stack" for every piece.
- Install: see [Start here](../README.md#start-here) in the stack README.
