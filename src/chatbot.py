# ==============================================================================
# SafeX RAG - Chatbot Runtime Query Engine
# ==============================================================================
import time
from typing import List, Dict, Any, Tuple
from abc import ABC, abstractmethod
from pathlib import Path
import google.generativeai as genai
from src.pipeline.vector_store import VectorStore
from src.pipeline.embeddings import get_embedding_provider
from src.config.settings import (
    GEMINI_API_KEY, 
    DEFAULT_LLM_MODEL, 
    TOP_K_RETRIEVAL, 
    RETRIEVAL_THRESHOLD,
    VECTOR_STORE_DIR,
    logger
)
from src.config.prompts import RAG_SYSTEM_PROMPT, RAG_USER_PROMPT_TEMPLATE

class LLMProvider(ABC):
    """
    Abstract interface for LLM operations.
    Enables swappability of Gemini with other providers (like OpenAI or local LLMs).
    """
    @abstractmethod
    def generate_response(self, system_instruction: str, user_prompt: str) -> str:
        pass


class GeminiLLMProvider(LLMProvider):
    """
    Default LLM client wrapping Google's Gemini SDK.
    """
    def __init__(self, model_name: str = DEFAULT_LLM_MODEL):
        self.model_name = model_name
        logger.info(f"Initializing GeminiLLMProvider with model: {self.model_name}")
        
        if GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
        else:
            logger.warning("GEMINI_API_KEY is not configured. Live LLM calls will fail.")

    def generate_response(self, system_instruction: str, user_prompt: str) -> str:
        try:
            # We use GenerativeModel and provide system instructions in the model configuration
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_instruction
            )
            logger.debug("Dispatching API request to Gemini...")
            response = model.generate_content(
                user_prompt,
                generation_config={"temperature": 0.2}  # Low temperature for factual RAG responses
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini LLM API call failed: {e}")
            raise e


class MockLLMProvider(LLMProvider):
    """
    Offline/mock LLM generator. Returns mock answers based on retrieved context.
    Ensures interns can run the full UI loop without credentials.
    """
    def __init__(self, model_name: str = "mock-llm"):
        self.model_name = model_name
        logger.warning(f"Initializing MockLLMProvider (Offline Mode). Model name: {self.model_name}")

    def generate_response(self, system_instruction: str, user_prompt: str) -> str:
        time.sleep(0.8) # Simulate LLM generation latency
        
        # Simple heuristic response logic for mock
        if "Context:" in user_prompt:
            # Extract context block
            context_part = user_prompt.split("User Query:")[0]
            # Check if there is actual content beyond placeholders
            if "[PDF PLURAL PLACEHOLDER]" in context_part or "placeholder" in context_part.lower():
                return "I see placeholder context in the database, so I cannot form a real answer. Please load raw files and build the index."
            
            # Simple keyword mock response
            if "safex" in user_prompt.lower():
                return "[Offline Mock Answer] Based on the context, SafeX Solutions is an organization offering AI/ML solutions and internships. For actual answers, configure your GEMINI_API_KEY in the .env file."
                
        return "[Offline Mock Answer] I am sorry, but I do not have information to answer that question based on my current knowledge base."


class RAGAssistant:
    """
    Orchestration class that coordinates document retrieval and generation.
    """
    def __init__(self, index_file: Path, provider_type: str = "gemini"):
        self.provider_type = provider_type
        
        # Initialize swappable Embedding Client
        self.embedding_provider = get_embedding_provider(provider_type)
        
        # Load Vector Store Index
        try:
            self.vector_store = VectorStore.load(index_file, self.embedding_provider)
            logger.info("RAGAssistant vector index successfully loaded.")
        except Exception as e:
            logger.error(f"Failed to load vector store at {index_file}: {e}")
            logger.warning("Initializing RAGAssistant with an empty index.")
            self.vector_store = VectorStore(self.embedding_provider)

        # Initialize swappable LLM client
        if provider_type.lower() == "gemini":
            if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
                logger.warning("No Gemini API key found. Falling back to MockLLMProvider.")
                self.llm_provider = MockLLMProvider()
            else:
                self.llm_provider = GeminiLLMProvider()
        else:
            self.llm_provider = MockLLMProvider()

    def query(self, user_query: str) -> Dict[str, Any]:
        """
        Executes the full RAG pipeline:
        1. Query -> Retrieval (similarity search)
        2. Context format -> LLM Query
        3. LLM generation -> Response
        """
        start_time = time.time()
        logger.info(f"RAG query received: '{user_query}'")
        
        # 1. Retrieve matching chunks
        retrieved_docs_with_scores = self.vector_store.similarity_search(
            query=user_query,
            top_k=TOP_K_RETRIEVAL,
            threshold=RETRIEVAL_THRESHOLD
        )
        
        latency_retrieval = time.time() - start_time
        logger.info(f"Retrieval step completed in {latency_retrieval:.4f}s. Found {len(retrieved_docs_with_scores)} matches.")
        
        # Formulate sources metadata list for Streamlit return
        sources = []
        context_chunks_texts = []
        
        for idx, (doc, score) in enumerate(retrieved_docs_with_scores):
            sources.append({
                "source": doc.metadata.get("source", "Unknown"),
                "type": doc.metadata.get("type", "txt"),
                "text": doc.text,
                "score": float(score)
            })
            # Combine text and metadata for context construction
            context_chunks_texts.append(
                f"[Source: {doc.metadata.get('source')} (Type: {doc.metadata.get('type')})]\n{doc.text}"
            )
            
        # 2. Synthesize prompt
        if context_chunks_texts:
            context_text = "\n\n".join(context_chunks_texts)
        else:
            context_text = "No relevant context found in the vector database."
            
        user_prompt = RAG_USER_PROMPT_TEMPLATE.format(
            context_text=context_text,
            query=user_query
        )
        
        # 3. Call LLM
        logger.info("Generating response from LLM...")
        llm_start_time = time.time()
        try:
            answer = self.llm_provider.generate_response(
                system_instruction=RAG_SYSTEM_PROMPT,
                user_prompt=user_prompt
            )
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            answer = "I'm sorry, an error occurred while generating the answer. Please check the logs."
            
        latency_generation = time.time() - llm_start_time
        total_latency = time.time() - start_time
        
        logger.info(f"Generation step completed in {latency_generation:.4f}s. Total RAG latency: {total_latency:.4f}s.")
        
        return {
            "answer": answer.strip(),
            "sources": sources,
            "latency": {
                "retrieval_seconds": latency_retrieval,
                "generation_seconds": latency_generation,
                "total_seconds": total_latency
            }
        }
