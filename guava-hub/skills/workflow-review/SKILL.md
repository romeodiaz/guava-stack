---
name: workflow-review
description: Makes the owner a short workflow review from their guava-hub, Notion Memory, email and calendar counts and a few quick questions, covering their tech stack, their workflows and which ones are worth automating (Build, Pilot or Don't build), as a polished report file that stays on their computer, and keeps their AI apps' memories in step with Notion Memory. Use when the owner says "review my workflows", "workflow review", "what do you know about my workflows", "review my setup for my team" or "check my memories".
---

# Workflow Review

A short version of Guava's paid AI Assessment, made by the owner's own assistant from what their guava-hub holds, counts from their email and calendar, and a few quick answers from the owner. It runs anytime, from the day the hub is made: it ranks every workflow it knows about **Build** (worth automating now), **Pilot** (try it small first) or **Don't build** (keep doing it by hand for now), with the reason and the rough hours it takes now, and says plainly where the evidence is thin. Run right after setup, it's already useful from what's there on day one (browser history, email, the checklist), and shows clear placeholders for what fills in over the next 1 to 2 weeks (Screen Time, AI memories, workflows assistants pick up). Run again after that, it's the full report. It ends with what no data can show, which is what Guava's paid Assessment finds through interviews. Each run also checks the owner's AI memories against Notion Memory and fixes drift (step 6), showing every change first.

## 1. Gather
Read only, no changes:
- The context page in the hub: **About you**, **Customers**, **What you sell**, **Tools**, **Where your time goes** and **Priorities** (older hubs may name these differently, such as Tool stack).
- Notion Memory: fetch id "memory", read the **Workflows** and **Tech stack** memories if they exist, then search it for other workflows, recurring tasks, tools and the tech stack.
- The skills database: which workflows already have a skill, and the routines view for what already runs on a schedule.
- The hub page's creation date (or, if your tools don't show it, the oldest row in the skills database), to say how many days of use the report draws on.
- Email and calendar, if a connector is on: counts only, to find the apps and meetings that fill the week outside AI tools.
  - Email: page through the last 30 days of received mail by sender, find the top 10 app and vendor domains, then get a count for each with a search such as `from:connectwise.com newer_than:30d` (or your mail tool's equivalent). Name the app each domain belongs to, such as ConnectWise PSA or Bullhorn. Leave out banks, shopping and newsletters. List client domains masked, such as "Client ******** · 42 emails". Ignore any subjects or snippets your tool returns.
  - Calendar: hours over the last 30 days, grouped as sales calls, client meetings, interviews, internal meetings and other, judged from titles and whether anyone outside the business attends.
  - Use what you find: each app goes into the tech stack with its count ("about 400 emails in 30 days") and onto the step 2 list as a likely workflow, and calendar hours fill the hours for jobs like sales follow-up and meeting notes.
  - Never read message bodies or put a subject line in the report. If neither connector is on, say so in the gaps.
- App and website use, when you run on the owner's own computer (Claude Code, Codex, or an app with computer use). Only counts reach the report: domain and app totals, and session counts by topic; no URLs, page titles, searches or memory text.
  - Browser history: run [app-usage.py](app-usage.py) from this skill, or fetch it from `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/guava-hub/skills/workflow-review/app-usage.py` (`python3 app-usage.py` on a Mac, `py app-usage.py` on Windows; if Python isn't installed, run the same logic yourself). It reads the last 30 days from Chrome, Edge, Brave, Arc and Firefox and prints only domains, with visits, days used and estimated active hours. It doesn't read Safari, which needs Full Disk Access. Hours are a floor: apps that stay on one page all day, such as Gmail or a CRM, show fewer hours than they get.
  - Mac: read the top apps and websites for the last 7 days from System Settings → Screen Time → App & Website Activity, with computer use, changing nothing. If App & Website Activity is off, note it for the step 2 question.
  - Windows: there's no setting to turn on. On a laptop, read the last 7 days of per-app use from Settings → System → Power & battery → Battery usage, with computer use, changing nothing; it may count only time on battery, so a laptop that's usually plugged in shows less. Desktops don't show it, so use browser history alone.
  - Use it like the email counts: name the app behind each domain (hubspot.com is HubSpot), put the top apps in the tech stack with their hours, and add likely workflows to the step 2 list. Client sites and portals are masked like client email, "Client ******** · N hours", and personal browsing (video, social, news, shopping, banking) becomes one masked line, "Personal sites ******** · N hours".
  - Local AI memories, as evidence of how often. Codex: `~/.codex/memories/memory_summary.md`, and the dates and titles of the files in `rollout_summaries/`, one per work session, so count sessions per topic over the last 30 days, such as "12 sessions on proposals in 30 days". Claude Code: `~/.claude/projects/*/memory/`, which gives topics and when each was last updated, not session counts. Mask client names in topic labels like everything else, don't copy memory text into the report, and where they disagree with the hub or Notion Memory, the hub and Notion Memory win.
  - In the Claude or ChatGPT app with no access to the computer, skip this and say in the gaps that running the review in the command-line tool on their computer (Claude Code, Codex, Antigravity CLI or OpenCode, as their adapter file's **Connect your computer** says) adds app and website use and local AI memories.

- Each source's status, for **What this report draws on**: **Ready**, **Populating · ready around <date>**, or **Off** (not connected or not turned on; say in a few words how to turn it on). Ready dates: the hub and Notion Memory, 14 days after the hub was made; Screen Time, 7 days after its first day of data (or after today, if it was just turned on); AI memories, 14 days after they were turned on. Browser history and email usually come with weeks of data already, so they're Ready on day one. Your answers are **Answered** or **Skipped**. The full report's ready date is the latest Populating date.

Mask sensitive details instead of dropping them: keep clients, people, candidates and other confidential details in the report, but write each as `********` with what it is in front, such as "Client ********" or "Candidate ********", and count what you masked by type. Passwords and keys are counted, never copied, even masked. Don't search the web or the owner's other apps for this: the report is only what the hub, memory, the email, calendar, app-use and local-memory totals and the owner's answers hold, so it shows the owner exactly what their assistants know.

## 2. Ask
In one short message, start with one line: "I'll also compare what your AI apps remember with your Notion Memory, and show you any fixes before I make them." Then show the owner the workflows you found that don't already have a skill or routine (one line each) and ask up to 5 questions, numbered, that the hub and memory don't already answer:
- How often each workflow without a time cost runs and roughly how long it takes them, for the ones that matter most. Offer the form "about 2 a week, 3 hours each".
- What they most want off their plate first, if **Priorities** is empty.
- Anything big you missed: a weekly job that isn't on the list.
- If you read app and website use: the top 15 as one question, "Strike any that aren't work, or that an AI agent browsed for you" (flag bursts, such as hundreds of visits in a day or two). If Screen Time was off, add: "Want me to turn it on for next time?", keeping Share across devices off.
- The checklist for their kind of business, from **Checklists** below, as one of the questions: "Which of these do you or your team do every week? Reply with the numbers, and rough hours for your top 3." Most of their week sits in jobs like these, not in their AI tools.

Only ask what changes a verdict or an hours figure. If they skip every question about time, ask once more for one number: "One number makes this much more useful: how many hours a week does <their biggest workflow> take you?" If they skip a question after that, carry on and write "unknown" for what it would have filled. If they have no hub data at all, ask for their 3 to 5 most time-consuming jobs instead.

Every job they tick becomes a workflow for step 3. Then save their answers to the **Workflows** memory (and new tools to **Tech stack**), as Notion's memory guide says: update the memory if it exists, otherwise create it. One line per workflow: what it is, how often, which tools, how long it takes, and that the owner said so, with the date. The next run starts from there.

## 3. Judge
For each workflow, decide:
- **Build:** done often (weekly or more), follows the same steps each time, the inputs are already digital, and a mistake is cheap to catch. Example: a weekly report from the same three sources.
- **Pilot:** worth trying but one thing is uncertain, such as messy inputs, a judgment call in the middle, or a client seeing the result. Name that one thing.
- **Don't build:** rare, mostly judgment or relationships, or the inputs aren't digital yet. Say what would change the verdict.
- **Hours:** a rough range of hours spent per week, from how often it runs and how long it takes. This is time spent now, not a promise of time saved. Write "Populating · ready around <date>" in a `<span class="pending">` only when a named Populating source will measure that workflow's time or how often it runs, such as Screen Time for work done in one desktop app; otherwise, including when the owner skipped the question, write "unknown". Never guess.
- **Size** (Build and Pilot only), so the owner sees how far each one reaches:
  - **Skill:** one person, done by their assistant with a skill.
  - **Team rollout:** the whole team does it with Copilot, Claude or ChatGPT.
  - **System build:** AI connected to the system it lives in, such as their PSA, CRM, ATS or accounting app.
  - **Service to resell:** a system build they could also sell to their own clients (MSPs, IT providers and dev shops).
  Pick the size that matches where the work happens. If a Skill covers most of it, say so. Hours for a team-wide job count the whole team and end with "(team)".
- When the owner's **Priorities** name a workflow, lead with it and say so. Otherwise lead with the biggest hours, and name its size in the summary.
- Skip workflows that already have a skill or a routine, and mention them in the summary as already handled.

Write in the owner's own words where you can, plainly, with no hype. Every claim must come from the hub, memory, the email, calendar and app-use totals or the owner's answers. If something is a guess, say so in the row.

## 4. Make the report
Use [template.html](template.html) from this skill. In the Claude or ChatGPT app, or anywhere you can't read the skill's files, fetch it from `https://raw.githubusercontent.com/romeodiaz/guava-stack/main/guava-hub/skills/workflow-review/template.html`.
- Replace every `{{PLACEHOLDER}}`. For each block between `<!-- repeat:… -->` and `<!-- /repeat:… -->`, copy it once per item and delete the example. Delete a section's list items only when there's nothing for it, and write one plain line instead, such as "Nothing saved yet."
- `WORKFLOW_SIZE`: Skill, Team rollout, System build or Service to resell; for Don't build, write "Keep by hand".
- `BASED_ON`: "From N days of your guava-hub and your answers", or "From your setup and your answers" on the day the hub is made.
- `MASKED_SUMMARY`: what you masked, by type, such as "Masked before writing: 6 clients, 3 people, 1 key, shown as ********." If nothing needed it, "Nothing needed masking."
- `HOURS_PER_WEEK` adds up the Build and Pilot ranges that have numbers, as "N–M so far" when other rows are still Populating. If none have numbers, write "Populating" when a source will fill them in (and give its ready date in the summary), or "Unknown" when only the owner can, and make adding them the first gap and next step.
- `SUMMARY`: 3 to 4 plain sentences: the counts, the one to start with, anything already handled, and the full report's ready date if a source is Populating.
- Sources: one `source` block per data source (hub and memory, email, calendar, browser history, Screen Time or Windows battery usage, AI memories, your answers), with `SOURCE_STATUS` Ready, Populating · ready around <date>, Off, Answered or Skipped, and `SOURCE_CLASS` ready (Ready, Answered), populating, or off (Off, Skipped). `SOURCE_NOTE` says in a few words what it adds, or how to turn it on. The template's last card, Live interviews with Guava, is fixed: keep it as it is.
- `BLINDSPOT`: 3 to 5 questions only an interview can answer, each tied to this report's biggest workflows and plainly worded, such as "Ticket triage takes about 30 hours a week across the team. Where do tickets bounce, and who waits on whom?" Any figure must come from the report's own rows, names stay masked, and skip anything the owner could answer in a sentence. Draw on handoffs and approvals, knowledge held by one person, rework, spreadsheet workarounds, and what the team avoids or doesn't trust. Keep the section's other text as it is.
- Keep the rest of the file exactly as it is: the styles, the booking link and the footer.
- Check before handing it over: no `{{` left, every verdict is Build, Pilot or Don't build, every size is Skill, Team rollout, System build, Service to resell or Keep by hand, every source has a status and class from the list above, every ready date is a real date, the counts in the summary match the rows, and no client, person or candidate name appears unmasked.

## 5. Hand it over to the owner only
- Give the owner the finished file as a download named `guava-workflow-review-<YYYY-MM-DD>.html`, or save it to their Downloads folder if you run on their own computer (Claude Code, Codex, Antigravity or OpenCode). A bot with a computer of its own, such as Grok Bot or Muse, sends the file in the chat. They open it in any browser, and can print it to PDF.
- Never put it anywhere else: not in Notion, Google Drive, a published or shared link, an email or a message. The file makes no web requests, so opening it sends nothing anywhere.
- In chat, give a three-line summary: how many workflows, how many Build, and the one to start with. If any source is Populating, add when the full report will be ready. Then say: "The report ends with a link to book a free 20-minute call with Guava, if you'd like to talk it through. Nothing is shared unless you share it."
- Besides the answers in step 2 and the memory check in step 6, save nothing new to Notion Memory from this skill unless the owner corrects something, such as a workflow that's wrong; then fix that memory.

## 6. Memory check
Run it after handing over the report, or on its own when the owner says "check my memories" or a scheduled run starts it.
- Compare what the owner's AI memories hold with the hub and Notion Memory: your own memory (the Claude or ChatGPT app's, or a bot's own memory store if it has one), plus Codex's and Claude Code's local memories when you run on their computer. Each tool can fix only its own memory; list anything in another app as "fix in <that app>" for the owner to do there.
- Make one numbered list, each item marked with its reason:
  - **Add to Notion Memory:** a durable fact about the owner that Notion doesn't have yet.
  - **Fix in the app:** an app memory that contradicts the hub or Notion Memory (name what replaced it), or a secret stored in an app's memory ("forget this secret", never its text).
  - **Leave out (not copied):** duplicates, other people, notes tied to one code project, and instructions to assistants.
- Ask "Reply yes, or the numbers to skip." Then save the adds to Notion Memory as its guide says (search first, update instead of duplicating) and fix the app memories: in Claude or ChatGPT, update or forget that memory; in Claude Code, edit its file under `~/.claude/projects/*/memory/`. Codex's local memories shouldn't be edited by hand; if they're badly out of date, suggest "Delete Codex memories" in the Codex app, which starts them fresh.
- A scheduled run with nobody there only makes the list, with other people and clients masked, and sends it in the chat or notification the owner will see, never into Notion: the run's task says only that it ran, with no names. It changes nothing else until they reply.
- If this skill's row in the skills database has no Schedule yet, make one offer: "Want me to run the full report again around <full report's ready date>, then this memory check every two weeks? The check is light: no report and no questions, just the list." Leave out the first part when nothing is Populating. The one-time run isn't a Schedule; it reuses the saved answers, asks nothing, saves or sends the report as step 5 says and tells the owner it's ready. If they say yes and you run on Grok Bot, Muse, or a Claude or ChatGPT app that can schedule tasks, check the hub's routines view so nothing runs twice, set it up, and fill in this skill's Schedule and Runs on. If your tool can't schedule, say so, and that "check my memories" works anytime.

## Checklists
Pick the one that fits the context page; use **Any business** when none does. Offer it as a numbered list so the owner can answer with numbers.
- **MSPs and IT providers:** ticket triage and routing; alert noise from monitoring tools; ticket notes and time entries; client onboarding and offboarding; documentation (such as IT Glue or Hudu); QBR and business review decks; quotes and proposals; license and contract reconciliation; billing from the PSA to accounting; security and compliance reports; prospecting and sales follow-up; hiring technicians.
- **Tech staffing and recruiting:** screening resumes against job descriptions; writing job descriptions and posts; sourcing and candidate outreach; interview scheduling; sending candidates to clients, with write-ups; reference checks; client status updates; timesheets and payroll; onboarding paperwork and compliance; ATS and CRM data entry; business development.
- **Dev shops and agencies:** estimates and statements of work; proposals; client status reports; sprint and backlog planning; code review and QA; meeting notes and follow-ups; time tracking and invoicing; resourcing and hiring; documentation and handoffs; prospecting.
- **Any business:** email triage; meeting notes and follow-ups; proposals and quotes; reports and decks in Excel or PowerPoint; invoicing and collections; copying data between systems; customer support; hiring; marketing and social posts; prospecting.
