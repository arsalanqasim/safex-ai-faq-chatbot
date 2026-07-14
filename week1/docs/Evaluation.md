# safex-ai-faq-chatbot — Evaluation Guidelines

This document outlines the guidelines and testing procedures for measuring the matching quality and latency of the FAQ Chatbot.

---

## 1. Evaluation Objectives
The goal of the evaluation is to verify:
- **Retrieval Accuracy:** Whether positive test queries are matched with the correct FAQ item, and negative test queries correctly trigger fallback responses.
- **Latency Benchmarks:** Processing latency should remain below 50 milliseconds.

---

## 2. Test Dataset Format (`evaluation/test_questions.json`)
The testing dataset should include positive and negative test cases.
- **Positive Category:** Queries containing rephrased or colloquial formulations of verified FAQ questions.
- **Negative Category:** Unrelated queries designed to test threshold fallback reliability.

Expected fields per test case:
- `id`: Unique identifier (e.g. `q_01`)
- `question`: Query text string
- `expected_faq_id`: Target FAQ matching ID (or `None` for negative cases)
- `category`: `positive` or `negative`

---

## 3. Evaluation Tasks (TODO for Hammad Abbas)
Implement the evaluation framework:
1. **Load Test Cases:** Parse `evaluation/test_questions.json` and load test cases.
2. **Query Model:** Query each question through the `FAQChatbot` class.
3. **Assert Correctness:**
   - For positive cases, verify `predicted_faq_id == expected_faq_id` and `is_fallback == False`.
   - For negative cases, verify `is_fallback == True`.
4. **Log Results:** Record latency and match details in a CSV format under `evaluation/evaluation_results.csv`.
5. **Compute Metrics:** Calculate the overall accuracy percentage and average processing latency in milliseconds.
