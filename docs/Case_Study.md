# Portfolio Case Study: SafeX AI Knowledge Assistant (RAG)

Use this document to compile your team's approach, technical contributions, evaluations, and final learnings. This will serve as a portfolio piece for the interns.

---

## 1. Project Overview & Objective
- **Company**: SafeX Solutions
- **Project Duration**: [Insert Weeks/Timeline]
- **Team**: Group 54
- **Core Challenge**: Creating an intelligent, non-hallucinating knowledge retrieval chatbot capable of answering internal organization questions using unstructured documents.

---

## 2. Technical Architecture & Approach
Describe the technology stack and architecture decisions your team implemented.
- **Frontend / UI**: Streamlit (Python-native interactive chat interface).
- **RAG Pipeline**:
  - Source-agnostic document loader supporting PDF, HTML, MD, JSON, and TXT files.
  - Custom vector database built using NumPy and Pickle.
  - Large Language Model: Google Gemini API (`gemini-1.5-flash`).
  - Decoupled OOP interfaces allowing providers and models to be swapped easily.

---

## 3. Engineering Implementation Details
Detail what your team worked on.
- **Document Loading & Extraction**: [Detail how you implemented PDF text extraction or website scrapers].
- **Text Preprocessing**: [Detail cleaning logic, regex tags, and text chunking strategy].
- **Similarity Matching**: [Describe how cosine similarity was computed using NumPy and how you tuned the retrieval threshold].
- **Prompts**: [Explain your prompt engineering strategies to prevent model hallucinations].

---

## 4. Evaluation & Results
Summarize your retrieval and generation experiments. Refer to the logs compiled in `docs/Evaluation.md` and `evaluation/evaluation_results.csv`.

| Metric | Baseline | Final Value | Target Met? |
| :--- | :--- | :--- | :--- |
| **Retrieval Accuracy** | [e.g. 60%] | [e.g. 95%] | Yes/No |
| **Response Latency** | [e.g. 3.2s] | [e.g. 1.1s] | Yes/No |
| **Hallucination Rate** | [e.g. High] | [e.g. 0%] | Yes/No |

---

## 5. Challenges Overcome
Describe specific technical obstacles your team faced and resolved:
1. *Challenge 1 (e.g. Windows C++ compilation errors for DBs)*: [Explain how you bypassed this using NumPy/Pickle vector stores].
2. *Challenge 2 (e.g. Gemini API Rate Limits)*: [Explain how you resolved this via batch chunking/throttling].

---

## 6. Key Achievements & Deliverables
- **Production-Inspired Codebase**: Decoupled, modular, documented Python repository.
- **Complete Test Coverage**: Verified query/ingestion stages.
- **Full Case Study & Documentation**: Ready-to-share portfolio project.
- **Professional Collaboration**: Managed via a structured Git feature-branch workflow.
