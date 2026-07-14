# week1/src/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# File System Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
FAQ_PATH = DATA_DIR / "faq.json"
EVAL_DIR = BASE_DIR / "evaluation"
TEST_QUESTIONS_PATH = EVAL_DIR / "test_questions.json"

# Default Chatbot Parameters
DEFAULT_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.35"))
FALLBACK_MESSAGE = os.getenv(
    "FALLBACK_MESSAGE",
    "I couldn't find information about that. Please contact the SafeX team for further assistance."
)
