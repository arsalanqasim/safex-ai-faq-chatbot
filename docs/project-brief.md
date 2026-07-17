# Project Brief

## Identity

- Project name: SafeX Solutions Summer Internship Portfolio.
- Group: Group 54.
- Group Leader: Arsalan Qasim.
- Stakeholder: SafeX Solutions internship team and evaluators.
- Purpose: complete weekly internship tasks as a group, build practical AI/ML and automation portfolio work, and document each task clearly for review.

## What We Are Building

Group 54 is building a structured portfolio of weekly internship submissions for SafeX Solutions. Each week has its own folder, dependencies, source code, tests, and documentation.

The repository currently contains:

- Week 1: SafeX FAQ chatbot prototype.
- Week 2: Business Automation Research suite with separate automation modules for members.

The project should show both the technical implementation and the group process: what was assigned, what each member contributed, how the work was built, how it can be run, and what evidence supports completion.

## For Whom We Are Working

The work is prepared for SafeX Solutions as part of the summer internship program. It is also intended for internship evaluators, university or HEC-style evaluation, and portfolio review.

## How We Are Building

The repository uses a week-by-week structure:

- Each week is isolated in its own root folder.
- Each week has its own requirements and run commands.
- Week 2 uses independent modules so members can work in parallel.
- Shared documentation tracks assignments, progress, deliverables, and review criteria.

Technical expectations:

- Python-first implementation.
- Streamlit for local interactive demos where applicable.
- Pandas / NumPy for data handling where applicable.
- NLP, OCR, ML, or LLM APIs only where relevant to the assigned module.
- Small sample data and clear demonstration outputs.
- Screenshots or recordings for portfolio evidence.

## Week 1 Summary

Week 1 task:

> Build a small AI/ML prototype for SafeX, such as an FAQ chatbot for safexsolutions.com, a social-media engagement forecast model, or a data dashboard using real/sample data. Document approach and results as a portfolio case study. The group leader consolidates weekly submissions and sends a short summary to the Team Lead by Friday. The group leader also submits anonymous feedback on the Team Lead / overall program through the feedback form.

Group 54 selected the FAQ chatbot direction. The project is stored in `week1/`.

Core idea:

- Build a small chatbot that answers SafeX-related FAQ questions.
- Use a local knowledge base and similarity matching.
- Provide a Streamlit interface.
- Document approach, evaluation, and results as a case study.

Important files:

- `week1/src/app.py`
- `week1/src/chatbot.py`
- `week1/src/knowledge_base.py`
- `week1/src/similarity.py`
- `week1/data/faq.json`
- `week1/docs/Case_Study.md`
- `week1/docs/Evaluation.md`
- `week1/tests/test_chatbot.py`

## Week 2 Summary

Week 2 task:

> Business Automation Research. Each member designs, builds, and documents one automation prototype component that continues the group's Week 1 work. Modules should integrate cleanly, avoid duplicate work, and include source code, short documentation, screenshots or recordings, progress reporting, and a mandatory explanation video.

The Week 2 project is stored in `week2/`.

Core idea:

- Build a modular business automation prototype suite.
- Give each member a separate automation module.
- Expose modules through a shared Streamlit app.
- Track progress and deliverables centrally.

Important files:

- `week2/src/app.py`
- `week2/src/modules/registry.py`
- `week2/src/modules/*/engine.py`
- `week2/src/modules/*/ui.py`
- `week2/docs/Weekly/Week2_Status_Report.md`

## Source Data Note

The original roster included fields named `Internship Field (Original Response)` and `Field Category`. Those fields are not task assignments and should not be copied into harness files as task data.

The source roster also included personal contact details. Harness files should track names, roles, assignments, progress, and deliverables, but not personal phone numbers or emails.
