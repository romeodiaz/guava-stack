# Grok Bot template wrapper

The Grok Bot template for Owner Mode and the AI Context & Skills Hub is a thin wrapper around this repo. These files are the template's built-in memories and skills, kept here so every platform's wrapper stays in sync.

- `memories.md`: the 3 standing memories
- `skills/getting-started-hub.md`: the first conversation
- `skills/ai-context-hub-setup.md`: runs `hub-setup/SETUP.md`
- The Owner Mode skill runs `owner-mode/PROMPT.md` and `owner-mode/RULES.md`

To port to another assistant, copy these into that platform's memory, skills or custom instructions.
