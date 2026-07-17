# Agent Memory

This file stores durable project context for future coding agents. Keep entries short, dated, factual, and useful.

Do not store:

- phone numbers
- personal emails
- API keys or credentials
- private feedback form content
- sensitive personal comments
- unverified assumptions presented as facts

## Persistent Repo Facts

- 2026-07-17: Repository is the SafeX Solutions Summer Internship portfolio for Group 54.
- 2026-07-17: The repo is split into independent week folders: `week1/` and `week2/`.
- 2026-07-17: Week 1 is the SafeX FAQ chatbot prototype.
- 2026-07-17: Week 2 is the Business Automation Research prototype suite.
- 2026-07-17: Week 2 modules live under `week2/src/modules/`.
- 2026-07-17: Each Week 2 module is expected to have `__init__.py`, `engine.py`, and `ui.py`.

## Decisions Made

- 2026-07-17: Harness files should target any coding agent, not only one tool.
- 2026-07-17: Harness files should avoid personal phone numbers and emails.
- 2026-07-17: Agent memory should live at `docs/agent-memory.md`.
- 2026-07-17: The harness file set is `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.cursor/rules/project.mdc`, and docs under `docs/`.
- 2026-07-17: The roster fields `Internship Field (Original Response)` and `Field Category` are not task assignments and should not be inserted into harness docs as task data.

## Workflow Notes

- 2026-07-17: For Week 2 Streamlit modules, keep module rendering inside `render_ui()` in each module's `ui.py`.
- 2026-07-17: Keep app-level Streamlit setup in `week2/src/app.py`.
- 2026-07-17: Keep `week2/src/modules/registry.py` aligned with module folders and app routing.
- 2026-07-17: Track non-responsive members in `docs/team-roster.md` using factual status fields and follow-up dates.

## Member / Progress Observations

- 2026-07-17: Current confirmed Week 2 assignments are listed in `docs/team-roster.md`.
- 2026-07-17: Malik Sudais appears in the source roster with an Invoice Automation Prototype assignment, while `week2/src/modules/` currently has one `invoice_automation` module associated with Arsalan Qasim. Confirm ownership before changing module structure.
- 2026-07-17: Existing registry marks HR Proposal, Email Assistant, and Report Generator as completed, but deliverable evidence should be verified before marking them Submitted in harness docs.

## Open Questions

- 2026-07-17: Should Malik Sudais share the existing invoice module, create a separate invoice-related module, or be tracked outside the current code structure?
- 2026-07-17: Which members have submitted screenshots, recordings, progress reports, and explanation videos for Week 2?
- 2026-07-17: Which members should be marked `No response` after follow-up dates are known?

## Do-Not-Repeat Mistakes

- Do not copy private contact details from source rosters into public project harness docs.
- Do not treat internship preference fields as task assignments.
- Do not make broad cross-week refactors when a request targets only one week or module.
- Do not update member status without evidence.
