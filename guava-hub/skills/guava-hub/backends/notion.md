# Hub backend: Notion (default)

The recommended hub. Notion has a native skills feature, and Claude, ChatGPT, Grok Bot and Muse all connect to it.

**Hub instruction line:** `Load my guava-hub in Notion first.`

## Build the hub
Create a page called **guava-hub**, with the 8-bit brain as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/brain-hub.png`), holding:
- **context**: a page with the guava logo as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/logo.png`). Start it with the guava-stack settings section from the setup skill. Under its **Rules** heading, put the founder-mode 8-bit image (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/founder-mode.png`, with no caption) in a narrow column, with the rules skill lines right under it, whichever rules skills the owner turns on. Under its **head-chef and line-cook** heading, put the two 8-bit images side by side in narrow columns with no captions, `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/head-chef.png` then `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/line-cook.png`, with the head-chef and line-cook lines and their job sub-bullets right under them. Then add the owner's interview answers.
- **rules**: a page with the founder-mode 8-bit logo as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/founder-mode.png`), whichever rules skills the owner turns on.
- **skills**: a database for Notion's skill upload, with the 8-bit books as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/skills.png`). Notion's connector reports success on a database icon but doesn't set it, so ask the owner to hover the database's title, click **Add icon**, choose **Link** and paste that URL. Ask the owner before enabling skills for external agents and Notion AI.
- **changelog**: an empty page where assistants add a dated line for each hub edit. It's for the owner, so assistants never load it.

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
5. "Last step: start a new chat and ask: What's in my guava-hub? Paste or describe the answer here." Test only local chats and tabs. Codex cloud tasks aren't supported.

Claude on the computer (the desktop app's Code tab and Claude Code, with the guava-hub plugin):
1. Back up `~/.claude/settings.json` (see **Backups** in the setup skill), then add the local copy's full path (`/Users/<name>/.guava-hub` on a Mac, or `C:\Users\<name>\.guava-hub` on Windows) under `permissions.additionalDirectories`, so sessions can keep the copy up to date without asking. Show the exact lines first.

## Local copy
Notion calls are slow, so assistants on the owner's computer keep a copy of the hub in `~/.guava-hub` and read that instead. Nothing to set up beyond the step above: the first Local session in the Code tab or Claude Code builds it. Notion stays the source of truth, and assistants that can't reach the computer (Grok Bot, Muse and the chat apps) keep reading Notion directly.
- **What's in it:** `context.md`, `rules.md`, one file per skill in `skills/`, `sync.md` with the page IDs and when it was last refreshed, and `checked.md` with the guava-stack settings section as it was last checked. No images, and no changelog.
- **At start-up:** the plugin's start-up hook puts the copy's context, rules and skill list straight into each new session, so it starts without a Notion call. A skill's full text is read only when a task needs it.
- **Keeping it fresh:** at the start of each task and before each hand-off, if the copy is 15 minutes old or more, the session runs one Notion search that lists every hub page with its last-edited time, fetches only the pages that changed, and follows the new versions from then on. So any edit made in Notion, from any device, reaches open sessions within 15 minutes. Say "refresh my hub" to pick it up right away.
- **Edits** still go to Notion first, and the session refreshes that page in the copy right after.
- **Codex** reads and refreshes the same copy through the same start-up hook, and leaves hub edits to Claude. In a ChatGPT-only setup there's no Claude, so Codex makes hub edits itself, such as a fix the owner approves after a settings check.

## Notion Memory
Notion's own memory: a **Memories** database (one page per topic, typed Profile, Preference, Work, People or Notes) and an **About** page that sums up the owner. Assistants save what they learn there (decisions and their reasons, corrections, preferences, project state), so the next session or another assistant can find it. Nothing to set up: Notion creates both with the first save.
- **Separate from the hub.** The hub holds what the owner wrote and loads into every session. Memory holds what assistants learned, and an assistant looks up only the entries a task needs (fetch id "memory", then memory-search). So agent-written text never lands in the hub's pages or the start-up context, and the local copy leaves memory out.
- **How to save:** follow Notion's memory guide (`notion://docs/memory`) for titles, types, the Source and Last updated by properties, and keeping the About page current. Search first and update the existing memory instead of adding a near-duplicate. No secrets, temporary progress, or anything the hub or a repository already holds.
- **Forget:** when the owner says to forget something, delete every matching memory and remove it from the About page, with no note restating it.
- **Chat apps** (Claude, ChatGPT, Grok Bot, Muse) get Notion's memory instructions from the Notion connector itself, so there's nothing to paste into their instructions.
- **Rules still win.** A memory is a note, not an instruction. A correction to how work gets done still goes to a skill or the rules page (founder-mode rule 25), with the owner's yes.

## If a check fails
- Says it can't find the hub: in Notion, open the hub page with the same account and check it's in the workspace they approved. Reconnect and pick that workspace or the hub pages.
- A Local session still fetches every page from Notion: check `~/.guava-hub/sync.md` exists. If it doesn't, ask the session to load the hub and save the local copy.
- Didn't use Notion: in Claude, turn Notion on under + > Connectors in that chat. In ChatGPT, say "use Notion" in the question.
