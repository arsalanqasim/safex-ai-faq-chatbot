# SafeX AI FAQ Chatbot — Case Study

*Prepared by: Ali Zaib (Technical Writer) & Arsalan Qasim (Group Lead / QA & Backend)*
*Team: SafeX Solutions — Week 1 Internship Cohort (Group 54)*

---

## 1. Executive Summary

The SafeX AI FAQ Chatbot is a lightweight, fully local semantic search assistant designed to streamline the onboarding experience for academic and professional AI/ML internship cohorts. Rather than querying static documents or incurring the high latency, cost, and privacy risks of external Large Language Model (LLM) APIs, the system transforms user questions into numerical vectors using a Term Frequency-Inverse Document Frequency (TF-IDF) representation and calculates Cosine Similarity against a verified JSON database. Evaluated on a test suite of 185 queries, the application achieves an average retrieval response time of **0.90 ms** with an overall retrieval accuracy of **61.29%** and a fallback success rate of **86.67%** at a tuned decision threshold of `0.35`.

---

## 2. Problem Statement

*   **Friction in Onboarding:** Internal internship cohorts at SafeX Solutions frequently ask the same questions regarding policies, IT support, leave procedures, and company timings. Searching through long, static PDF and markdown documentation is slow and inefficient.
*   **The User Persona:** End-users are new hires, academic interns, and internal corporate staff requiring quick, accurate guidance.
*   **The Architecture Constraint:** Utilizing commercial APIs (such as OpenAI or Anthropic) introduces recurring costs, data leakage privacy concerns, and potential downtime. A fully local, resource-light, and offline similarity engine was selected to address these constraints.

---

## 3. Goals & Success Criteria

| Goal | Metric | Target | Achieved | Target Met? |
|---|---|---|---|---|
| Accurate FAQ matching | Precision on positive test cases | &ge; 90% | 61.29% | No (See Section 6) |
| Reject unrelated queries | Fallback success rate on negative test set | &ge; 95% | 86.67% | No (See Section 6) |
| Usability / Responsiveness | Streamlit UI response time | &lt; 50 ms | **0.90 ms** | **Yes** |

---

## 4. System Architecture

```text
User Query ➔ Streamlit UI (src/app.py)
           ➔ Chatbot Orchestrator (src/chatbot.py)
           ➔ Knowledge Base Loader (src/knowledge_base.py) ➔ Reads data/faq.json
           ➔ TF-IDF + Cosine Similarity Engine (src/similarity.py)
           ➔ Threshold Check ➔ Returns Best Match / Fallback Message
           ➔ Response rendered in UI with typing animation
```

**Component Ownership:**

| Component | File | Owner |
|---|---|---|
| Data Loader | `src/knowledge_base.py` | Muhammad Wasim |
| Similarity Engine | `src/similarity.py` | Muhammad Faozan Mujtaba |
| Frontend/UI | `src/app.py` | Shahidullah |
| FAQ Data & Test Set | `data/faq.json`, `evaluation/test_questions.json` | Ali Ammar Haider |
| Orchestration & Backend | `src/chatbot.py` | Arsalan Qasim |
| QA & Unit Testing | `tests/test_chatbot.py` | Arsalan Qasim |
| Technical Writer | `docs/Case_Study.md` | Ali Zaib |

---

## 5. Technical Approach

### 5.1 Knowledge Base
*   **Structure:** Located at `data/faq.json`, the dataset contains 95 structured records with `id` (integer), `category` (string), `question` (string), and `answer` (string).
*   **Validation:** The loader verifies that the target file exists, decodes the JSON, and enforces schema verification (checking for the presence of `question` and `answer` keys) while raising custom exceptions for invalid or corrupted datasets.

### 5.2 TF-IDF Vectorization
*   **Text Preprocessing:** Automated tokenization, lowercasing, and English stop-word filtering using scikit-learn's `TfidfVectorizer`.
*   **Vocabulary Matrix:** The corpus of 95 FAQ questions is fit-transformed into a sparse term-document matrix, capturing tf-idf weightings for all unique vocabulary terms.

### 5.3 Cosine Similarity Matching
*   **Matching Math:** Incoming user queries are transformed into the same tf-idf vector space. Cosine similarity is calculated between the query vector and the question matrix:
    $$\text{Cosine Similarity}(\vec{A}, \vec{B}) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|}$$
*   **Selection:** The question indexing maximum similarity score is identified using NumPy's `argmax`.

### 5.4 Threshold & Fallback Logic
*   **Decision Boundary:** The orchestrator enforces a minimum similarity score boundary (configured to `0.35` by default). If the highest matching score is below the threshold, a standard fallback message is returned, preventing the chatbot from hallucinating or presenting irrelevant answers.

---

## 6. Evaluation & Results

The system was evaluated against a test suite of 185 sample questions (`evaluation/test_questions.json`):
*   **Positive test cases:** 155 queries (questions that map to a specific FAQ ID).
*   **Negative test cases:** 30 queries (out-of-domain questions like "cooking recipe for lasagna" that should be rejected).

### 6.1 Performance Summary
*   **Retrieval Accuracy:** **61.29%**
*   **Fallback Success Rate:** **86.67%**
*   **Average Latency:** **0.90 ms** per query.

### 6.2 Analysis of Failures (Engineering Retrospective)
1.  **Question Overlap Mismatch:** The query `"Who are SafeX clients?"` expected FAQ ID `7` (`"Who does SafeX Solutions work with?"`). However, the similarity model matched it to FAQ ID `56` (`"Who are the clients of SafeX Solutions?"`) with a score of `0.9673`. Because both questions exist in the database and have almost identical meanings, the model behaved correctly, but was flagged as a failure since the expected test ID was hardcoded to `7`.
2.  **Vocabulary Mismatches:** The query `"How does SafeX help students?"` expected FAQ ID `9` (`"How does SafeX Solutions support young professionals?"`), but the model matched it to FAQ ID `94` (`"Can students learn from SafeX Solutions?"`). Since TF-IDF only tracks keyword overlap, it failed to map the synonym `"students"` to `"young professionals"`, instead matching on the word `"students"` in ID `94`.
*   **Screenshot:**
    ![Chatbot Interface](file:///c:/Users/arsal/Desktop/safex/assets/chatbot_demo.png)

---

## 7. Challenges & Learnings

*   **Term Mismatch Limitation:** TF-IDF lacks semantic understanding of synonyms (e.g., mapping `"clients"` to `"customers"` or `"students"` to `"interns"`). Expanding the database questions with alternative formulations is necessary to mitigate this.
*   **Parallel Development Contract:** Collaborating on independent branches required defining strict function signatures early on. For example, ensuring `load_faq_data` preserved the `id` field was critical to enabling automated benchmarking against `evaluation/test_questions.json`.

---

## 8. Future Improvements

*   **TF-IDF N-grams:** Introduce bigrams/trigrams (e.g. `ngram_range=(1, 2)`) to capture multi-word terms like "leave policy" and "office hours".
*   **Synonym Preprocessing:** Incorporate a lemmatizer or a predefined synonym map during preprocessing.
*   **Lightweight Transformer Model:** Transition from TF-IDF to a lightweight Sentence-Transformer model (e.g. `all-MiniLM-L6-v2`) to capture deep semantic similarity instead of exact token overlap.

---

## 9. Appendix

*   **Repository Location:** `https://github.com/arsalanqasim/safex-ai-faq-chatbot.git`
*   **Vocabulary Glossary:**
    *   **TF-IDF:** Term Frequency-Inverse Document Frequency, a statistical measure evaluating how relevant a word is to a document in a collection.
    *   **Cosine Similarity:** Metric measuring the cosine of the angle between two vectors projected in multi-dimensional space, representing similarity.
    *   **Fallback Guardrail:** The mechanism of rejecting predictions whose confidence score falls below a set minimum threshold.

---

*Last updated: July 8, 2026 — Arsalan Qasim*
