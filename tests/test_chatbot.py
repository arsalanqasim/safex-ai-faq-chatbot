# ==============================================================================
# SafeX AI FAQ Chatbot - Unit Tests
# ==============================================================================
import os
import json
import tempfile
import pytest
from pathlib import Path

from src.utils import preprocess_text
from src.knowledge_base import load_faq_data
from src.similarity import FAQSimilarityModel
from src.chatbot import FAQChatbot
from src.config import FALLBACK_MESSAGE

# ------------------------------------------------------------------------------
# Test Text Preprocessing
# ------------------------------------------------------------------------------
def test_preprocess_text():
    """Verifies text normalization (lowercasing, punctuation removal, whitespace)."""
    assert preprocess_text("Hello World!") == "hello world"
    assert preprocess_text("SafeX Solutions - AI/ML Cohort") == "safex solutions aiml cohort"
    assert preprocess_text("   Double   Space   ") == "double space"
    assert preprocess_text("") == ""
    assert preprocess_text(None) == ""

# ------------------------------------------------------------------------------
# Test FAQ JSON Loading
# ------------------------------------------------------------------------------
def test_load_faq_data_valid():
    """Verifies that the FAQ loader correctly parses a valid JSON structure."""
    mock_data = [
        {
            "id": "faq_test_1",
            "category": "Test Category",
            "question": "What is the test question?",
            "answer": "This is the test answer."
        }
    ]
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w", encoding="utf-8") as tmp:
        json.dump(mock_data, tmp)
        tmp_path = Path(tmp.name)
        
    try:
        faqs = load_faq_data(tmp_path)
        assert len(faqs) == 1
        assert faqs[0]["id"] == "faq_test_1"
        assert faqs[0]["question"] == "What is the test question?"
        assert faqs[0]["answer"] == "This is the test answer."
        assert faqs[0]["category"] == "Test Category"
    finally:
        os.remove(tmp_path)

def test_load_faq_data_invalid_keys():
    """Verifies that FAQ loader raises ValueError when keys are missing."""
    mock_data = [{"question": "No answer key?"}]
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w", encoding="utf-8") as tmp:
        json.dump(mock_data, tmp)
        tmp_path = Path(tmp.name)
        
    try:
        with pytest.raises(ValueError, match="missing required 'question' or 'answer'"):
            load_faq_data(tmp_path)
    finally:
        os.remove(tmp_path)

# ------------------------------------------------------------------------------
# Test Similarity Calculations
# ------------------------------------------------------------------------------
def test_similarity_model():
    """Verifies TF-IDF cosine similarity vector math and indexing."""
    questions = [
        "Who is the founder of SafeX Solutions?",
        "What are the office hours?",
        "How is performance evaluated?"
    ]
    model = FAQSimilarityModel()
    model.fit(questions)
    
    # query: "tell me about the founder" (should match founder question)
    idx, score = model.find_best_match("tell me about the founder")
    assert idx == 0
    assert score > 0.0
    
    # query: "office hours" (exact match should yield near 1.0)
    idx, score = model.find_best_match("What are the office hours?")
    assert idx == 1
    assert score == pytest.approx(1.0)

# ------------------------------------------------------------------------------
# Test Chatbot Execution Flow
# ------------------------------------------------------------------------------
def test_chatbot_query_success():
    """Verifies chatbot returns the correct answer when similarity is above threshold."""
    mock_data = [
        {"id": "faq_1", "question": "Who founded SafeX?", "answer": "Founded by Ateeq Ullah."},
        {"id": "faq_2", "question": "What hours?", "answer": "9 to 5."}
    ]
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w", encoding="utf-8") as tmp:
        json.dump(mock_data, tmp)
        tmp_path = Path(tmp.name)
        
    try:
        chatbot = FAQChatbot(tmp_path)
        # Using a low threshold (0.2) to guarantee a match
        res = chatbot.query("Who founded SafeX?", threshold=0.2)
        assert res["answer"] == "Founded by Ateeq Ullah."
        assert res["is_fallback"] is False
        assert res["similarity_score"] > 0.5
    finally:
        os.remove(tmp_path)

def test_chatbot_query_fallback():
    """Verifies chatbot returns the fallback message when similarity is below threshold."""
    mock_data = [
        {"id": "faq_1", "question": "Who founded SafeX?", "answer": "Founded by Ateeq Ullah."}
    ]
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w", encoding="utf-8") as tmp:
        json.dump(mock_data, tmp)
        tmp_path = Path(tmp.name)
        
    try:
        chatbot = FAQChatbot(tmp_path)
        # Querying unrelated topic with high threshold (0.8)
        res = chatbot.query("What is the recipe for cooking lasagna?", threshold=0.8)
        assert res["answer"] == FALLBACK_MESSAGE
        assert res["is_fallback"] is True
    finally:
        os.remove(tmp_path)
