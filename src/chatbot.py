# ==============================================================================
# SafeX AI FAQ Chatbot - Orchestrator
# ==============================================================================
import time
from pathlib import Path
from typing import Dict, Any, Optional
from src.knowledge_base import load_faq_data
from src.similarity import FAQSimilarityModel
from src.config import SIMILARITY_THRESHOLD, FALLBACK_MESSAGE

class FAQChatbot:
    """
    Orchestration class that coordinates loading the FAQ knowledge base,
    fitting the similarity engine, and running user query evaluation.
    """
    def __init__(self, faq_path: Path):
        self.faq_path = faq_path
        
        # Load FAQ dataset
        self.faqs = load_faq_data(faq_path)
        
        # Extract questions for the vectorizer
        self.questions = [faq["question"] for faq in self.faqs]
        
        # Initialize and fit similarity model
        self.similarity_model = FAQSimilarityModel()
        self.similarity_model.fit(self.questions)
        
    def query(self, user_query: str, threshold: Optional[float] = None) -> Dict[str, Any]:
        """
        Executes query matching workflow:
        1. Finds best matching FAQ question.
        2. Compares score against configured threshold.
        3. Returns either the FAQ answer or the fallback message.
        """
        start_time = time.time()
        
        # Use provided override or configuration default threshold
        active_threshold = threshold if threshold is not None else SIMILARITY_THRESHOLD
        
        # Get matching score and index
        best_idx, score = self.similarity_model.find_best_match(user_query)
        matched_faq = self.faqs[best_idx]
        
        # Threshold logic
        if score >= active_threshold:
            answer = matched_faq["answer"]
            is_fallback = False
        else:
            answer = FALLBACK_MESSAGE
            is_fallback = True
            
        latency = time.time() - start_time
        
        return {
            "query": user_query,
            "answer": answer,
            "matched_question": matched_faq["question"],
            "similarity_score": score,
            "is_fallback": is_fallback,
            "latency_seconds": latency,
            "faq_id": matched_faq["id"],
            "category": matched_faq["category"]
        }
