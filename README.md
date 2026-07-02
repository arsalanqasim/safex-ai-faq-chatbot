# safex-ai-faq-chatbot

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Dashboard-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered semantic FAQ chatbot for SafeX Solutions using sentence TF-IDF embeddings and cosine similarity. Built as a Week 1 internship prototype with a complete portfolio case study.

---

## 📖 Project Overview

This repository represents the Week 1 deliverable for the SafeX AI/ML internship cohort. The objective was to build a polished, modular AI prototype that answers user questions using semantic matching against a verified internal FAQ database. Rather than relying on heavy and complex enterprise architectures (RAG, vector databases, LLM APIs), this prototype implements a lightweight, local text representation model (TF-IDF vectorizer) and cosine similarity metrics to search, analyze, and retrieve matching FAQs entirely offline.

---

## ✨ Features

- **Semantic FAQ Retrieval:** Maps user queries to the closest verified FAQ question using TF-IDF word frequency vectors and cosine similarity calculations.
- **Configurable Relevance Threshold:** Features a slider in the user interface to adjust the minimum similarity score (default `0.35`). Queries scoring below the threshold trigger a friendly fallback message, preventing false positives.
- **Streamlit Diagnostic Dashboard:** An internal tool-style UI that displays the matched FAQ, similarity score, response latency, and a progress bar visualizer.
- **Automated Evaluation Framework:** Includes a batch evaluation script to query the chatbot against positive/negative test questions, logging execution metrics and accuracy to a CSV file.
- **Clean and Modular Structure:** Follows professional software engineering practices with decoupled files for configuration, database parsing, text preprocessing, similarity math, and testing.

---

## 📁 Project Structure

```text
safex-ai-faq-chatbot/
├── .env                          # Local environment variables
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git tracking exclusions
├── README.md                     # Project documentation (This File)
├── requirements.txt              # Project dependencies
├── assets/
│   ├── screenshots/              # UI and diagnostic screenshots
│   └── demo.gif                  # Interactive application demonstration
├── data/
│   └── faq.json                  # Verified SafeX FAQ knowledge base (JSON)
├── docs/
│   ├── Architecture.md           # Mermaid system flow diagrams
│   ├── Case_Study.md             # Complete portfolio case study
│   ├── Evaluation.md             # Benchmark procedures and results analysis
│   └── Weekly/
│       └── weekly_summary_template.md  # Template for intern weekly summaries
├── evaluation/
│   ├── run_eval.py               # Automated evaluation test script
│   ├── test_questions.json       # positive/negative test datasets
│   └── evaluation_results.csv    # Benchmark log outputs from test runs
├── src/
│   ├── app.py                    # Streamlit visual dashboard
│   ├── chatbot.py                # Chatbot orchestrator
│   ├── config.py                 # Project path and threshold settings
│   ├── knowledge_base.py         # JSON database parser & validator
│   ├── similarity.py             # TF-IDF & Cosine Similarity engine
│   └── utils.py                  # Text preprocessing utilities
└── tests/
    └── test_chatbot.py           # Pytest unit tests suite
```

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/arsalanqasim/safex-ai-faq-chatbot.git
cd safex-ai-faq-chatbot
```

### 2. Set Up a Virtual Environment
It is highly recommended to run this project inside a clean virtual environment to prevent package conflicts:
```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the template environment variables:
```bash
cp .env.example .env
```
*(No API keys are required; the chatbot runs entirely locally using scikit-learn.)*

---

## 🚀 Running the Project

### 1. Start the Streamlit App
Run the frontend UI server:
```bash
streamlit run src/app.py
```
Open `http://localhost:8501` in your browser to interact with the internal FAQ dashboard.

### 2. Run Automated Evaluation
Execute the performance test suite:
```bash
python evaluation/run_eval.py
```
This script runs a series of positive (semantically rephrased) and negative (unrelated) queries, matches them, evaluates correctness, and logs the outcomes to `evaluation/evaluation_results.csv`.

### 3. Run Unit Tests
Verify codebase integrity using `pytest`:
```bash
pytest tests/
```

---

## 📊 Evaluation Metrics

The current baseline run metrics logged by the automated script:
- **Total Test Cases:** 12 (10 positive, 2 negative)
- **Matching Accuracy:** 100%
- **Average Latency:** ~0.80 ms
- **Details:** Can be viewed under [docs/Evaluation.md](file:///c:/Users/arsal/Desktop/safex/docs/Evaluation.md) and [evaluation_results.csv](file:///c:/Users/arsal/Desktop/safex/evaluation/evaluation_results.csv).

---

## 👥 Team & Task Distribution

To ensure modular collaboration and minimize merge conflicts, the project responsibilities were distributed among the cohort members as follows:

| Intern Name | Role | Primary Responsibility / Ownership |
| :--- | :--- | :--- |
| **Arsalan Qasim** | **Leader / Release Coordinator** | Project architecture setup, GitHub repository management, and PR approvals. |
| **Muhammad Wasim** | **Similarity Engine Engineer** | Core similarity algorithm implementation (`src/similarity.py`). |
| **Muhammad Faozan Mujtaba** | **Knowledge Base Architect** | JSON FAQ database preparation and loading (`src/knowledge_base.py` & `data/faq.json`). |
| **Shahidullah** | **Frontend UI Developer** | Streamlit user interface development and theme design (`src/app.py`). |
| **Ali Ammar Haider** | **Backend Integration Lead** | Chatbot coordination, thresholds, and configuration settings (`src/chatbot.py` & `src/config.py`). |
| **Abdul Haseeb** | **QA & Test Engineer** | Writing unit test coverage and verification scripts (`tests/test_chatbot.py`). |
| **Hammad Abbas** | **Evaluation Lead** | Creating test cases, writing the evaluation script, and documenting results (`evaluation/run_eval.py` & `docs/Evaluation.md`). |
| **Ali Zaib** | **Technical Writer** | Preparing the case study, architectural details, and templates (`docs/Case_Study.md` & `docs/Architecture.md`). |

---

## 🤝 Contribution Workflow

1. **Checkout Main:** `git checkout main` and pull latest updates: `git pull origin main`.
2. **Create Branch:** Create a branch for your assigned task: `git checkout -b feature/your-feature-name`.
3. **Commit:** Commit your changes with descriptive messages: `git commit -m "feat(module): description of contribution"`.
4. **Push:** Push branch to remote: `git push origin feature/your-feature-name`.
5. **Pull Request:** Open a Pull Request on GitHub against `main` and request reviews.

---

## 🖼️ Screenshots & Demo

*Placeholders for media showcase:*
- **App Dashboard Overview:** `assets/screenshots/dashboard_screenshot.png`
- **Matching Evaluation Runs:** `assets/screenshots/evaluation_terminal.png`
- **Application Demo:** `assets/demo.gif`

---

## 🔮 Future Improvements

1. **Character N-gram Matching:** Adding n-grams to TF-IDF to support better handling of spelling typos.
2. **Contextual Word Embeddings:** Swapping TF-IDF with a lightweight Transformer model (e.g. `all-MiniLM-L6-v2` via `sentence-transformers`) for true semantic similarity that understands synonyms without explicit keyword addition.
3. **Automated KB Expansion:** Integrating a script to automatically ingest and convert document PDFs into FAQ entries.
