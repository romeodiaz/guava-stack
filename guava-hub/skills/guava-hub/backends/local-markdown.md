# Hub backend: local Markdown or Obsidian

For owners who want their hub only on their own computer: private client work, a client that can't put its details in Notion, Google or Microsoft, or anyone who'd rather not have a cloud account involved. The hub is a plain folder of Markdown files. Obsidian is optional; it's just a nicer way to read and edit the same folder.

**Hub instruction line:** `Load my guava-hub first: the "guava-hub" folder at <path>.` Fill in the full path, for example `~/Documents/guava-hub`.

## Before you pick this hub
Tell the owner these trade-offs in plain words before building anything:
- **Only assistants on this computer can read it:** the Claude desktop app's Code tab (Local sessions), Claude Code and Codex. Grok Bot, Muse, Code tab cloud sessions and the Claude and ChatGPT chat apps run in the cloud and can't reach a folder on the computer. If the owner picked one of those as their day-to-day assistant, recommend the Code tab instead and say why.
- **On the phone:** Remote Control opens the computer's Code tab sessions from the Claude phone app while the computer is on, and those sessions can read the hub. Chat on the phone can't.
- **Private isn't the same as offline.** The files stay on the computer, but the AI still sends the parts it reads to its own service (Anthropic for Claude, OpenAI for Codex) as part of the work, under the owner's plan. For a client that needs nothing to leave the building, the hub is ready, but the AI also has to run on their own hardware. Local models in the router are coming soon: say so plainly and don't present this hub as fully offline yet.

## Build the hub
You need to be running on the owner's computer to build this hub: the Code tab in a Local session, Claude Code or Codex. If you're a chat app, a cloud session or a cloud assistant, say so and ask the owner to paste the Start here line into a Local session in the Claude desktop app's Code tab instead.

1. Ask where the folder should go. Default: `~/Documents/guava-hub`. If the owner already has an Obsidian vault, offer to put the folder inside it instead.
2. Keep it out of cloud-synced folders (iCloud Drive, Dropbox, OneDrive, Google Drive) unless the owner wants it synced between their own computers and is fine with that service holding a copy. Never put it inside a folder that's shared, published or pushed to GitHub.
3. Create the folder with:
   - **`Profile & Context.md`**: start it with the Stack settings section from the setup skill, then the owner's interview answers. In Stack settings, write the hub line as `- Hub: Local Markdown (<path>)`, or `- Hub: Obsidian (<path>)` if they use Obsidian.
   - **`Rules.md`**
   - **`Skills/`**: one Markdown file per skill, named after the skill (for example `Skills/humanizer.md`). Start each with a short header, then the steps:
     ```
     ---
     name: humanizer
     description: One line on when to use it.
     ---
     ```
     Every skill in this folder counts as turned on. To turn one off, move it to a sibling folder called **`Skills (off)`**.
4. **Obsidian (optional):** if the owner wants it, have them install Obsidian from obsidian.md, choose **Open folder as vault** and pick the hub folder (or their existing vault). Skip community plugins for this vault, and leave Obsidian Sync and Publish off unless they ask for them.

## Connect the apps
There are no connectors. Each assistant on the computer reads the folder directly, so this step gives each one permission and the hub instruction line. Do Claude first, then Codex, one step at a time, showing each change and waiting for a yes.

Claude (the desktop app's Code tab and Claude Code):
1. Back up `~/.claude/settings.json`, then add the hub folder's full path (for example `/Users/<name>/Documents/guava-hub` on a Mac, or `C:\Users\<name>\Documents\guava-hub` on Windows) under `permissions.additionalDirectories` so every session can read it without asking. Show the exact lines first.
2. Add the hub instruction line, with the real path, in a short section at the end of `~/.claude/CLAUDE.md`, even with the guava-hub plugin installed: its start-up hook tells each session to load the hub, but only this line says where the folder is. Without the plugin, add the rest of the standing instructions there too. Never replace what's already in the file.
3. "Start a new Local session in the Code tab and ask: What's in my guava-hub? Paste or describe the answer here."

Codex (only if it's in the owner's AI setup):
1. Add the hub instruction line, with the real path, in a short section at the end of `~/.codex/AGENTS.md`. Create the file if it doesn't exist; never replace what's in it.
2. Test it with `codex exec --skip-git-repo-check "What's in my guava-hub?" < /dev/null`. Codex can read the folder; leave hub edits to Claude or the owner.

Skip the Claude and ChatGPT app steps and the phone chat check in setup step 4: those apps can't reach this hub. If the owner wants the phone, set up Remote Control (see `assistants/claude.md`) and check one session from the Claude phone app.

## If a check fails
- Says it can't find the hub: check the path in the hub instruction line matches the folder exactly, including spaces and capitals, and that the folder holds `Profile & Context.md`.
- Asks permission to read the folder every time: the `additionalDirectories` line is missing or has a different path. Fix it and start a new session.
- Works in a Local session but not a cloud one: expected. Cloud sessions can't see the computer's files.
- Obsidian shows the files but the assistant doesn't: the vault and the hub may be different folders. Point the hub instruction line at the folder that holds `Profile & Context.md`.
