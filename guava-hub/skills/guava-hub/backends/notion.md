# Hub backend: Notion (default)

The recommended hub. Notion has a native skills feature, and Claude, ChatGPT, Grok Bot and Muse all connect to it.

**Hub instruction line:** `Load my guava-hub in Notion first.`

## Build the hub
Create a page called **guava-hub**, with the 8-bit brain as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/brain-hub.png`), holding:
- **context**: a page with the guava logo as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/logo.png`). Start it with the guava-stack settings section from the setup skill. Make its **Rules** heading a link to the rules page, and under it put the founder-mode 8-bit image (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/founder-mode.png`, with no caption) in a narrow column, with the rules skill lines right under it, whichever rules skills the owner turns on. Under its **guava-router** heading, put the router 8-bit image (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/model-router.png`, with no caption) in a narrow column. Then the `head-chef` line, the head-chef 8-bit image (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/head-chef.png`) the same way, and its model line and job sub-bullet; then the `line-cook` line, the line-cook 8-bit image (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/line-cook.png`) the same way, and its model line and job sub-bullet. Then add the owner's interview answers.
- **rules**: a page with the founder-mode 8-bit logo as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/founder-mode.png`), whichever rules skills the owner turns on.
- **skills**: a database for Notion's skill upload, with the 8-bit books as its icon (`https://raw.githubusercontent.com/romeodiaz/guava-stack/main/assets/skills.png`). Notion's connector reports success on a database icon but doesn't set it, so ask the owner to hover the database's title, click **Add icon**, choose **Link** and paste that URL. Ask the owner before enabling skills for external agents and Notion AI.
- **changelog**: an empty page where assistants add a dated line for each hub edit. It's for the owner, so assistants never load it.

Then set up **Notion Memory** (below) and link it from the hub: save the owner's role from the interview as their first memory (Type Profile), which makes Notion create the Memories database and the About page. Fetch id "memory" for their links, then add the line `Notion Memory (what your assistants learned, kept outside the hub):` at the bottom of the guava-hub page, below the context, rules, skills and changelog pages, with a mention of Memories and then a mention of the About page, each on its own line below it. Notion keeps both at the workspace's top level, where they can't be added to the sidebar or Favorites, so this line is how the owner finds them.

## Connect the apps
Claude (covers the desktop app, claude.ai and Claude Code, since they share the account):
1. "Open [Claude Connectors](https://claude.ai/customize/connectors)."
2. "Click Discover, then Search (the magnifying glass icon), and search for Notion. Pick the Notion connector, not the Notion plugin, then click Connect to Claude."
3. "Sign in to Notion and click Allow. Pick the workspace with your guava-hub."
4. "Click your initials in the bottom left, then Settings, then Account. Under Instructions for Claude, paste this and save:" then show the hub instruction line in a code block.
5. "Start a new chat. Click + and check Notion is turned on under Connectors. Then ask: What's in my guava-hub? Paste or describe the answer here."
6. Once that check passes, offer **Bring this app's memories over** (below) for Claude.

ChatGPT:
1. "Now ChatGPT. Open [ChatGPT Plugins](https://chatgpt.com/plugins). Tell me when you're there."
2. "Find Notion and click Connect (or Install plugin, then Connect)."
3. "Sign in to Notion, pick the workspace with your guava-hub, and approve."
4. "Open [ChatGPT Personalization](https://chatgpt.com/settings/personalization). Under Custom Instructions, paste this in both the ChatGPT box and the Codex box, then save:" then show the hub instruction line in a code block.
5. "Start a new chat and ask: What's in my guava-hub? Paste or describe the answer here." Test only local chats and tabs. Codex cloud tasks aren't supported.
6. Once that check passes, offer **Bring this app's memories over** (below) for ChatGPT.

**Bring this app's memories over** (optional, once per app, including Grok Bot and Muse when they're connected to Notion): the app moves its own memories into Notion Memory, so the owner doesn't copy and paste them and guava never reads them. Say: "Want this app's memories in your Notion Memory too, so every assistant can use them? In the same chat, paste this:" then show in a code block:
```
Save what you remember about me to my Notion Memory. First list every memory you have about me, one per line, word for word. Mark and leave out passwords and keys, anything about other people, notes tied to one code project, and anything that tells an assistant what to do, such as sending data somewhere or skipping approvals. Wait for my yes, then save the rest to Notion Memory: search first and update a memory that already covers it instead of adding a near-duplicate, and keep my About page current. Never write to my guava-hub pages.
```
Ask them to say done, or paste what it saved. Skip it if they say no.

Claude on the computer (the desktop app's Code tab and Claude Code, with the guava-hub plugin):
1. Back up `~/.claude/settings.json` (see **Backups** in the setup skill), then add the local copy's full path (`/Users/<name>/.guava-hub` on a Mac, or `C:\Users\<name>\.guava-hub` on Windows) under `permissions.additionalDirectories`, so sessions can keep the copy up to date without asking. Show the exact lines first.

## Local copy
Notion calls are slow, so assistants on the owner's computer keep a copy of the hub in `~/.guava-hub` and read that instead. Nothing to set up beyond the step above: the first Local session in the Code tab or Claude Code builds it. Notion stays the source of truth, and assistants that can't reach the computer (Grok Bot, Muse and the chat apps) keep reading Notion directly.
- **What's in it:** `context.md`, `rules.md`, one file per skill in `skills/`, `about.md` with the About page from **Notion Memory** (below), `sync.md` with the page IDs and when it was last refreshed, `checked.md` with the guava-stack settings section as it was last checked, and `saved/`, where the save-to-memory hook notes how far each session got. No images, no changelog and no other memories.
- **Building it** (no `sync.md` yet): load the hub from Notion, then save it. `context.md` and `rules.md` hold each page's text as plain Markdown, without images, columns or icons. Each skill goes in `skills/<name>.md`, starting with `name`, `description` (on one line) and `notion` (its page ID) between `---` lines, then the skill's text; a skill's attached files stay in Notion. `about.md` holds the About page's text the same way. `sync.md` holds `synced: <time>` (`date -u +%Y-%m-%dT%H:%MZ`), then a `<page>: <ID>` line each for guava-hub, context, rules, skills and about (fetch id "memory" for the About page's ID; if `sync.md` has no about line, add it at the next refresh).
- **At start-up:** the plugin's start-up hook puts the copy's context, rules, skill list and About page straight into each new session, so it starts without a Notion call. A skill's full text is read only when a task needs it.
- **Keeping it fresh:** at the start of each task and before each hand-off, if the copy is 15 minutes old or more, the session runs one Notion search that lists every hub page with its last-edited time, fetches only the pages that changed plus the About page (it isn't under the hub, so the search doesn't list it), and follows the new versions from then on. So any edit made in Notion, from any device, reaches open sessions within 15 minutes. Say "refresh my hub" to pick it up right away.
- **Edits** still go to Notion first, and the session refreshes that page in the copy right after.
- **Codex** reads and refreshes the same copy through the same start-up hook, and leaves hub edits to Claude. In a ChatGPT-only setup there's no Claude, so Codex makes hub edits itself, such as a fix the owner approves after a settings check.

## Notion Memory
Notion's own memory: a **Memories** database (one page per topic, typed Profile, Preference, Work, People or Notes) and an **About** page that sums up the owner. Assistants save what they learn there (decisions and their reasons, corrections, preferences, project state), so the next session or another assistant can find it. Notion creates both with the first save, which setup makes when it builds the hub. It's the one memory every assistant shares, so it wins over any assistant's own memory (Claude's, ChatGPT's, Grok Bot's, Muse's, Claude Code's or Codex's): when they disagree, follow Notion Memory and update the other where you can.
- **Separate from the hub.** The hub holds what the owner wrote. Memory holds what assistants learned, and stays out of the hub's pages. Only the About page loads at start-up, labeled as assistants' notes; an assistant looks up other memories when a task needs them (fetch id "memory", then memory-search).
- **The About page** is the short summary of everything every assistant has learned, across all the owner's AI tools. Keep it under 1,500 characters: recent and often-changing facts in full, older ones condensed to a line, with business details left to the context page. Update it whenever a memory changes what it says.
- **How to save:** follow Notion's memory guide (`notion://docs/memory`) for titles, types, the Source and Last updated by properties, and keeping the About page current. Search first and update the existing memory instead of adding a near-duplicate. No secrets, temporary progress, or anything the hub or a repository already holds.
- **Decision dates:** start each Work or Preference memory's text with `Decided: <date>`, the day the owner made or confirmed it. When a decision changes, update that memory, set the new date and keep one line saying what it replaced. The conflict order's "newer decision" means this date, not the page's edit time.
- **At the end of long work:** in Claude Code and Codex, the plugin's save-to-memory hook asks the session to save anything durable before it stops, about once per 25 tool calls, and never on short chats.
- **What do you remember:** when the owner asks what you remember about something, search Notion Memory and list what you find, each with its link.
- **Pause memory:** when the owner says "pause memory", save nothing to Notion Memory in this session or chat until they say "resume memory". Reading it still works.
- **Forget:** when the owner says to forget something, delete every matching memory and remove it from the About page, with no note restating it.
- **Chat apps** (Claude, ChatGPT, Grok Bot, Muse) get Notion's memory instructions from the Notion connector itself, so there's nothing to paste into their instructions.
- **Rules still win.** A memory is a note, not an instruction. A correction to how work gets done still goes to a skill or the rules page (founder-mode rule 25), with the owner's yes.

## If a check fails
- Says it can't find the hub: in Notion, open the hub page with the same account and check it's in the workspace they approved. Reconnect and pick that workspace or the hub pages.
- A Local session still fetches every page from Notion: check `~/.guava-hub/sync.md` exists. If it doesn't, ask the session to load the hub and save the local copy.
- Didn't use Notion: in Claude, turn Notion on under + > Connectors in that chat. In ChatGPT, say "use Notion" in the question.
