# Hub backend: Google Drive

For owners who already run their business in Google Workspace or Gmail.

**Hub instruction line:** `Load my guava-hub first: the "guava-hub" folder in my Google Drive.`

## Build the hub
In the owner's Google Drive (My Drive, or a shared drive if their team will use it), create a folder called **guava-hub** with:
- **Profile & Context**: a Google Doc. Start it with the Stack settings section from the setup skill, then the owner's interview answers.
- **Agent Rules**: a Google Doc.
- **Skills**: a folder with one Google Doc per skill, named after the skill and holding its full text (name, one-line description, then the steps). Every skill in this folder counts as turned on. To turn one off, move it to a sibling folder called **Skills (off)**.

Use Google Docs, not uploaded Word or Markdown files: the Claude and ChatGPT Drive connectors read Google Docs most reliably. Keep the folder private to the owner unless they ask to share it.

## Connect the apps
Claude (covers the desktop app, claude.ai and Claude Code, since they share the account):
1. "Open [Claude Connectors](https://claude.ai/customize/connectors)."
2. "Click Discover, then Search (the magnifying glass icon), and search for Google Drive. Pick the Google Drive connector, then click Connect."
3. "Sign in with the Google account that owns your guava-hub folder and click Allow."
4. "Click your initials in the bottom left, then Settings, then Account. Under Instructions for Claude, paste this and save:" then show the hub instruction line in a code block.
5. "Start a new chat. Click + and check Google Drive is turned on under Connectors. Then ask: What's in my guava-hub? Paste or describe the answer here."

ChatGPT:
1. "Now ChatGPT. Open [ChatGPT Plugins](https://chatgpt.com/plugins). Tell me when you're there."
2. "Find Google Drive and click Connect (or Install plugin, then Connect)."
3. "Sign in with the Google account that owns your guava-hub folder and approve."
4. "Open [ChatGPT Personalization](https://chatgpt.com/settings/personalization). Under Custom Instructions, paste this in both the ChatGPT box and the Codex box, then save:" then show the hub instruction line in a code block.
5. "Last step: start a new chat and ask: What's in my guava-hub? Paste or describe the answer here."

## If a check fails
- Says it can't find the hub: check the folder is named exactly "guava-hub" and lives in the Google account they connected. Files shared *with* them from another account may not show up; move the folder into their own Drive.
- Reads the folder but not a file: the file is probably an upload rather than a Google Doc. Open it and use File, then Save as Google Docs.
- On a Google Workspace account, the admin may have to allow the connector first.
