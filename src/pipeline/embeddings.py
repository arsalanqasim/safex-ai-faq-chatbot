# ==============================================================================
# SafeX RAG Pipeline - Decoupled Vector Embeddings Generator
# ==============================================================================
import time
from typing import List
from abc import ABC, abstractmethod
import google.generativeai as genai
from src.config.settings import GEMINI_API_KEY, DEFAULT_EMBEDDING_MODEL, logger

class EmbeddingProvider(ABC):
    """
    Abstract interface for embedding generation. 
    Allows easily swapping Gemini embeddings for OpenAI, HuggingFace, etc.
    """
    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Generates a numerical embedding vector for a single string."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generates embedding vectors for a list of strings."""
        pass


class GeminiEmbeddingProvider(EmbeddingProvider):
    """
    Default embedding generator using Google's Gemini SDK.
    """
    def __init__(self, model_name: str = DEFAULT_EMBEDDING_MODEL):
        self.model_name = model_name
        logger.info(f"Initializing GeminiEmbeddingProvider with model: {self.model_name}")
        
        # Configure the Google SDK
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
        else:
            logger.warning("GEMINI_API_KEY not detected. API calls will fail.")

    def embed_text(self, text: str) -> List[float]:
        try:
            response = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_query"
            )
            return response["embedding"]
        except Exception as e:
            logger.error(f"Gemini API single embedding call failed: {e}")
            raise e

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        logger.debug(f"Generating Gemini embeddings for batch of {len(texts)} chunks...")
        try:
            # Note: Gemini embed_content handles batching automatically when content is a list
            # We can run it in chunks to avoid API rate limits if necessary, but keep it simple here.
            response = genai.embed_content(
                model=self.model_name,
                content=texts,
                task_type="retrieval_document"
            )
            return response["embedding"]
        except Exception as e:
            logger.error(f"Gemini API batch embedding call failed: {e}")
            raise e


class MockEmbeddingProvider(EmbeddingProvider):
    """
    Fallback mock embedding provider. Generates random/dummy 768-dimension vectors.
    Useful for offline testing or when API keys are not yet configured.
    """
    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        logger.warning(f"Initializing MockEmbeddingProvider (Offline / Dummy Embeddings). Dimension: {self.dimension}")

    def embed_text(self, text: str) -> List[float]:
        # Simple deterministic mock embedding based on character values
        import random
        random.seed(sum(ord(c) for c in text))
        return [random.uniform(-1.0, 1.0) for _ in range(self.dimension)]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        # Add a artificial small delay to mimic API latency
        time.sleep(0.1)
        return [self.embed_text(text) for text in texts]


def get_embedding_provider(provider_type: str = "gemini") -> EmbeddingProvider:
    """
    Factory function to retrieve selected embedding client.
    """
    if provider_type.lower() == "gemini":
        if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
            logger.warning("No Gemini API key found. Falling back to MockEmbeddingProvider.")
            return MockEmbeddingProvider()
        return GeminiEmbeddingProvider()
    elif provider_type.lower() == "mock":
        return MockEmbeddingProvider()
    else:
        logger.error(f"Unknown embedding provider '{provider_type}'. Falling back to Mock.")
        return MockEmbeddingProvider()
