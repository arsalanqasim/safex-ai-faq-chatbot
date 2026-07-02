# ==============================================================================
# SafeX AI FAQ Chatbot - Text Preprocessing Utilities
# ==============================================================================
import re

def preprocess_text(text: str) -> str:
    """
    Normalizes a text string by:
    1. Converting to lowercase.
    2. Removing special punctuation (retaining alphanumeric characters and spaces).
    3. Stripping leading/trailing spaces and collapsing internal whitespace.
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove characters other than letters, numbers, and basic whitespaces
    text = re.sub(r"[^\w\s]", "", text)
    
    # Replace multiple whitespaces/newlines with a single space
    text = re.sub(r"\s+", " ", text)
    
    return text.strip()
