# ==============================================================================
# SafeX AI FAQ Chatbot - Similarity Matching Engine
# ==============================================================================
from typing import List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.utils import preprocess_text

class FAQSimilarityModel:
    """
    Fits a TF-IDF vectorizer over FAQ questions, transforms user queries,
    and computes cosine similarities to find the closest FAQ item.
    """
    def __init__(self):
        self.vectorizer = TfidfVectorizer(preprocessor=preprocess_text, stop_words='english')
        self.tfidf_matrix = None
        self.questions = []
        
    def fit(self, questions: List[str]):
        """
        Fits the TF-IDF model on a list of FAQ questions.
        """
        if not questions:
            raise ValueError("Cannot fit similarity model on an empty list of questions.")
            
        self.questions = questions
        self.tfidf_matrix = self.vectorizer.fit_transform(questions)
        
    def find_best_match(self, query: str) -> Tuple[int, float]:
        """
        Computes cosine similarity between query and all stored questions.
        Returns the index of the highest similarity question and the similarity score.
        """
        if self.tfidf_matrix is None:
            raise ValueError("Similarity model has not been fit on a dataset yet.")
            
        if not query.strip():
            # For empty query, return first item with 0.0 similarity
            return 0, 0.0
            
        # Vectorize the query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate cosine similarity against all questions in knowledge base
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Identify the best matching question index and score
        best_index = int(np.argmax(similarities))
        best_score = float(similarities[best_index])
        
        return best_index, best_score
