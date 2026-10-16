# Hub backend: OneDrive or SharePoint

For owners who run their business on Microsoft 365. Use OneDrive for a hub only the owner uses, and a SharePoint site when their team will share it.

**Hub instruction line:** `Load my guava-hub first: the "guava-hub" folder in my OneDrive.` (For SharePoint, name the site instead: `...in the <site name> SharePoint site.`)

## Build the hub
Ask whether the hub goes in OneDrive or in a SharePoint site (and which site). Create a folder called **guava-hub** there with:
- **Profile & Context**: a Word document. Start it with the Stack settings section from the setup skill, then the owner's interview answers.
- **Agent Rules**: a Word document.
- **Skills**: a folder with one Word document per skill, named after the skill and holding its full text (name, one-line description, then the steps). Every skill in this folder counts as turned on. To turn one off, move it to a sibling folder called **Skills (off)**.

Keep the folder private to the owner, or to the site's members, unless they ask to share it more widely.

## Connect the apps
Claude (covers the desktop app, claude.ai and Claude Code, since they share the account):
1. "Open [Claude Connectors](https://claude.ai/customize/connectors)."
2. "Click Discover, then Search (the magnifying glass icon), and search for Microsoft 365. Pick the Microsoft 365 connector (it covers OneDrive and SharePoint), then click Connect."
3. "Sign in with the Microsoft account that holds your guava-hub folder and approve."
4. "Click your initials in the bottom left, then Settings, then Account. Under Instructions for Claude, paste this and save:" then show the hub instruction line in a code block.
5. "Start a new chat. Click + and check Microsoft 365 is turned on under Connectors. Then ask: What's in my guava-hub? Paste or describe the answer here."

ChatGPT:
1. "Now ChatGPT. Open [ChatGPT Plugins](https://chatgpt.com/plugins). Tell me when you're there."
2. "Search for SharePoint or OneDrive (whichever holds your hub) and click Connect (or Install plugin, then Connect)."
3. "Sign in with the Microsoft account that holds your guava-hub folder and approve."
4. "Open [ChatGPT Personalization](https://chatgpt.com/settings/personalization). Under Custom Instructions, paste this in both the ChatGPT box and the Codex box, then save:" then show the hub instruction line in a code block.
5. "Last step: start a new chat and ask: What's in my guava-hub? Paste or describe the answer here."

## If a check fails
- Says it can't find the hub: check the folder name and that it's in the account or site they connected. For SharePoint, check the owner is a member of that site.
- On a work account, a Microsoft 365 admin usually has to approve the Claude or ChatGPT connector before it works. Tell the owner exactly that; don't look for a way around it.
