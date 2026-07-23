# Weekly Task Log

This file documents what Group 54 was asked to build each week, how the work is organized, and how member contributions should be tracked.

## Week 1 - SafeX AI/ML Prototype

### Original Task

Build a small AI/ML prototype for SafeX, for example:

- FAQ chatbot for safexsolutions.com or SafeX-related information.
- Social-media engagement forecast model.
- Data dashboard using real or sample data.

Also document the approach and results as a portfolio case study.

Group leader responsibility:

- consolidate the group's weekly submissions
- send a short summary to the Team Lead by Friday
- submit anonymous feedback on the Team Lead / overall program through the feedback form

### Group Direction

Group 54 selected the FAQ chatbot prototype.

### What Was Built

The Week 1 workspace contains a local SafeX FAQ chatbot with:

- FAQ data in JSON format
- text similarity matching
- chatbot response logic
- Streamlit interface
- evaluation scripts and tests
- portfolio case-study documentation

### How It Was Built

Primary approach:

- Store FAQ content in `week1/data/faq.json`.
- Load and normalize FAQ entries through the knowledge base layer.
- Use vector similarity to match user questions with the closest FAQ answer.
- Render the chatbot through Streamlit.
- Validate expected responses through tests and evaluation questions.

Important files:

- `week1/src/app.py`
- `week1/src/chatbot.py`
- `week1/src/knowledge_base.py`
- `week1/src/similarity.py`
- `week1/data/faq.json`
- `week1/docs/Case_Study.md`
- `week1/docs/Evaluation.md`
- `week1/evaluation/benchmark.py`
- `week1/tests/test_chatbot.py`

### Week 1 Member Tracking

| Member | Contribution Area | Evidence | Status | Notes |
|---|---|---|---|---|
| Arsalan Qasim | Group consolidation and FAQ chatbot contribution | `week1/` project files and docs | Submitted | Consolidated group summary. |
| MUHAMMAD WASIM | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Muhammad Faozan Mujtaba | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Shahidullah | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Ali Ammar Haider | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Abdul Haseeb | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Hammad Abbas | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Ali Zaib | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |
| Malik Sudais | FAQ chatbot group contribution | Pending detail | Submitted | Add exact contribution if later confirmed. |

## Week 2 - Business Automation Research

### Original Task

Each member designs, builds, and documents one component of the Business Automation Research project. Each module should continue the group's Week 1 work and integrate cleanly with the other modules.

Common deliverables:

- Jupyter notebook or script with sample input/output.
- Source code or working files for the assigned module.
- Short written documentation explaining what was built, how it works, and how to run or view it.
- Screenshots or a short recording of the module working.
- GitHub repository updates.
- Final working demo.
- Progress report.
- Mandatory explanation video, 5-15 minutes, HD, face visible, covering architecture, challenges, tools used, and working demo.

Common technologies:

- Python
- Pandas / NumPy
- NLP libraries such as spaCy or NLTK, or an LLM API
- Flask or FastAPI where applicable
- Streamlit for local module demos
- WhatsApp Business API or Twilio where applicable

### Group Direction

Group 54 organized Week 2 as a modular business automation suite under `week2/`.

The shared Streamlit app routes to member-owned modules. Each module should stay isolated so members can work without duplicating or overwriting each other's work.

### Module Assignments

| Member | Module | Objective | Difficulty |
|---|---|---|---|
| Arsalan Qasim | Invoice Automation Prototype | Research and prototype a workflow that auto-generates and sends invoices for a sample small business. | Advanced |
| MUHAMMAD WASIM | Attendance Automation Prototype | Design an automated attendance-tracking workflow, such as QR or geofence check-in, for a sample organization. | Advanced |
| Muhammad Faozan Mujtaba | HR Automation Proposal | Propose and partially prototype an automated onboarding or leave-request workflow for a sample business. | Intermediate |
| Shahidullah | AI Email Assistant Prototype | Build a small prototype that drafts reply suggestions for common customer emails. | Advanced |
| Ali Ammar Haider | AI Report Generator Prototype | Build a script that turns raw sample data into a formatted weekly report. | Intermediate |
| Abdul Haseeb | Resume Screening Prototype | Build a small tool that scores sample resumes against a job description using keyword or embedding matching. | Advanced |
| Hammad Abbas | OCR / Document Processing Prototype | Build a prototype that extracts structured fields from a scanned sample document using OCR. | Intermediate |
| Ali Zaib | Predictive Analytics Mini-Study | Use a small sample or public dataset to build a simple predictive model and report findings. | Advanced |
| Malik Sudais | Invoice Automation Prototype | Source roster lists this assignment; confirm whether it is shared or separate. | Intermediate |

### Week 2 Workspace

Important files:

- `week2/src/app.py`
- `week2/src/config.py`
- `week2/src/modules/registry.py`
- `week2/src/modules/attendance/`
- `week2/src/modules/email_assistant/`
- `week2/src/modules/hr_proposal/`
- `week2/src/modules/invoice_automation/`
- `week2/src/modules/ocr_document/`
- `week2/src/modules/predictive_analytics/`
- `week2/src/modules/report_generator/`
- `week2/src/modules/resume_screening/`
- `week2/docs/Weekly/Week2_Status_Report.md`

### How Week 2 Is Built

Each module should provide:

- an `engine.py` for core workflow logic
- a `ui.py` with a `render_ui()` Streamlit entrypoint
- module-level documentation where needed
- sample inputs and outputs
- screenshots or recordings for evidence
- tests for core logic where practical

### Week 2 Progress Tracking

Use `docs/team-roster.md` as the source for member-level progress. Use `week2/docs/Weekly/Week2_Status_Report.md` for the weekly consolidated summary.

When a member is not responding:

1. Mark the status as `No response` only after a follow-up date is known.
2. Add the first and second follow-up dates.
3. Record the exact deliverables missing.
4. Keep notes factual and professional.

## Week 3 - AI Agent Automation Proposal Suite

### Original Task

Each member designs, builds, and documents an AI agent prototype for a specific business automation domain and target company.

Common deliverables:

- Working prototype (script or hosted demo).
- Prompt template / architecture documentation & diagrams.
- Sample dataset / inputs and before-after outputs.
- Weekly Progress Report (PDF) & Daily Work Log.
- Demo Video (5-10 min, HD, face visible).
- Presentation Slides & Problems Encountered writeup.

### Group Direction

Group 54 organized Week 3 as an AI Agent Automation Proposal Suite under `week3/`.
The shared Streamlit app routes to member-owned modules, providing clean isolation and consistent UI styling.

### Module Assignments

| Member | Module Key | Assigned Project | Scope Summary |
|---|---|---|---|
| Arsalan Qasim | `customer_support_chatbot` | AI Customer Support Chatbot | Map 12+ queries, build intent classifier + escalation rules, 10+ query test benchmark with accuracy score. |
| MUHAMMAD WASIM | `email_auto_reply` | AI Email Automation & Auto-Reply | Collect 15-20 queries, prompt templates, draft reply generation, human-review step. |
| Muhammad Faozan Mujtaba | `meeting_summarizer` | AI Meeting Summarizer & Action-Item Extractor | Process meeting transcripts, extract summary, decisions, action items with owners & deadlines. |
| Shahidullah | `report_generation_agent` | Automatic Report Generation Agent | Read operational CSVs, generate narrative written report using LLM + embedded charts. |
| Ali Ammar Haider | `social_media_scheduler` | AI Social Media Scheduler & Caption Generator | 7-day content calendar, LLM caption generator, Buffer/Meta API integration proposal. |
| Abdul Haseeb | `lead_qualification` | AI Lead Qualification & Sales Assistant | 5-8 scoring criteria, LLM rubric engine, qualification score + next action for 10+ leads. |
| Hammad Abbas | `resume_interview_assistant` | Resume Screening & Interview Assistant | Screen 5-8 resumes against job description, fit explanation, 5 tailored interview questions. |
| Ali Zaib | `doc_knowledge_assistant` | Document Knowledge Assistant (RAG) | RAG pipeline over policy docs, vector similarity, log accuracy across 10+ questions. |
| Malik Sudais | `proposal_invoice_generator` | Invoice / Proposal Generator Agent | Structured input template, LLM cover paragraph, formatted proposal & invoice packages. |

### Week 3 Workspace

Important files:

- `week3/src/app.py`
- `week3/src/config.py`
- `week3/src/modules/registry.py`
- `week3/src/modules/customer_support_chatbot/`
- `week3/src/modules/email_auto_reply/`
- `week3/src/modules/meeting_summarizer/`
- `week3/src/modules/report_generation_agent/`
- `week3/src/modules/social_media_scheduler/`
- `week3/src/modules/lead_qualification/`
- `week3/src/modules/resume_interview_assistant/`
- `week3/src/modules/doc_knowledge_assistant/`
- `week3/src/modules/proposal_invoice_generator/`
- `week3/docs/Self_Initiative.md`
- `week3/docs/Weekly/Week3_Status_Report.md`
- `week3/tests/`

---

## Future Weeks

Add future weekly tasks below using the same structure:

- original task
- selected group direction
- member assignments
- what was built
- how it was built
- deliverables
- evidence
- final status

