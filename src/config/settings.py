# ==============================================================================
# SafeX RAG - Configuration Settings Loader
# ==============================================================================
import os
from pathlib import Path
from dotenv import load_dotenv
from src.logger import setup_logger

# Load environment variables from .env file
load_dotenv()

# Project Root Directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Resolve settings from environment variables or defaults
ENV_MODE = os.getenv("ENV_MODE", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Initialize and configure logging based on settings
logger = setup_logger(name="safex_rag", log_level=LOG_LEVEL, log_file=str(ROOT_DIR / "safex_rag.log"))

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check for API Key at startup
if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    logger.warning("GEMINI_API_KEY is not set or using placeholder in .env. LLM calls will fail until configured.")

# Data Directories (with fallback to project root folder paths)
RAW_DATA_DIR = ROOT_DIR / os.getenv("RAW_DATA_DIR", "data/raw")
PROCESSED_DATA_DIR = ROOT_DIR / os.getenv("PROCESSED_DATA_DIR", "data/processed")
VECTOR_STORE_DIR = ROOT_DIR / os.getenv("VECTOR_STORE_DIR", "data/vector_store")

# Ensure critical data directories exist
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, VECTOR_STORE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Default Model Selection (Configured for easy swappability)
# Google Gemini defaults
DEFAULT_LLM_MODEL = "gemini-1.5-flash"
DEFAULT_EMBEDDING_MODEL = "models/text-embedding-004"

# RAG Hyperparameters
CHUNK_SIZE = 500       # Character limit per text chunk
CHUNK_OVERLAP = 50     # Overlapping characters between consecutive chunks
TOP_K_RETRIEVAL = 3    # Number of chunks retrieved to answer a query
RETRIEVAL_THRESHOLD = 0.3 # Minimum cosine similarity score for relevance

# Export variables
__all__ = [
    "ROOT_DIR",
    "ENV_MODE",
    "LOG_LEVEL",
    "GEMINI_API_KEY",
    "RAW_DATA_DIR",
    "PROCESSED_DATA_DIR",
    "VECTOR_STORE_DIR",
    "DEFAULT_LLM_MODEL",
    "DEFAULT_EMBEDDING_MODEL",
    "CHUNK_SIZE",
    "CHUNK_OVERLAP",
    "TOP_K_RETRIEVAL",
    "RETRIEVAL_THRESHOLD",
    "logger"
]
