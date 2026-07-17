# Review and Submission Checklist

Use this checklist before submitting weekly work or handing changes back to the group leader.

## Repository Hygiene

- [ ] Changes are limited to the intended week or module.
- [ ] No unrelated files were refactored.
- [ ] No private phone numbers, personal emails, secrets, or API keys were added.
- [ ] Generated caches, virtual environments, and large artifacts are not included.
- [ ] File paths are relative to the relevant week folder.
- [ ] Documentation matches the current code structure.

## Python Quality

- [ ] Public functions and classes have type hints.
- [ ] Function names are clear and task-specific.
- [ ] Error handling is appropriate for the prototype.
- [ ] Sample data is small, readable, and safe to commit.
- [ ] Core logic is kept out of Streamlit UI code where practical.
- [ ] Tests cover changed behavior where practical.

## Streamlit Quality

- [ ] Module UI is inside `render_ui()`.
- [ ] Page-level setup remains in `week2/src/app.py`.
- [ ] UI labels are clear and professional.
- [ ] Demo flow works with sample data.
- [ ] Empty, loading, and error states are understandable.

## Week 1 Checklist

- [ ] FAQ data is present and valid.
- [ ] Chatbot can answer representative questions.
- [ ] Evaluation or tests run successfully.
- [ ] Case study explains approach and results.
- [ ] Screenshots or demo evidence are available.

## Week 2 Module Checklist

- [ ] Module folder exists under `week2/src/modules/`.
- [ ] Module has `__init__.py`, `engine.py`, and `ui.py`.
- [ ] Module is listed correctly in `week2/src/modules/registry.py`.
- [ ] Module can be reached through the Week 2 app.
- [ ] Module has sample input and output.
- [ ] Module has short documentation explaining what was built, how it works, and how to run or view it.
- [ ] Screenshots or a short recording are available.
- [ ] Explanation video status is tracked.
- [ ] Progress report status is tracked.

## Member Progress Checklist

- [ ] `docs/team-roster.md` has current status.
- [ ] Last known update date is recorded.
- [ ] Missing deliverables are listed.
- [ ] Non-responsive members have follow-up dates, if applicable.
- [ ] Status is based on evidence, not assumptions.

## Final Handoff Checklist

- [ ] Relevant tests were run, or reason for not running them is documented.
- [ ] Changed files are summarized.
- [ ] Remaining blockers or open questions are listed.
- [ ] `docs/agent-memory.md` is updated if new durable context was learned.
