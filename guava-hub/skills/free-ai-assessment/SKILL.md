---
name: free-ai-assessment
description: Makes the owner a free, short AI Assessment from their guava-hub, Notion Memory and a few quick questions, covering their tech stack, their workflows and which ones are worth automating (Build, Pilot or Don't build), as a polished report file that stays on their computer. Use when the owner says "run my free AI assessment", "free AI assessment", "what do you know about my workflows", "review my workflows" or "review my setup for my team".
---

# Free AI Assessment

A short version of Guava's paid AI Assessment, made by the owner's own assistant from what their guava-hub holds plus a few quick answers from the owner. It runs anytime, from the day the hub is made: it ranks every workflow it knows about **Build** (worth automating now), **Pilot** (try it small first) or **Don't build** (keep doing it by hand for now), with the reason and a rough time saving, and says plainly where the evidence is thin. It gets sharper the longer the owner uses their assistants, so they can run it again anytime.

## 1. Gather
Read only, no changes:
- The context page in the hub: **About you**, **Customers**, **What you sell**, **Tools**, **Where your time goes** and **Priorities** (older hubs may name these differently, such as Tool stack).
- Notion Memory: fetch id "memory", read the **Workflows** and **Tech stack** memories if they exist, then search it for other workflows, recurring tasks, tools and the tech stack.
- The skills database: which workflows already have a skill, and the routines view for what already runs on a schedule.
- The hub page's creation date (or, if your tools don't show it, the oldest row in the skills database), to say how many days of use the report draws on.

Leave out anything about other people, clients' confidential details, passwords and keys. Don't search the web or the owner's other apps for this: the report is only what the hub, memory and the owner's answers hold, so it shows the owner exactly what their assistants know.

## 2. Ask
In one short message, show the owner the workflows you found that don't already have a skill or routine (one line each) and ask up to 5 questions, numbered, that the hub and memory don't already answer:
- How often each workflow without a time cost runs and roughly how long it takes them, for the ones that matter most. Offer the form "about 2 a week, 3 hours each".
- What they most want off their plate first, if **Priorities** is empty.
- Anything big you missed: a weekly job that isn't on the list.

Only ask what changes a verdict or an hours figure. If they skip every question about time, ask once more for one number: "One number makes this much more useful: how many hours a week does <their biggest workflow> take you?" If they skip a question after that, carry on and write "unknown" for what it would have filled. If they have no hub data at all, ask for their 3 to 5 most time-consuming jobs instead.

Then save their answers to the **Workflows** memory (and new tools to **Tech stack**), as Notion's memory guide says: update the memory if it exists, otherwise create it. One line per workflow: what it is, how often, which tools, how long it takes, and that the owner said so, with the date. The next run starts from there.

## 3. Judge
For each workflow, decide:
- **Build:** done often (weekly or more), follows the same steps each time, the inputs are already digital, and a mistake is cheap to catch. Example: a weekly report from the same three sources.
- **Pilot:** worth trying but one thing is uncertain, such as messy inputs, a judgment call in the middle, or a client seeing the result. Name that one thing.
- **Don't build:** rare, mostly judgment or relationships, or the inputs aren't digital yet. Say what would change the verdict.
- **Hours:** a rough range per week, from how often it runs and how long it takes. If nobody has said how long it takes, write "unknown" instead of guessing.
- When the owner's **Priorities** name a workflow, lead with it and say so.
- Skip workflows that already have a skill or a routine, and mention them in the summary as already handled.

Write in the owner's own words where you can, plainly, with no hype. Every claim must come from the hub, memory or the owner's answers. If something is a guess, say so in the row.

## 4. Make the report
Use [template.html](template.html) from this skill. In the Claude or ChatGPT app, or anywhere you can't read the skill's files, fetch it from `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/guava-hub/skills/free-ai-assessment/template.html`.
- Replace every `{{PLACEHOLDER}}`. For each block between `<!-- repeat:… -->` and `<!-- /repeat:… -->`, copy it once per item and delete the example. Delete a section's list items only when there's nothing for it, and write one plain line instead, such as "Nothing saved yet."
- `BASED_ON`: "From N days of your guava-hub and your answers", or "From your setup and your answers" on the day the hub is made.
- `HOURS_PER_WEEK` adds up the Build and Pilot ranges that have numbers. If none do, write "Unknown" and make adding them the first gap and next step.
- Keep the rest of the file exactly as it is: the styles, the booking link and the footer.
- Check before handing it over: no `{{` left, every verdict is Build, Pilot or Don't build, and the counts in the summary match the rows.

## 5. Hand it over to the owner only
- Give the owner the finished file as a download named `guava-ai-assessment-<YYYY-MM-DD>.html`, or save it to their Downloads folder if you run on their own computer (Claude Code or Codex). A bot with a computer of its own, such as Grok Bot or Muse, sends the file in the chat. They open it in any browser, and can print it to PDF.
- Never put it anywhere else: not in Notion, Google Drive, a published or shared link, an email or a message. The file makes no web requests, so opening it sends nothing anywhere.
- In chat, give a three-line summary: how many workflows, how many Build, and the one to start with. Then say: "The report ends with a link to book a free 20-minute call with Guava, if you'd like to talk it through. Nothing is shared unless you share it."
- Besides the answers in step 2, save nothing new to Notion Memory from this skill unless the owner corrects something, such as a workflow that's wrong; then fix that memory.
