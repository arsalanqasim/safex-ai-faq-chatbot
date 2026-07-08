# safex-ai-faq-chatbot

An AI-powered semantic FAQ chatbot project boilerplate for SafeX Solutions. Designed as a Week 1 internship cohort starter template.

---

## 📖 Project Overview
This repository serves as a starting boilerplate template for building a lightweight semantic FAQ chatbot. The final system will normalize onboarding questions, vectorize them locally using TF-IDF representation, and calculate Cosine Similarity against a verified JSON database to retrieve matching responses.

---

## ✨ Features (To Be Implemented)
- **JSON Knowledge Base Loader:** Loads and validates questions and answers.
- **TF-IDF Vector Space Model:** Transforms strings into term frequency vectors.
- **Cosine Similarity Engine:** Calculates and retrieves the best-matching FAQ index.
- **Threshold Decision Boundary:** Enforces a minimum matching score to trigger fallback messages.
- **Streamlit Interactive UI:** Dashboard visualizer showing matching details.
- **Pytest Verification Suite:** Unit testing checking component boundaries.

---

## 📁 Folder Structure
```text
safex-ai-faq-chatbot/
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git file tracking rules
├── README.md                     # Onboarding and task workflow (This File)
├── requirements.txt              # Project package requirements
├── assets/
│   └── screenshots/              # UI mockups and screenshots
├── data/
│   └── faq.json                  # verified FAQ database (JSON)
├── docs/
│   ├── Case_Study.md             # Portfolio Case Study Template
│   ├── Evaluation.md             # Benchmark guidelines
│   └── Weekly/
│       └── weekly_summary_template.md  # Template for weekly updates
├── evaluation/
│   └── test_questions.json       # positive/negative test datasets
├── src/
│   ├── app.py                    # Streamlit layout skeleton
│   ├── chatbot.py                # Chatbot orchestrator skeleton
│   ├── config.py                 # System paths and constants
│   ├── knowledge_base.py         # Data loader skeleton
│   └── similarity.py             # Similarity calculation skeleton
└── tests/
    └── test_chatbot.py           # Pytest unit tests skeleton
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/arsalanqasim/safex-ai-faq-chatbot.git
cd safex-ai-faq-chatbot
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
```bash
cp .env.example .env
```

---

## 👥 Team & Task Distribution

Responsibilities are divided to allow parallel implementation:

| Team Member | Role | File / Component Ownership |
| :--- | :--- | :--- |
| **Arsalan Qasim** | **Leader, Backend & QA Engineer** | Project architecture, GitHub management, integration, documentation, chatbot orchestration (`src/chatbot.py`), unit tests (`tests/test_chatbot.py`), and performance benchmarks. |
| **Muhammad Wasim** | **Data Loader Dev** | Knowledge base module (`src/knowledge_base.py`). |
| **Muhammad Faozan Mujtaba** | **Algorithm Dev** | Similarity algorithm (`src/similarity.py`). |
| **Shahidullah** | **Frontend Dev** | Streamlit layout and dashboard visualizer (`src/app.py`). |
| **Ali Ammar Haider** | **Data Architect** | FAQ data (`data/faq.json`) and test questions (`evaluation/test_questions.json`). |
| **Ali Zaib** | **Technical Writer** | Case study layout (`docs/Case_Study.md`), guidelines, and assets. |

---

## 🤝 Collaborative Git Workflow
1. **Pull Main:** `git checkout main` and run `git pull origin main`.
2. **Create Feature Branch:** Create a branch for your module: `git checkout -b feature/your-feature-name`.
3. **Commit Code:** Make changes and commit: `git commit -m "feat(module): description of contribution"`.
4. **Push:** Push branch to remote: `git push origin feature/your-feature-name`.
5. **Open Pull Request:** Open a Pull Request on GitHub and request review from the Leader.

---

## 🔮 Future Improvements
- **TF-IDF N-grams:** Capturing partial word matching for typo resilience.
- **Lightweight Transformers:** Upgrading vector space to transformer models (e.g. BERT/MiniLM).
- **Automated Logging:** Saving runtime interaction logs for analytical reviews.
