# ==============================================================================
# SafeX AI FAQ Chatbot - Configuration Settings
# ==============================================================================
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Project Root and File System Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
FAQ_PATH = DATA_DIR / "faq.json"

EVAL_DIR = BASE_DIR / "evaluation"
TEST_QUESTIONS_PATH = EVAL_DIR / "test_questions.json"
EVAL_RESULTS_PATH = EVAL_DIR / "evaluation_results.csv"

# Chatbot Algorithmic Configuration
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.35"))
FALLBACK_MESSAGE = os.getenv(
    "FALLBACK_MESSAGE",
    "I couldn't find information about that. Please contact the SafeX team for further assistance."
)

# UI Metadata Configuration
APP_TITLE = "SafeX FAQ Chatbot"
APP_SUBTITLE = "AI-powered Semantic FAQ Assistant"
