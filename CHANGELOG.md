# Changelog

Owner Mode version history.

- 2026-10-14 (setup only): Setup now walks owners step by step through connecting Notion and adding the hub instruction in the Claude and ChatGPT apps, then checks both work. The Owner Mode rules are unchanged.
- v1.7.0 (2026-10-14): The plugin now uses only its own bundled files: no live fetching of instructions. Rule 17 summarizes humanizer principles and links blader's humanizer skill instead of fetching it. Setup asks before every edit or install and asks the owner to paste or export context from other AI tools. Changelog moved here.
- v1.6.1 (2026-10-14): Moved the files into the skills/ folder. The rules are unchanged.
- v1.6.0 (2026-10-14): Rule 21 now scans third-party skills with [Cisco Skill Scanner](https://github.com/cisco-ai-defense/skill-scanner) before installing them.
- v1.5.0 (2026-10-14): Rule 17 now runs final copy through the live [humanizer skill](https://github.com/blader/humanizer) by blader, fetched fresh each time.
- v1.4.0 (2026-10-14): Rule 4 now asks for all decisions at once as a numbered list with a recommended answer for each. New rule 23 keeps passwords, keys and personal details out of notes and handoffs. Both ideas come from [Matt Pocock's skills](https://github.com/mattpocock/skills).
- v1.3.0 (2026-10-14): Simplified the repo to a few files. The rules haven't changed since v1.0.0.
- v1.0.0 (2026-10-14): First release of the 22 rules, adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack).
