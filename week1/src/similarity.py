# ==============================================================================
# SafeX AI FAQ Chatbot - Similarity Engine
# ==============================================================================
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class FAQSimilarityModel:
    """
    Fits representation vectors over FAQ questions and computes cosine similarity
    against incoming queries to identify closest matches.
    """
    def __init__(self):
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words="english")
        self.questions: List[str] = []
        self.question_matrix = None

    def fit(self, questions: List[str]):
        """
        Fits the similarity model on the FAQ questions list.

        Parameters:
            questions (List[str]): List of all FAQ questions.
        """
        self.questions = questions
        self.question_matrix = self.vectorizer.fit_transform(questions)

    def find_best_match(self, query: str) -> Tuple[int, float]:
        """
        Calculates cosine similarity and returns the best matching FAQ item.

        Parameters:
            query (str): Cleaned user input query.

        Returns:
            Tuple[int, float]: index of the matched question and its similarity score.
        """
        if self.question_matrix is None or not self.questions:
            return -1, 0.0

        query_vector = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vector, self.question_matrix)[0]

        best_index = int(scores.argmax())
        best_score = float(scores[best_index])
        return best_index, best_score
