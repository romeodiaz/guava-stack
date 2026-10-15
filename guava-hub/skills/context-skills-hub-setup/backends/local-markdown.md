# Hub backend: Obsidian or local Markdown

For owners who want their hub as plain files on their own computer, often inside an Obsidian vault. Nothing leaves their computer unless they choose to sync it.

**Hub instruction line:** `Load my AI Context Hub first: <full path to the hub folder>.`

## Build the hub
Ask where the folder goes. Default to `~/AI Context Hub`, or inside their Obsidian vault if they use one. Create:
- `Profile & Context.md`: start it with the Stack settings section from the setup skill, then the owner's interview answers.
- `Agent Rules.md`
- `Skills/<skill-name>/SKILL.md`: one folder per skill, in the same format as the skills in this repo (a `name` and `description` header, then the steps). Claude Code and Codex use this format too. Every skill in `Skills/` counts as turned on; to turn one off, move it to `Skills (off)/`.

Plain Markdown only. Obsidian links and properties are fine, but don't install Obsidian plugins as part of setup.

## Connect the apps
Only tools running on the same computer can read a local folder: Claude Code, Codex, Cursor and other coding tools. The Claude and ChatGPT web and desktop chats, Grok Bot and Muse run elsewhere and can't see it.

Tell the owner this plainly, then offer three choices:
- **Stay local** (best if they mostly work in Claude Code, Codex or Cursor): skip the app connections. The Model Router step points both CLIs at the folder.
- **Sync it to a private GitHub repo** and connect GitHub in Claude and ChatGPT, so the apps can read it too. Only with a yes, and only if they're comfortable with GitHub.
- **Move to a cloud backend** (Notion, Google Drive or OneDrive/SharePoint) and follow that backend's file instead.

For any app that can reach the folder, add the hub instruction line to its custom instructions and test it by asking "What's in my AI Context Hub?".

## If a check fails
- Can't find the hub: check the path in the instruction line is the full path (no `~` for apps that don't expand it) and the folder name matches exactly.
- Claude Code reads it in a chat but not in a non-interactive run: see the Model Router's "Never skip the hub" step.
