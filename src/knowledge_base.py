# ==============================================================================
# SafeX AI FAQ Chatbot - Knowledge Base Loader (Skeleton)
# ==============================================================================

import json
from pathlib import Path
from typing import List, Dict

def load_faq_data(filepath: Path) -> List[Dict[str, str]]:
    if not filepath.exists():
        raise FileNotFoundError(f"FAQ file not found: {filepath}")

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        validated = []

        for item in data:
            if "question" in item and "answer" in item:
                validated.append({
                    "question": item["question"],
                    "answer": item["answer"]
                })

        return validated

    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format.")
