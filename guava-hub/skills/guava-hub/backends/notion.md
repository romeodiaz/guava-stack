# Hub backend: Notion (default)

The recommended hub. Notion has a native skills feature, and Claude, ChatGPT, Grok Bot and Muse all connect to it.

**Hub instruction line:** `Load my guava-hub in Notion first.`

## Build the hub
Create a page called **guava-hub**, with the 8-bit brain as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/brain-hub.png`), holding:
- **Profile & Context**: a page with the guava logo as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/logo.png`). Start it with the Stack settings section from the setup skill, then the owner's interview answers.
- **Agent Rules**: a page with the 🛡️ icon.
- **Skills**: a database for Notion's skill upload. Ask the owner before enabling skills for external agents and Notion AI.

## Connect the apps
Claude (covers the desktop app, claude.ai and Claude Code, since they share the account):
1. "Open [Claude Connectors](https://claude.ai/customize/connectors)."
2. "Click Discover, then Search (the magnifying glass icon), and search for Notion. Pick the Notion connector, not the Notion plugin, then click Connect to Claude."
3. "Sign in to Notion and click Allow. Pick the workspace with your guava-hub."
4. "Click your initials in the bottom left, then Settings, then Account. Under Instructions for Claude, paste this and save:" then show the hub instruction line in a code block.
5. "Start a new chat. Click + and check Notion is turned on under Connectors. Then ask: What's in my guava-hub? Paste or describe the answer here."

ChatGPT:
1. "Now ChatGPT. Open [ChatGPT Plugins](https://chatgpt.com/plugins). Tell me when you're there."
2. "Find Notion and click Connect (or Install plugin, then Connect)."
3. "Sign in to Notion, pick the workspace with your guava-hub, and approve."
4. "Open [ChatGPT Personalization](https://chatgpt.com/settings/personalization). Under Custom Instructions, paste this in both the ChatGPT box and the Codex box, then save:" then show the hub instruction line in a code block.
5. "Last step: start a new chat and ask: What's in my guava-hub? Paste or describe the answer here." Test only local chats and tabs. Skip cloud tasks: they need a GitHub-connected cloud environment, which is too technical for this setup and doesn't pick up custom instructions yet. If the owner asks, tell them cloud tasks can still find the hub through Notion, just more slowly.

## If a check fails
- Says it can't find the hub: in Notion, open the hub page with the same account and check it's in the workspace they approved. Reconnect and pick that workspace or the hub pages.
- Didn't use Notion: in Claude, turn Notion on under + > Connectors in that chat. In ChatGPT, say "use Notion" in the question.
