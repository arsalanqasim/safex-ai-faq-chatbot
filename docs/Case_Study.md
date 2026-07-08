# SafeX AI FAQ Chatbot — Case Study

*Prepared by: Ali Zaib (Technical Writer)*
*Team: SafeX Solutions — Week 1 Internship Cohort*

---

## 1. Executive Summary

> *One paragraph, written last. Summarize the problem, the solution, and the outcome in plain language for a non-technical reader (e.g., a recruiter or client).*

The SafeX AI FAQ Chatbot is a lightweight, fully local semantic search assistant that answers onboarding questions by matching user input against a verified knowledge base using TF-IDF vectorization and Cosine Similarity — with no external LLM API calls required.

---

## 2. Problem Statement

- What onboarding/support pain point does this solve?
- Who is the end user (new hires, customers, internal staff)?
- Why a local/offline similarity model instead of a hosted LLM (cost, privacy, latency, simplicity)?

---

## 3. Goals & Success Criteria

| Goal | Metric | Target |
|---|---|---|
| Accurate FAQ matching | Precision on `evaluation/test_questions.json` | e.g. ≥ 90% |
| Reject unrelated queries | Fallback trigger rate on negative test set | e.g. ≥ 95% |
| Usability | Streamlit UI response time | < 1s |

*(Fill in actual targets/results once Hammad's benchmarks are available.)*

---

## 4. System Architecture

```
User Query → Streamlit UI (app.py)
           → Chatbot Orchestrator (chatbot.py)
           → Knowledge Base Loader (knowledge_base.py) ← data/faq.json
           → TF-IDF + Cosine Similarity Engine (similarity.py)
           → Threshold Check → Best Match / Fallback Message
           → Response rendered in UI
```

**Component ownership:**

| Component | File | Owner |
|---|---|---|
| Data Loader | `src/knowledge_base.py` | Muhammad Wasim |
| Similarity Engine | `src/similarity.py` | Muhammad Faozan Mujtaba |
| Frontend/UI | `src/app.py` | Shahidullah |
| FAQ Data & Test Set | `data/faq.json`, `evaluation/test_questions.json` | Ali Ammar Haider |
| Orchestration | `src/chatbot.py` | Abdul Haseeb |
| Testing | `tests/test_chatbot.py` | Hammad Abbas |
| Architecture/Integration | Overall repo | Arsalan Qasim |

---

## 5. Technical Approach

### 5.1 Knowledge Base
- Structure of `faq.json` (question/answer pairs, categories if any).
- Validation rules applied on load.

### 5.2 TF-IDF Vectorization
- Text normalization steps (lowercasing, stopword removal, tokenization).
- Vocabulary size, vectorizer library used (e.g., scikit-learn's `TfidfVectorizer`).

### 5.3 Cosine Similarity Matching
- How the query vector is compared against the FAQ matrix.
- How the best match index is selected.

### 5.4 Threshold / Fallback Logic
- Minimum similarity score required to return an answer.
- Fallback message shown when no match clears the threshold.

---

## 6. Evaluation & Results

> *Pull actual numbers from `evaluation/test_questions.json` runs and Hammad's benchmark suite.*

- Positive test accuracy: ___
- Negative/fallback test accuracy: ___
- Notable failure cases and why they occurred.
- Screenshot(s) of the Streamlit dashboard showing match scores (place in `assets/screenshots/`).

---

## 7. Challenges & Learnings

- Technical challenges (e.g., short-query ambiguity, synonym mismatches).
- Team/process challenges (parallel development, merge conflicts, API contracts between modules).
- What the team would do differently.

---

## 8. Future Improvements

- TF-IDF n-grams for typo resilience.
- Upgrading to lightweight transformer embeddings (BERT/MiniLM).
- Automated interaction logging for analytics.

---

## 9. Appendix

- Links: GitHub repo, live demo (if deployed).
- Full team & role table (see README.md).
- Glossary of terms (TF-IDF, Cosine Similarity, Threshold Boundary).

---

*Last updated: [DATE] — [YOUR NAME]*
