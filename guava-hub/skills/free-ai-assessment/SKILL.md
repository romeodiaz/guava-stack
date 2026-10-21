---
name: free-ai-assessment
description: Makes the owner a free, short AI Assessment from their guava-hub and Notion Memory: their tech stack, the workflows assistants have picked up, and which ones are worth automating (Build, Pilot or Don't build), as a polished report file that stays on their computer. Use when the owner says "run my free AI assessment", "free AI assessment", "what do you know about my workflows", "review my workflows" or "review my setup for my team".
---

# Free AI Assessment

A short version of Guava's paid AI Assessment, made by the owner's own assistant from what their guava-hub already holds. It does two jobs:
- **Day 1 check-in** (fewer than 14 days since the hub was made): shows what the assistant has picked up about the owner's tech stack and workflows so far, and what it still doesn't know, so the owner can see it's keeping track.
- **Workflow review** (14 days or more): ranks each captured workflow, however few there are, and says plainly where the evidence is thin, **Build** (worth automating now), **Pilot** (try it small first) or **Don't build** (keep doing it by hand for now), with the reason and a rough time saving.

The owner can ask for either one anytime. Use the one that fits and say which in one line.

## 1. Gather
Read only, no changes:
- The context page in the hub: **About you**, **Customers**, **What you sell**, **Tools**, **Where your time goes** and **Priorities** (older hubs may name these differently, such as Tool stack).
- Notion Memory: fetch id "memory", then search it for workflows, recurring tasks, tools and the tech stack. Read the **Workflows** and **Tech stack** memories if they exist.
- The skills database: which workflows already have a skill, and the routines view for what already runs on a schedule.
- The hub page's creation date, to tell which kind of report this is.

Leave out anything about other people, clients' confidential details, passwords and keys. Don't search the web or the owner's other apps for this: the report is only what the hub and memory already hold, so it shows the owner exactly what their assistants know.

## 2. Judge
For each workflow (Workflow review only), decide:
- **Build:** done often (weekly or more), follows the same steps each time, the inputs are already digital, and a mistake is cheap to catch. Example: a weekly report from the same three sources.
- **Pilot:** worth trying but one thing is uncertain, such as messy inputs, a judgment call in the middle, or a client seeing the result. Name that one thing.
- **Don't build:** rare, mostly judgment or relationships, or the inputs aren't digital yet. Say what would change the verdict.
- **Hours:** a rough range per week, from how often it runs and how long it takes. Mark it as an estimate. If the owner never said how long it takes, write "unknown" instead of guessing.
- When the owner's **Priorities** name a workflow, lead with it and say so.
- Skip workflows that already have a skill or a routine, and mention them in the summary as already handled.

Write in the owner's own words where you can, plainly, with no hype. Every claim must come from the hub or memory. If something is a guess, say so in the row.

## 3. Make the report
Use [template.html](template.html) from this skill. In the Claude or ChatGPT app, or anywhere you can't read the skill's files, fetch it from `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/guava-hub/skills/free-ai-assessment/template.html`.
- Replace every `{{PLACEHOLDER}}`. For each block between `<!-- repeat:… -->` and `<!-- /repeat:… -->`, copy it once per item and delete the example. Delete a section's list items only when there's nothing for it, and write one plain line instead, such as "Nothing saved yet."
- Day 1 check-in: the workflows table lists what you've picked up, with Verdict "Pilot" and Why "Too early to judge" for each, or leave one row saying none are saved yet. Make the gaps and next steps the main content: what to tell you so the review in two weeks has something to work with.
- Keep the rest of the file exactly as it is: the styles, the booking link and the footer.
- Check before handing it over: no `{{` left, every verdict is Build, Pilot or Don't build, and the counts in the summary match the rows.

## 4. Hand it over to the owner only
- Give the owner the finished file as a download named `guava-ai-assessment-<YYYY-MM-DD>.html`, or save it to their Downloads folder if you run on their own computer (Claude Code or Codex). A bot with a computer of its own, such as Grok Bot or Muse, sends the file in the chat. They open it in any browser, and can print it to PDF.
- Never put it anywhere else: not in Notion, Google Drive, a published or shared link, an email or a message. The file makes no web requests, so opening it sends nothing anywhere.
- In chat, give a three-line summary: how many workflows, how many Build, and the one to start with. Then say: "The report ends with a link to book a free 20-minute call with Guava, if you'd like to talk it through. Nothing is shared unless you share it."
- Save nothing new to Notion Memory from this skill unless the owner corrects something, such as a workflow that's wrong; then fix that memory.
