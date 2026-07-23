# Agent Harness for SafeX Group 54

This repository is the working portfolio for Group 54 during the SafeX Solutions Summer Internship. The project is organized by weekly tasks, with each week kept as a self-contained workspace so group members can contribute without disturbing unrelated work.

Use this file as the common operating guide for any coding agent, including Codex, Claude Code, Cursor, GitHub Copilot coding agents, and other LLM-based assistants.

## Project Context

- Program: SafeX Solutions Summer Internship.
- Group: Group 54.
- Group Leader: Arsalan Qasim.
- Stakeholder: SafeX Solutions internship team and evaluators.
- Purpose: complete weekly group tasks, document the work as portfolio case studies, and maintain a clean shared codebase.
- Current structure:
  - `week1/`: SafeX FAQ chatbot prototype and case-study documentation.
  - `week2/`: Business Automation Research prototype suite with independent member modules.
  - `week3/`: AI Agent Automation Proposal prototype suite with independent member modules.

For full context, read:

- `docs/project-brief.md`
- `docs/team-roster.md`
- `docs/weekly-task-log.md`
- `docs/agent-memory.md`
- `docs/review-checklist.md`

## Repository Structure

```text
safex/
  AGENTS.md
  CLAUDE.md
  README.md
  docs/
    agent-memory.md
    project-brief.md
    review-checklist.md
    team-roster.md
    weekly-task-log.md
  .github/
    copilot-instructions.md
  .cursor/
    rules/
      project.mdc
  week1/
    src/
    data/
    docs/
    tests/
  week2/
    src/
      app.py
      modules/
    docs/
    tests/
  week3/
    src/
      app.py
      modules/
    docs/
    tests/
```

## Working Rules

1. Read the relevant week folder before making changes.
2. Keep changes inside the smallest relevant area.
3. Do not refactor unrelated modules.
4. Preserve existing member work unless the request is specifically to update it.
5. Keep generated files, secrets, local environments, and raw private data out of commits.
6. Do not add phone numbers, personal emails, or private contact details to harness docs.
7. Prefer clear documentation and focused tests over broad rewrites.
8. Update `docs/agent-memory.md` when a durable project fact, decision, workflow note, or open question should survive future sessions.

## Week 1 Guide

`week1/` contains the SafeX FAQ chatbot prototype.

The task was to build a small AI/ML prototype for SafeX, such as an FAQ chatbot, social-media engagement forecast model, or data dashboard, then document the approach and results as a portfolio case study.

The selected group project is the FAQ chatbot. It uses a local FAQ knowledge base, text similarity, and a Streamlit interface to answer SafeX-related questions. The work should remain stable unless the user asks for a specific fix or documentation update.

Run from `week1/`:

```bash
pip install -r requirements.txt
streamlit run src/app.py
python -m pytest
```

## Week 2 Guide

`week2/` contains the Business Automation Research prototype suite. Each member owns a separate module under `week2/src/modules/`.

Expected module shape:

```text
week2/src/modules/<module_name>/
  __init__.py
  engine.py
  ui.py
```

Module standards:

- `engine.py` contains module logic, data handling, calculations, model calls, or workflow helpers.
- `ui.py` contains a self-contained Streamlit `render_ui()` function.
- Do not place Streamlit page configuration in module files; keep page-level configuration in `week2/src/app.py`.
- Keep imports relative to the `week2` source layout.
- Keep `week2/src/modules/registry.py` aligned with available modules and visible app routing.

Run from `week2/`:

```bash
pip install -r requirements.txt
streamlit run src/app.py
python -m pytest
```

## Week 3 Guide

`week3/` contains the AI Agent Automation Proposal prototype suite. Each member owns a separate module under `week3/src/modules/`.

Expected module shape:

```text
week3/src/modules/<module_name>/
  __init__.py
  engine.py
  ui.py
```

Run from `week3/`:

```bash
pip install -r requirements.txt
streamlit run src/app.py
python -m pytest
```

## Week 2 Member Modules

| Module | Owner | Week 2 Work |
|---|---|---|
| `invoice_automation` | Arsalan Qasim | Invoice Automation Prototype |
| `attendance` | MUHAMMAD WASIM | Attendance Automation Prototype |
| `hr_proposal` | Muhammad Faozan Mujtaba | HR Automation Proposal |
| `email_assistant` | Shahidullah | AI Email Assistant Prototype |
| `report_generator` | Ali Ammar Haider | AI Report Generator Prototype |
| `resume_screening` | Abdul Haseeb | Resume Screening Prototype |
| `ocr_document` | Hammad Abbas | OCR / Document Processing Prototype |
| `predictive_analytics` | Ali Zaib | Predictive Analytics Mini-Study |
| `invoice_automation` | Malik Sudais | Invoice Automation Prototype assignment listed in source roster. |

## Week 3 Member Modules

| Module | Owner | Week 3 Assignment |
|---|---|---|
| `customer_support_chatbot` | Arsalan Qasim | AI Customer Support Chatbot |
| `email_auto_reply` | MUHAMMAD WASIM | AI Email Automation & Auto-Reply |
| `meeting_summarizer` | Muhammad Faozan Mujtaba | AI Meeting Summarizer & Action-Item Extractor |
| `report_generation_agent` | Shahidullah | Automatic Report Generation Agent |
| `social_media_scheduler` | Ali Ammar Haider | AI Social Media Scheduler & Caption Generator |
| `lead_qualification` | Abdul Haseeb | AI Lead Qualification & Sales Assistant |
| `resume_interview_assistant` | Hammad Abbas | Resume Screening & Interview Assistant |
| `doc_knowledge_assistant` | Ali Zaib | Document Analysis & Knowledge-Base Assistant |
| `proposal_invoice_generator` | Malik Sudais | Invoice / Proposal Generator Agent |

If the roster and code disagree, update `docs/team-roster.md` first with a note under open questions, then adjust code only when the requested ownership is clear.

## Documentation Standards

- Use Markdown for project notes, status summaries, and case studies.
- Keep weekly task history in `docs/weekly-task-log.md`.
- Keep member progress in `docs/team-roster.md`.
- Keep persistent agent notes in `docs/agent-memory.md`.
- Keep review and submission criteria in `docs/review-checklist.md`.
- Keep root `README.md` focused on setup, structure, and high-level project overview.

## Status Tracking

Use these statuses consistently in docs and summaries:

- `Not started`: no visible work yet.
- `In progress`: contributor has started or shared progress.
- `Ready for review`: implementation and documentation are available.
- `Needs changes`: reviewed, but revisions are required.
- `Blocked`: progress is stopped by a specific blocker.
- `No response`: member has not replied or submitted a usable update.
- `Submitted`: final deliverables are available for the week.

Every weekly status update should include:

- member name
- module or task
- current status
- last known update date
- deliverables received
- blocker or follow-up needed

## Code Standards

- Use Python type hints for public functions and classes.
- Keep module interfaces simple and documented.
- Prefer existing package patterns over new frameworks.
- Add tests for behavior changes.
- Use relative paths anchored to the relevant week folder.
- Avoid hardcoded local system paths.
- Keep sample data small and safe for Git.
- Do not commit `.env`, virtual environments, caches, notebooks with secrets, or generated heavy artifacts.

## Review Workflow

Before handing work back:

1. Confirm the changed files are in the intended week/module.
2. Run the narrowest relevant tests or explain why they were not run.
3. Check docs for outdated statuses or assignment names.
4. Check for secrets or private contact details.
5. Summarize what changed, what was verified, and any remaining risk.

## Agent Memory

Use `docs/agent-memory.md` for durable notes that future agents should know. Do not store secrets, phone numbers, personal emails, API keys, or private feedback content there.

Good memory entries:

- confirmed project facts
- assignment decisions
- repo workflow notes
- repeated mistakes to avoid
- unresolved questions
- member progress observations without private contact details

Bad memory entries:

- private contact details
- credentials
- sensitive personal notes
- raw feedback form content
- unverified assumptions written as facts
