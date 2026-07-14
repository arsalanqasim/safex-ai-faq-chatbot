# SafeX Solutions AI/ML Internship Portfolio (Summer 2026)

This repository serves as the official collaborative workspace and portfolio for **Group 54** during the **SafeX Solutions Remote Summer Internship Cohort (2026)**. SafeX Solutions is a technology firm specializing in custom AI/ML implementations, operations automation, and business intelligence systems. 

---

## 🏆 Leadership & Group Roster

* **Group Leader:** **Arsalan Qasim** (AI/ML Intern, COMSATS University Islamabad)
* **Team size:** 8 Members

Below is the complete registry of Group 54 contributors and their universities:

| # | Intern Name | Role | University | Specialty / Track | Contact Email |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Arsalan Qasim** | Group Leader | COMSATS University Islamabad | AI/ML, Automation | arsalanqasim400@gmail.com |
| 2 | **MUHAMMAD WASIM** | Team Member | UET Peshawar | AI/ML, Data Science | muhammadwasimpukhtoon@gmail.com |
| 3 | **Muhammad Faozan Mujtaba** | Team Member | NUST H-12 | AI/ML, Computer Science | fozanmujtaba.480@gmail.com |
| 4 | **Shahidullah** | Team Member | Bahria University | AI/ML, Web Development | shahidullahkhan091@gmail.com |
| 5 | **Ali Ammar Haider** | Team Member | COMSATS University Islamabad | Business Data Analytics | ahwheh688@gmail.com |
| 6 | **Abdul Haseeb** | Team Member | COMSATS University Islamabad | AI/ML, Computer Science | abdlhaseeb17@gmail.com |
| 7 | **Hammad Abbas** | Team Member | Agriculture University of Peshawar | Data Analyst & Data Science | hammadhadid723@gmail.com |
| 8 | **Ali Zaib** | Team Member | COMSATS University Islamabad | AI/ML, Computer Science | aliofficialzaib@gmail.com |

---

## 📁 Modular Directory Architecture

To ensure code hygiene, avoid merge conflicts, and keep submissions clean, the repository is segmented into independent week-by-week subfolders at the root. Each week's workspace is completely self-contained with its own dependencies, source files, documentation, and tests:

### 📚 [week1/](file:///c:/Users/arsal/Desktop/safex/week1/) — SafeX AI FAQ Chatbot
* **Purpose:** A collaborative semantic search chatbot built to resolve internal intern onboarding queries about SafeX Solutions (HR policies, office timings, IT rules).
* **Core Technology:** Python, Streamlit, scikit-learn (TF-IDF Vectorizer & Cosine Similarity), pytest.
* **Deliverable Status:** 100% Completed & Verified.

### ⚙️ [week2/](file:///c:/Users/arsal/Desktop/safex/week2/) — Business Automation Research
* **Purpose:** Modular prototyping hub for SafeX Solutions' business automation systems.
* **Core Technology:** Python, Pandas, Streamlit.
* **Deliverable Status:** Structural Scaffolding & Boilerplate active. Each of the 8 members has a dedicated folder containing UI stubs and engine stubs ready for their individual logic implementation.
* **Individual Module Assignments:**
  1. **Arsalan Qasim:** *Invoice Automation Prototype* (Scaffolding ready)
  2. **MUHAMMAD WASIM:** *Attendance Automation Prototype* (Scaffolding ready)
  3. **Muhammad Faozan Mujtaba:** *HR Automation Proposal* (Scaffolding ready)
  4. **Shahidullah:** *AI Email Assistant Prototype* (Scaffolding ready)
  5. **Ali Ammar Haider:** *AI Report Generator Prototype* (Scaffolding ready)
  6. **Abdul Haseeb:** *Resume Screening Prototype* (Scaffolding ready)
  7. **Hammad Abbas:** *OCR / Document Processing Prototype* (Scaffolding ready)
  8. **Ali Zaib:** *Predictive Analytics Mini-Study* (Scaffolding ready)

---

## ⚙️ How to Navigate and Execute

Since every week task is fully modular, you must navigate into the specific folder before installing requirements or running code:

### Running Week 1 FAQ Chatbot
```bash
# Navigate to Week 1 workspace
cd week1

# Install requirements
pip install -r requirements.txt

# Run original chatbot app
streamlit run src/app.py
```

### Running Week 2 Business Automation Suite
```bash
# Navigate to Week 2 workspace
cd week2

# Install requirements
pip install -r requirements.txt

# Run automation hub routing app
streamlit run src/app.py
```

### Running Tests
To run unit tests for a specific week:
```bash
cd week1
python -m pytest
```
