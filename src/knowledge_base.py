# ==============================================================================
# SafeX AI FAQ Chatbot - Knowledge Base Loader
# ==============================================================================
import json
from pathlib import Path
from typing import List, Dict

def load_faq_data(filepath: Path) -> List[Dict[str, str]]:
    """
    Loads and validates FAQ question-answer pairs from a JSON file.
    
    Expected format:
    [
        {
            "id": "faq_01",
            "category": "Category Name",
            "question": "Question text?",
            "answer": "Answer text."
        },
        ...
    ]
    
    Raises FileNotFoundError if file is missing, and ValueError if structure is invalid.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Knowledge base JSON file not found at: {filepath}")
        
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse knowledge base JSON. Invalid syntax: {e}")
            
    if not isinstance(data, list):
        raise ValueError("Knowledge base JSON root must be a list of QA pairs.")
        
    validated_faqs = []
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"FAQ item at index {idx} is not a valid JSON object.")
            
        if "question" not in item or "answer" not in item:
            raise ValueError(f"FAQ item at index {idx} is missing required 'question' or 'answer' keys.")
            
        question = item["question"].strip()
        answer = item["answer"].strip()
        
        if not question or not answer:
            raise ValueError(f"FAQ item at index {idx} contains an empty 'question' or 'answer' field.")
            
        validated_faqs.append({
            "id": item.get("id", f"faq_{idx + 1}"),
            "category": item.get("category", "General").strip(),
            "question": question,
            "answer": answer
        })
        
    return validated_faqs
