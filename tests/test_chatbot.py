# ==============================================================================
# SafeX AI FAQ Chatbot - Unit Tests
# ==============================================================================
import pytest
import tempfile
import os
from pathlib import Path

from src.knowledge_base import load_faq_data
from src.similarity import FAQSimilarityModel
from src.chatbot import FAQChatbot
from src.config import FAQ_PATH, FALLBACK_MESSAGE

def test_knowledge_base_loading():
    """
    Test case to verify JSON data loader.
    """
    # Test valid FAQ load
    data = load_faq_data(FAQ_PATH)
    assert isinstance(data, list)
    assert len(data) > 0
    for item in data:
        assert "question" in item
        assert "answer" in item
        assert "id" in item

    # Test file missing exception
    with pytest.raises(FileNotFoundError):
        load_faq_data(Path("nonexistent_file_path_12345.json"))

    # Test invalid JSON format
    fd, temp_path = tempfile.mkstemp(suffix=".json")
    try:
        with open(temp_path, "w") as f:
            f.write("{ invalid json")
        with pytest.raises(ValueError):
            load_faq_data(Path(temp_path))
    finally:
        os.close(fd)
        os.remove(temp_path)


def test_similarity_calculation():
    """
    Test case to verify similarity calculations.
    """
    model = FAQSimilarityModel()
    
    # Test queries when not fitted
    idx, score = model.find_best_match("What is SafeX?")
    assert idx == -1
    assert score == 0.0

    # Fit with mock questions
    questions = [
        "What is SafeX Solutions?",
        "How can I apply for leave?",
        "Where is the office located?"
    ]
    model.fit(questions)

    # Test exact match
    idx, score = model.find_best_match("What is SafeX Solutions?")
    assert idx == 0
    assert score > 0.99  # Should be close to 1.0

    # Test partial match
    idx, score = model.find_best_match("Apply leave query")
    assert idx == 1
    assert score > 0.0

    # Test unrelated query (completely different vocabulary)
    idx, score = model.find_best_match("lasagna recipe baking instruction")
    # Even if it matches something, score should be very low
    assert score < 0.2


def test_chatbot_fallback_triggering():
    """
    Test case to verify chatbot query and threshold fallbacks.
    """
    chatbot = FAQChatbot(FAQ_PATH)
    
    # Query with a highly relevant query
    res = chatbot.query("What is SafeX Solutions?")
    assert res["is_fallback"] is False
    assert "SafeX Solutions is a global technology" in res["answer"]
    assert res["similarity_score"] > 0.8
    assert res["expected_answer_id"] == 1

    # Query with a completely irrelevant query triggering fallback
    res_fallback = chatbot.query("cooking recipe for biryani")
    assert res_fallback["is_fallback"] is True
    assert res_fallback["answer"] == FALLBACK_MESSAGE
    assert res_fallback["expected_answer_id"] is None
    
    # Query with custom high threshold
    res_high_thresh = chatbot.query("What is SafeX?", threshold=0.99)
    # The score should be high but less than 0.99, triggering fallback
    assert res_high_thresh["is_fallback"] is True
    assert res_high_thresh["answer"] == FALLBACK_MESSAGE
