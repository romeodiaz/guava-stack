---
name: free-ai-assessment
description: Makes the owner a free, short AI Assessment from their guava-hub, Notion Memory, email and calendar counts and a few quick questions, covering their tech stack, their workflows and which ones are worth automating (Build, Pilot or Don't build), as a polished report file that stays on their computer. Use when the owner says "run my free AI assessment", "free AI assessment", "what do you know about my workflows", "review my workflows" or "review my setup for my team".
---

# Free AI Assessment

A short version of Guava's paid AI Assessment, made by the owner's own assistant from what their guava-hub holds, counts from their email and calendar, and a few quick answers from the owner. It runs anytime, from the day the hub is made: it ranks every workflow it knows about **Build** (worth automating now), **Pilot** (try it small first) or **Don't build** (keep doing it by hand for now), with the reason and the rough hours it takes now, and says plainly where the evidence is thin. It gets sharper the longer the owner uses their assistants, so they can run it again anytime.

## 1. Gather
Read only, no changes:
- The context page in the hub: **About you**, **Customers**, **What you sell**, **Tools**, **Where your time goes** and **Priorities** (older hubs may name these differently, such as Tool stack).
- Notion Memory: fetch id "memory", read the **Workflows** and **Tech stack** memories if they exist, then search it for other workflows, recurring tasks, tools and the tech stack.
- The skills database: which workflows already have a skill, and the routines view for what already runs on a schedule.
- The hub page's creation date (or, if your tools don't show it, the oldest row in the skills database), to say how many days of use the report draws on.
- Email and calendar, if a connector is on: counts only, to find the apps and meetings that fill the week outside AI tools.
  - Email: page through the last 30 days of received mail by sender, find the top 10 app and vendor domains, then get a count for each with a search such as `from:connectwise.com newer_than:30d` (or your mail tool's equivalent). Name the app each domain belongs to, such as ConnectWise PSA or Bullhorn. Leave out people, banks, shopping and newsletters, and count mail from clients as one line, "client email: N", never by domain. Ignore any subjects or snippets your tool returns.
  - Calendar: hours over the last 30 days, grouped as sales calls, client meetings, interviews, internal meetings and other, judged from titles and whether anyone outside the business attends.
  - Use what you find: each app goes into the tech stack with its count ("about 400 emails in 30 days") and onto the step 2 list as a likely workflow, and calendar hours fill the hours for jobs like sales follow-up and meeting notes.
  - Never read message bodies, and never put a subject line, a person's name or a client's name in the report. If neither connector is on, say so in the gaps.

Leave out anything about other people, clients' confidential details, passwords and keys. Don't search the web or the owner's other apps for this: the report is only what the hub, memory, the email and calendar counts and the owner's answers hold, so it shows the owner exactly what their assistants know.

## 2. Ask
In one short message, show the owner the workflows you found that don't already have a skill or routine (one line each) and ask up to 5 questions, numbered, that the hub and memory don't already answer:
- How often each workflow without a time cost runs and roughly how long it takes them, for the ones that matter most. Offer the form "about 2 a week, 3 hours each".
- What they most want off their plate first, if **Priorities** is empty.
- Anything big you missed: a weekly job that isn't on the list.
- The checklist for their kind of business, from **Checklists** below, as one of the questions: "Which of these do you or your team do every week? Reply with the numbers, and rough hours for your top 3." Most of their week sits in jobs like these, not in their AI tools.

Only ask what changes a verdict or an hours figure. If they skip every question about time, ask once more for one number: "One number makes this much more useful: how many hours a week does <their biggest workflow> take you?" If they skip a question after that, carry on and write "unknown" for what it would have filled. If they have no hub data at all, ask for their 3 to 5 most time-consuming jobs instead.

Every job they tick becomes a workflow for step 3. Then save their answers to the **Workflows** memory (and new tools to **Tech stack**), as Notion's memory guide says: update the memory if it exists, otherwise create it. One line per workflow: what it is, how often, which tools, how long it takes, and that the owner said so, with the date. The next run starts from there.

## 3. Judge
For each workflow, decide:
- **Build:** done often (weekly or more), follows the same steps each time, the inputs are already digital, and a mistake is cheap to catch. Example: a weekly report from the same three sources.
- **Pilot:** worth trying but one thing is uncertain, such as messy inputs, a judgment call in the middle, or a client seeing the result. Name that one thing.
- **Don't build:** rare, mostly judgment or relationships, or the inputs aren't digital yet. Say what would change the verdict.
- **Hours:** a rough range of hours spent per week, from how often it runs and how long it takes. This is time spent now, not a promise of time saved. If nobody has said how long it takes, write "unknown" instead of guessing.
- **Size** (Build and Pilot only), so the owner sees how far each one reaches:
  - **Skill:** one person, done by their assistant with a skill.
  - **Team rollout:** the whole team does it with Copilot, Claude or ChatGPT.
  - **System build:** AI connected to the system it lives in, such as their PSA, CRM, ATS or accounting app.
  - **Service to resell:** a system build they could also sell to their own clients (MSPs, IT providers and dev shops).
  Pick the size that matches where the work happens. If a Skill covers most of it, say so. Hours for a team-wide job count the whole team and end with "(team)".
- When the owner's **Priorities** name a workflow, lead with it and say so. Otherwise lead with the biggest hours, and name its size in the summary.
- Skip workflows that already have a skill or a routine, and mention them in the summary as already handled.

Write in the owner's own words where you can, plainly, with no hype. Every claim must come from the hub, memory, the email and calendar counts or the owner's answers. If something is a guess, say so in the row.

## 4. Make the report
Use [template.html](template.html) from this skill. In the Claude or ChatGPT app, or anywhere you can't read the skill's files, fetch it from `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/guava-hub/skills/free-ai-assessment/template.html`.
- Replace every `{{PLACEHOLDER}}`. For each block between `<!-- repeat:… -->` and `<!-- /repeat:… -->`, copy it once per item and delete the example. Delete a section's list items only when there's nothing for it, and write one plain line instead, such as "Nothing saved yet."
- `WORKFLOW_SIZE`: Skill, Team rollout, System build or Service to resell; for Don't build, write "Keep by hand".
- `BASED_ON`: "From N days of your guava-hub and your answers", or "From your setup and your answers" on the day the hub is made.
- `HOURS_PER_WEEK` adds up the Build and Pilot ranges that have numbers. If none do, write "Unknown" and make adding them the first gap and next step.
- Keep the rest of the file exactly as it is: the styles, the booking link and the footer.
- Check before handing it over: no `{{` left, every verdict is Build, Pilot or Don't build, every size is Skill, Team rollout, System build, Service to resell or Keep by hand, and the counts in the summary match the rows.

## 5. Hand it over to the owner only
- Give the owner the finished file as a download named `guava-ai-assessment-<YYYY-MM-DD>.html`, or save it to their Downloads folder if you run on their own computer (Claude Code or Codex). A bot with a computer of its own, such as Grok Bot or Muse, sends the file in the chat. They open it in any browser, and can print it to PDF.
- Never put it anywhere else: not in Notion, Google Drive, a published or shared link, an email or a message. The file makes no web requests, so opening it sends nothing anywhere.
- In chat, give a three-line summary: how many workflows, how many Build, and the one to start with. Then say: "The report ends with a link to book a free 20-minute call with Guava, if you'd like to talk it through. Nothing is shared unless you share it."
- Besides the answers in step 2, save nothing new to Notion Memory from this skill unless the owner corrects something, such as a workflow that's wrong; then fix that memory.

## Checklists
Pick the one that fits the context page; use **Any business** when none does. Offer it as a numbered list so the owner can answer with numbers.
- **MSPs and IT providers:** ticket triage and routing; alert noise from monitoring tools; ticket notes and time entries; client onboarding and offboarding; documentation (such as IT Glue or Hudu); QBR and business review decks; quotes and proposals; license and contract reconciliation; billing from the PSA to accounting; security and compliance reports; prospecting and sales follow-up; hiring technicians.
- **Tech staffing and recruiting:** screening resumes against job descriptions; writing job descriptions and posts; sourcing and candidate outreach; interview scheduling; sending candidates to clients, with write-ups; reference checks; client status updates; timesheets and payroll; onboarding paperwork and compliance; ATS and CRM data entry; business development.
- **Dev shops and agencies:** estimates and statements of work; proposals; client status reports; sprint and backlog planning; code review and QA; meeting notes and follow-ups; time tracking and invoicing; resourcing and hiring; documentation and handoffs; prospecting.
- **Any business:** email triage; meeting notes and follow-ups; proposals and quotes; reports and decks in Excel or PowerPoint; invoicing and collections; copying data between systems; customer support; hiring; marketing and social posts; prospecting.
