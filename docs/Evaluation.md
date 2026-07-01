# Evaluation Guide - SafeX RAG Knowledge Assistant

This guide explains how to measure, audit, and log the retrieval and response quality of the RAG system. Regular evaluations ensure the assistant is accurate, fast, and does not hallucinate.

---

## 1. Key Metrics to Measure

As part of our quality assurance, we track three primary metrics:

1. **Retrieval Relevance**:
   - Do the retrieved context chunks actually contain the answer to the user's question?
   - Measured as a relevance similarity score (from numpy search) and manual audit.
2. **Answer Correctness & Faithfulness**:
   - Is the generated response accurate according to the retrieved context?
   - Did the system successfully state "I do not know" if the context lacked information (preventing hallucinations)?
3. **Response Latency**:
   - How long did the system take to execute retrieval and generate a response?
   - Target total latency: **< 2.0 seconds**.

---

## 2. Evaluation Assets

All evaluation datasets and results are stored in the root `evaluation/` directory:
- [test_questions.json](file:///c:/Users/arsal/Desktop/safex/evaluation/test_questions.json): Standardized set of representative questions, expected answers, and source URLs.
- [evaluation_results.csv](file:///c:/Users/arsal/Desktop/safex/evaluation/evaluation_results.csv): Spreadsheet template for logging test runs, latency, retrieved sources, and correctness notes.

---

## 3. Evaluation Procedure (How to Audit)

During weekly updates or after changing the loading/chunking parameters, interns should conduct a manual evaluation run:

1. **Prepare Raw Data**: Ensure the vector index has been built (`python src/pipeline/vector_store.py`).
2. **Query the System**: Run the test questions from `test_questions.json` through the Streamlit interface or the test suite.
3. **Audit Retrieval**:
   - Expand the **🔍 View References** accordion in the UI.
   - Verify if the source page matching the query was retrieved.
   - Record the top relevance score.
4. **Audit Response**:
   - Check if the generated answer is correct.
   - If the query was a "negative test" (asking about something not in the database), ensure the model correctly returned the "I do not know" response.
5. **Log Results**:
   - Record the latencies and findings in `evaluation/evaluation_results.csv`.
   - Update the logs before submitting weekly reports.
