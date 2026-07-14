# SafeX AI & Automation Suite Registry
# Tracks team member tasks, contact info, status, and module entry points.

MODULE_REGISTRY = {
    "week1": {
        "faq_chatbot": {
            "title": "🛡️ Semantic FAQ Chatbot",
            "developer": "Entire Group 54",
            "role": "Collaboration",
            "email": "group54-leads@safexsolutions.com",
            "status": "Completed",
            "difficulty": "Advanced",
            "tech": ["Python", "scikit-learn", "NumPy", "Streamlit", "pytest"],
            "description": "On-device FAQ chatbot using TF-IDF Vectorization and Cosine Similarity to answer internal staff and intern queries with zero API costs.",
            "import_path": "src.modules.week1.faq_chatbot",
            "icon": "💬"
        }
    },
    "week2": {
        "invoice_automation": {
            "title": "Invoice Automation Prototype",
            "developer": "Arsalan Qasim",
            "role": "Group Leader",
            "email": "arsalanqasim400@gmail.com",
            "status": "Placeholder (Scaffolding Ready)",
            "difficulty": "Advanced",
            "tech": ["Python", "Pandas", "NumPy", "NLP libraries (spaCy/NLTK) / LLM API", "FastAPI/Streamlit", "Twilio / WhatsApp API"],
            "description": "Workflow that extracts invoice line items from natural language orders, compiles a professional PDF, saves records, and simulates client delivery.",
            "import_path": "src.modules.week2.invoice_automation.ui",
            "icon": "📄"
        },
        "attendance": {
            "title": "Attendance Automation Prototype",
            "developer": "MUHAMMAD WASIM",
            "role": "Group Member",
            "email": "muhammadwasimpukhtoon@gmail.com",
            "status": "Placeholder (Scaffolding Ready)",
            "difficulty": "Advanced",
            "tech": ["Python", "Pandas", "NumPy", "Flask/FastAPI", "QR/Geofencing tracking logic"],
            "description": "Automated employee and intern attendance-tracking workflow supporting location-based or QR check-ins.",
            "import_path": "src.modules.week2.attendance.ui",
            "icon": "🕒"
        },
        "hr_proposal": {
            "title": "HR Automation Proposal",
            "developer": "Muhammad Faozan Mujtaba",
            "role": "Group Member",
            "email": "fozanmujtaba.480@gmail.com",
            "status": "Placeholder (Scaffolding Ready)",
            "difficulty": "Intermediate",
            "tech": ["Python", "Pandas", "NumPy", "LLM API / NLP", "Streamlit/FastAPI"],
            "description": "Automated onboarding pipeline and leave-request ticketing system template for corporate businesses.",
            "import_path": "src.modules.week2.hr_proposal.ui",
            "icon": "📋"
        },
        "email_assistant": {
            "title": "AI Email Assistant Prototype",
            "developer": "Shahidullah",
            "role": "Group Member",
            "email": "shahidullahkhan091@gmail.com",
            "status": "Placeholder (Scaffolding Ready)",
            "difficulty": "Advanced",
            "tech": ["Python", "Pandas / NumPy", "NLP (spaCy/NLTK) / LLM API", "Streamlit/FastAPI"],
            "description": "Automated response drafting assistant for common customer service and support email inquiries.",
            "import_path": "src.modules.week2.email_assistant.ui",
            "icon": "✉️"
        },
        "report_generator": {
            "title": "AI Report Generator Prototype",
            "developer": "Ali Ammar Haider",
            "role": "Group Member",
            "email": "ahwheh688@gmail.com",
            "status": "Placeholder (Scaffolding Ready)",
            "difficulty": "Intermediate",
            "tech": ["Python", "Pandas", "NumPy", "Report Generation Engine"],
            "description": "Data aggregation script that turns raw business metrics (sales, tasks, attendance) into a formatted weekly business report.",
            "import_path": "src.modules.week2.report_generator.ui",
            "icon": "📊"
        },
        "resume_screening": {
            "title": "Resume Screening Prototype",
            "developer": "Abdul Haseeb",
            "role": "Group Member",
            "email": "abdlhaseeb17@gmail.com",
            "status": "Placeholder (Scaffolding Ready)",
            "difficulty": "Advanced",
            "tech": ["Python", "Pandas / NumPy", "spaCy / Embeddings matching", "Streamlit"],
            "description": "Automated recruitment tool scoring sample resume text files against job description keywords and semantic similarity.",
            "import_path": "src.modules.week2.resume_screening.ui",
            "icon": "🔍"
        },
        "ocr_document": {
            "title": "OCR / Document Processing Prototype",
            "developer": "Hammad Abbas",
            "role": "Group Member",
            "email": "hammadhadid723@gmail.com",
            "status": "Placeholder (Scaffolding Ready)",
            "difficulty": "Intermediate",
            "tech": ["Python", "Pandas", "OCR Library (PyTesseract/EasyOCR)", "LLM/NLP extraction"],
            "description": "Scanned document scanner extracting structured metadata (vendor name, date, invoice amount) from images and PDFs.",
            "import_path": "src.modules.week2.ocr_document.ui",
            "icon": "🖨️"
        },
        "predictive_analytics": {
            "title": "Predictive Analytics Mini-Study",
            "developer": "Ali Zaib",
            "role": "Group Member",
            "email": "aliofficialzaib@gmail.com",
            "status": "Placeholder (Scaffolding Ready)",
            "difficulty": "Advanced",
            "tech": ["Python", "Pandas / NumPy", "scikit-learn (Regression/Classification)"],
            "description": "Forecasting module using historical sample/public datasets to predict key business KPIs like churn rates or demand trends.",
            "import_path": "src.modules.week2.predictive_analytics.ui",
            "icon": "📈"
        }
    }
}
