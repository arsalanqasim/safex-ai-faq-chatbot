# ==============================================================================
# SafeX AI FAQ Chatbot - Orchestrator
# ==============================================================================
import time
from pathlib import Path
from typing import Dict, Any

from src.knowledge_base import load_faq_data
from src.similarity import FAQSimilarityModel
from src.config import DEFAULT_THRESHOLD, FALLBACK_MESSAGE

class FAQChatbot:
    """
    Coordinates the chatbot workflow by loading the knowledge base,
    fitting the similarity engine, and routing queries.
    """
    def __init__(self, faq_path: Path):
        """
        Parameters:
            faq_path (Path): Path to faq.json.
        """
        self.faq_path = faq_path
        # Load and validate the FAQ dataset
        self.faq_data = load_faq_data(faq_path)
        # Instantiate and fit the similarity model
        self.similarity_model = FAQSimilarityModel()
        questions = [item["question"] for item in self.faq_data]
        self.similarity_model.fit(questions)
        
    def query(self, user_query: str, threshold: float = None) -> Dict[str, Any]:
        """
        Routes user query, matches similarity, and checks fallback threshold.

        Parameters:
            user_query (str): The raw text question from the user.
            threshold (float, optional): Custom threshold override.

        Returns:
            Dict[str, Any]: Results containing matched question, score, answer, and latency.
        """
        start_time = time.perf_counter()
        
        if threshold is None:
            threshold = DEFAULT_THRESHOLD

        # Calculate similarity match
        best_index, best_score = self.similarity_model.find_best_match(user_query)
        
        # Enforce similarity threshold logic (score < threshold triggers fallback)
        if best_index != -1 and best_score >= threshold:
            matched_item = self.faq_data[best_index]
            answer = matched_item["answer"]
            matched_question = matched_item["question"]
            expected_answer_id = matched_item.get("id")
            is_fallback = False
        else:
            answer = FALLBACK_MESSAGE
            matched_question = None
            expected_answer_id = None
            is_fallback = True

        latency_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "query": user_query,
            "answer": answer,
            "matched_question": matched_question,
            "similarity_score": best_score,
            "expected_answer_id": expected_answer_id,
            "is_fallback": is_fallback,
            "latency_ms": latency_ms
        }
