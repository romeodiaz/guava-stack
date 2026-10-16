# Hub backend: Notion (default)

The recommended hub. Notion has a native skills feature, and Claude, ChatGPT, Grok Bot and Muse all connect to it.

**Hub instruction line:** `Load my guava-hub in Notion first.`

## Build the hub
Create a page called **guava-hub**, with the 8-bit brain as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/brain-hub.png`), holding:
- **Context**: a page with the guava logo as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/logo.png`). Start it with the guava-stack settings section from the setup skill. Under its **Rules** heading, put the founder-mode 8-bit image (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/founder-mode.png`, with no caption) in a narrow column, with the rules skill lines right under it, whichever rules skills the owner turns on. Under its **head-chef and line-cook** heading, put the two 8-bit images side by side in narrow columns with no captions, `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/head-chef.png` then `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/line-cook.png`, with the head-chef and line-cook lines and their job sub-bullets right under them. Then add the owner's interview answers.
- **Rules**: a page with the founder-mode 8-bit logo as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/founder-mode.png`), whichever rules skills the owner turns on.
- **Skills**: a database for Notion's skill upload, with the 8-bit books as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/skills.png`). Notion's connector reports success on a database icon but doesn't set it, so ask the owner to hover the database's title, click **Add icon**, choose **Link** and paste that URL. Ask the owner before enabling skills for external agents and Notion AI.
- **Change log**: an empty page where assistants add a dated line for each hub edit. It's for the owner, so assistants never load it.

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

Claude on the computer (the desktop app's Code tab and Claude Code, with the guava-hub plugin):
1. Back up `~/.claude/settings.json`, then add the local copy's full path (`/Users/<name>/.guava-hub` on a Mac, or `C:\Users\<name>\.guava-hub` on Windows) under `permissions.additionalDirectories`, so sessions can keep the copy up to date without asking. Show the exact lines first.

## Local copy
Notion calls are slow, so assistants on the owner's computer keep a copy of the hub in `~/.guava-hub` and read that instead. Nothing to set up beyond the step above: the first Local session in the Code tab or Claude Code builds it. Notion stays the source of truth, and assistants that can't reach the computer (Grok Bot, Muse, the chat apps, cloud sessions) keep reading Notion directly.
- **What's in it:** `Context.md`, `Rules.md`, one file per skill in `Skills/`, and `sync.md` with the page IDs and when it was last refreshed. No images, and no Change log.
- **At start-up:** the plugin's start-up hook puts the copy's Context, Rules and skill list straight into each new session, so it starts without a Notion call. A skill's full text is read only when a task needs it.
- **Keeping it fresh:** at the start of each task and before each hand-off, if the copy is 15 minutes old or more, the session runs one Notion search that lists every hub page with its last-edited time, fetches only the pages that changed, and follows the new versions from then on. So any edit made in Notion, from any device, reaches open sessions within 15 minutes. Say "refresh my hub" to pick it up right away.
- **Edits** still go to Notion first, and the session refreshes that page in the copy right after.
- **Codex** reads the same copy, and leaves refreshing and hub edits to Claude.

## If a check fails
- Says it can't find the hub: in Notion, open the hub page with the same account and check it's in the workspace they approved. Reconnect and pick that workspace or the hub pages.
- A Local session still fetches every page from Notion: check `~/.guava-hub/sync.md` exists. If it doesn't, ask the session to load the hub and save the local copy.
- Didn't use Notion: in Claude, turn Notion on under + > Connectors in that chat. In ChatGPT, say "use Notion" in the question.
