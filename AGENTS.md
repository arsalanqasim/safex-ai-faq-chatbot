# Rules & Guidelines for AI Coding Agents

This repository serves as a collaborative portfolio for Group 54's AI/ML internship with SafeX Solutions. To maintain clean history and prevent cross-week code churn, all AI agents (LLMs, copilots, agentic scripts) must strictly adhere to the guidelines outlined in this document.

---

## 🛑 CRITICAL LAWS FOR AI AGENTS

> [!IMPORTANT]
> **NO UNAUTHORIZED IMPLEMENTATION OF ASSIGNED TASKS**
> * AI Agents **must never** write actual production code, business logic, calculations, or models for any assigned team member's Week 2+ tasks.
> * AI Agents **must never** write actual production code, business logic, calculations, or models for the Group Leader's individual tasks (e.g. Invoice Automation).
> * The **ONLY** exception is if the Group Leader explicitly commands the agent in a user prompt to write a specific implementation (e.g., *"Implement the invoice PDF extraction logic"*).

> [!WARNING]
> **LIMIT WORK TO SCAFFOLDING AND DOCUMENTATION**
> * Unless explicitly instructed by the Group Leader to implement a feature, AI agents must restrict all task-specific contributions to **scaffolding, templates, empty boilerplate, placeholder functions, interface definitions, and documentation stubs**.
> * Writing mocked consoles, dummy text inputs, and empty event trigger stubs in `ui.py` files is permitted to help verify frontend layout routing.

---

## 📁 Repository Modular Structure

AI agents must keep changes confined to the correct namespaces. The repository root is split into week subfolders, each acting as an independent, standalone project:

* **`/week1/`**: Contains the collaborative FAQ Chatbot project. Do not touch or modify any code here unless resolving a specific legacy bug.
* **`/week2/`**: Contains the Business Automation Research prototype suite.
  * All active stubs are located under `week2/src/modules/`.
  * Each task folder contains an `__init__.py`, `engine.py` (calculations, mock models, data processing), and `ui.py` (Streamlit rendering).
  * Agents must **only** make changes to the specific folder corresponding to the active task.

---

## 💻 Coding & Interface Standards

When modifying scaffolding or authorized code, agents must follow these guidelines:

1. **Clean Code and Type Hinting:**
   * Write clean, idiomatic Python code.
   * Provide proper type annotations for all function and class signatures.
2. **Boilerplate Layouts:**
   * When writing module stubs, use the standard Class names matching the directory name (e.g. `AttendanceEngineStub` inside `week2/src/modules/attendance/engine.py`).
   * Provide clean docstrings explaining the class interfaces and arguments.
3. **Streamlit Component Encapsulation:**
   * Streamlit UI components for a module must be fully self-contained inside the module's `ui.py` file within a `def render_ui():` function.
   * Do not write global session state updates or page setups inside module sub-files; keep page configuration inside `/week2/src/app.py`.
4. **Local Paths and Imports:**
   * Never hardcode absolute system paths. Use relative path references anchored to the root folder of that week.
   * Ensure namespace imports are formatted relative to that week's source directory (e.g., `from src.modules.registry import ...` executed from `week2/`).

---

## 📝 Documentation & Review Standards

1. **Keep Root Documentation Clean:**
   * Do not inject task-specific, developer-specific, or internship-specific comments into the root `README.md`.
   * Keep the root README generic, focusing on overall workspace description, setup instructions, structure, and contribution rules.
2. **Preserve Team Registry Metadata:**
   * Keep the `MODULE_REGISTRY` mapping in `week2/src/modules/registry.py` accurate. Any new module must first be registered there before files are created.
3. **No Code Churn:**
   * Do not refactor existing, working code in `week1/` or `week2/src/modules/` unless fixing a documented bug or explicitly requested. Preserve all docstrings and comments.
