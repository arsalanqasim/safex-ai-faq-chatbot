# SafeX AI Knowledge Assistant (RAG)

Welcome to the **SafeX AI Knowledge Assistant** repository! This project is a production-inspired, Retrieval-Augmented Generation (RAG) knowledge retrieval application developed by **Group 54** during the SafeX Solutions AI/ML Internship.

The assistant is built to ingest unstructured company documents (such as web pages, PDF offers, Markdown, plain text, and JSON FAQ sheets) and answer user inquiries accurately using Google's **Gemini API**—ensuring absolute factual accuracy by refusing to answer when data is missing.

---

## 👥 Group 54 Roster

*   **Group Leader:**
    *   **Arsalan Qasim** (arsalanqasim400@gmail.com) — *AI/ML Intern*
*   **Team Members:**
    1.  **MUHAMMAD WASIM** (muhammadwasimpukhtoon@gmail.com) — *AI, Data Science, ML*
    2.  **Muhammed Faizan Mujtaba** (fozanmujtaba.480@gmail.com) — *AI/ML*
    3.  **Shahidullah** (shahidullahkhan091@gmail.com) — *Web Development, AI/ML*
    4.  **Ali Ammar Haider** (aliwheht688@gmail.com) — *Data Analytics, Business Intelligence*
    5.  **Abdul Haseeb** (abdlhaseeb17@gmail.com) — *AI/ML*
    6.  **Hammad Abbas** (hammadhadid723@gmail.com) — *Data Analysis & Data Science*
    7.  **Ali Zaib** (aliofficialzaib@gmail.com) — *AI/ML*

---

## 📁 Repository Directory Structure

```text
safex/
├── .env.example                  # Environment configuration template
├── .gitignore                    # Python file tracking ignores
├── README.md                     # Onboarding and workflow instructions (This File)
├── SYSTEM_ARCHITECTURE.md        # Technical design diagrams (Mermaid format)
├── requirements.txt              # Project dependencies
├── assets/
│   ├── logo/                     # SafeX logo assets
│   ├── screenshots/              # Portfolio screenshots
│   └── demo.gif                  # Animated application preview
├── data/
│   ├── raw/                      # Raw text, HTML, JSON FAQ, and PDF files
│   ├── processed/                # Preprocessed and cleaned chunks
│   └── vector_store/             # Serialized NumPy vector database files
├── docs/
│   ├── Architecture.md           # Deep dive into engineering decisions
│   ├── Case_Study.md             # Portfolio Case Study Template
│   ├── Evaluation.md             # Guide for benchmarking accuracy & latency
│   ├── Meeting_Notes.md          # Templates for weekly team syncs
│   └── Weekly/                   # Weekly progress submissions folder
├── src/                          # RAG Source Code
│   ├── __init__.py
│   ├── app.py                    # Streamlit visual UI frontend
│   ├── chatbot.py                # Runtime query pipeline
│   ├── logger.py                 # Application logger configuration
│   ├── config/                   # Settings and prompt files
│   └── pipeline/                 # Modular document indexing modules
└── tests/                        # Automated unit tests
    └── test_rag.py
```

---

## 🛠️ Local Setup Instructions

Follow these steps to set up and run the project locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/arsalanqasim/safex-knowledge-assistant.git
cd safex-knowledge-assistant
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

### 4. Configure Environment Variables
1.  Copy the environment template:
    ```bash
    cp .env.example .env
    ```
2.  Open the newly created `.env` file and insert your **Gemini API Key**:
    ```text
    GEMINI_API_KEY=your_actual_api_key_here
    ```
    *Note: If no API key is specified, the application will automatically fall back to **Mock/Offline Mode**, allowing you to test UI and pipelines without internet connectivity.*

---

## 🚀 Execution & Workflow

### 1. Build the Vector Index (Run Once)
Before querying the assistant, you must populate the vector database with raw files. 
Place raw data files (HTML, TXT, MD, JSON FAQ, or PDF) into `data/raw/` and execute the indexing pipeline:
```bash
python src/pipeline/vector_store.py
```
This runs the full ingestion pipeline: Loader ➔ Cleaner ➔ Chunker ➔ Embedder ➔ NumPy Index compiler.

### 2. Start the Streamlit Application
Run the frontend UI server:
```bash
streamlit run src/app.py
```
Open the URL shown in your terminal (usually `http://localhost:8501`) to interact with the SafeX AI Knowledge Assistant. You can also trigger database rebuilds directly from the UI sidebar.

### 3. Run Automated Tests
Verify code integrity using `pytest`:
```bash
pytest tests/
```

---

## 🤝 Collaborative Development Git Workflow

To maintain a clean codebase, Group 54 uses a standard Feature-Branch git workflow:

1.  **Pull latest changes**: Always start by checking out the main branch and pulling the newest updates:
    ```bash
    git checkout main
    git pull origin main
    ```
2.  **Create a feature branch**: Never write code directly on `main`. Create a descriptive branch named after your task:
    *   *Loading tasks:* `git checkout -b feature/load-pdf`
    *   *Cleaning tasks:* `git checkout -b feature/clean-html`
    *   *UI modifications:* `git checkout -b feature/style-streamlit`
    *   *Bug fixes:* `git checkout -b bugfix/embed-rate-limit`
3.  **Commit changes**: Commit code in clean, logical units with descriptive messages:
    ```bash
    git add .
    git commit -m "feat(loader): implement PDF page extractor using pypdf"
    ```
4.  **Push and open a PR**: Push your branch to GitHub and create a Pull Request for code review:
    ```bash
    git push origin feature/load-pdf
    ```
5.  **Review**: At least one other team member should review the code before merging it to `main`.
