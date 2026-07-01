# ==============================================================================
# SafeX RAG Pipeline - Lightweight Vector Store (Numpy & Pickle)
# ==============================================================================
import pickle
from pathlib import Path
from typing import List, Tuple, Dict, Any
import numpy as np
from src.pipeline.load_documents import Document
from src.pipeline.embeddings import EmbeddingProvider, get_embedding_provider
from src.config.settings import logger, VECTOR_STORE_DIR

class VectorStore:
    """
    A lightweight, robust Vector Database using Numpy for cosine similarity
    computation and Pickle for serialized local storage.
    """
    def __init__(self, embedding_provider: EmbeddingProvider):
        self.embedding_provider = embedding_provider
        self.documents: List[Document] = []
        self.embeddings: np.ndarray = np.empty((0, 0))

    def add_documents(self, documents: List[Document], embeddings: List[List[float]]):
        """
        Appends documents and their pre-computed embeddings to the index.
        """
        if len(documents) != len(embeddings):
            raise ValueError("The number of documents must match the number of embeddings.")
            
        if not documents:
            logger.warning("No documents provided to add_documents.")
            return

        # Convert embeddings list to numpy array
        new_embeddings = np.array(embeddings, dtype=np.float32)
        
        self.documents.extend(documents)
        
        if self.embeddings.size == 0:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
            
        logger.info(f"Added {len(documents)} chunks to the vector store. Total size: {len(self.documents)}")

    def similarity_search(self, query: str, top_k: int = 3, threshold: float = 0.0) -> List[Tuple[Document, float]]:
        """
        Embeds the query and computes cosine similarity against all stored embeddings.
        Returns a list of (Document, similarity_score) tuples, sorted descending.
        """
        if not self.documents or self.embeddings.size == 0:
            logger.warning("Attempted similarity search on an empty vector store.")
            return []

        # Embed query text
        logger.debug(f"Embedding query for search: '{query}'")
        query_vector = np.array(self.embedding_provider.embed_text(query), dtype=np.float32)
        
        # Calculate Cosine Similarity: dot(A, B) / (norm(A) * norm(B))
        # 1. Norm of query vector
        query_norm = np.linalg.norm(query_vector)
        if query_norm == 0:
            logger.error("Query embedding vector norm is zero. Cannot compute similarity.")
            return []
            
        # 2. Norm of all stored vectors
        doc_norms = np.linalg.norm(self.embeddings, axis=1)
        # Avoid division by zero
        doc_norms = np.where(doc_norms == 0, 1e-10, doc_norms)
        
        # 3. Dot product and division
        dot_products = np.dot(self.embeddings, query_vector)
        similarities = dot_products / (doc_norms * query_norm)
        
        # Zip documents and their scores
        results = list(zip(self.documents, similarities))
        
        # Sort by similarity score descending
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Filter by threshold and take top_k
        filtered_results = [res for res in results if res[1] >= threshold]
        
        logger.debug(f"Found {len(filtered_results)} matches above threshold {threshold}. Returning top {top_k}.")
        return filtered_results[:top_k]

    def save(self, filepath: Path):
        """
        Serializes and saves the database index to a pickle file.
        """
        logger.info(f"Saving vector store index to: {filepath}")
        
        # Ensure parent directories exist
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Save both document objects (text + metadata) and raw numpy embeddings
        data = {
            "documents": [doc.to_dict() for doc in self.documents],
            "embeddings": self.embeddings
        }
        
        with open(filepath, "wb") as f:
            pickle.dump(data, f)
            
        logger.info("Vector store index saved successfully.")

    @classmethod
    def load(cls, filepath: Path, embedding_provider: EmbeddingProvider) -> 'VectorStore':
        """
        Loads and reconstructs a VectorStore from a saved index file.
        """
        logger.info(f"Loading vector store index from: {filepath}")
        
        if not filepath.exists():
            raise FileNotFoundError(f"No vector store file found at {filepath}")
            
        with open(filepath, "rb") as f:
            data = pickle.load(f)
            
        instance = cls(embedding_provider)
        
        # Reconstruct Document objects from serialized dicts
        documents_data = data.get("documents", [])
        instance.documents = [Document(d["text"], d["metadata"]) for d in documents_data]
        instance.embeddings = data.get("embeddings", np.empty((0, 0)))
        
        logger.info(f"Vector store index loaded successfully. Total chunks loaded: {len(instance.documents)}")
        return instance


def build_and_save_index(raw_dir: Path, store_filepath: Path, provider_type: str = "gemini"):
    """
    Executes the ingestion pipeline (Load -> Clean -> Chunk -> Embed -> Index -> Save).
    """
    logger.info("=== STARTING VECTOR STORE INDEX BUILD PIPELINE ===")
    
    # 1. Load documents
    from src.pipeline.load_documents import load_all_documents
    docs = load_all_documents(raw_dir)
    if not docs:
        logger.error("No raw files found. Index construction aborted.")
        return
        
    # 2. Clean documents
    from src.pipeline.clean import clean_all_documents
    cleaned_docs = clean_all_documents(docs)
    
    # 3. Chunk documents
    from src.pipeline.chunk import chunk_all_documents
    chunks = chunk_all_documents(cleaned_docs)
    
    # 4. Get embedding client and generate vectors
    provider = get_embedding_provider(provider_type)
    chunk_texts = [c.text for c in chunks]
    
    logger.info(f"Generating embeddings for {len(chunk_texts)} chunks...")
    embeddings = provider.embed_batch(chunk_texts)
    
    # 5. Populate and save index
    vstore = VectorStore(provider)
    vstore.add_documents(chunks, embeddings)
    vstore.save(store_filepath)
    
    logger.info("=== INDEX BUILD PIPELINE COMPLETED SUCCESSFULLY ===")
    return vstore

if __name__ == "__main__":
    # Test script to run index construction stand-alone
    # Sets up paths using config settings
    import sys
    from src.config.settings import RAW_DATA_DIR
    
    target_db_path = VECTOR_STORE_DIR / "vector_index.pkl"
    build_and_save_index(RAW_DATA_DIR, target_db_path, provider_type="gemini")
