# ==============================================================================
# SafeX RAG - Unit and Integration Tests
# ==============================================================================
import os
import tempfile
import json
from pathlib import Path
import pytest
import numpy as np

from src.pipeline.load_documents import Document, load_text_file, load_json_faq_file
from src.pipeline.clean import clean_html_boilerplate, clean_document
from src.pipeline.chunk import split_text, chunk_document
from src.pipeline.embeddings import get_embedding_provider, MockEmbeddingProvider
from src.pipeline.vector_store import VectorStore
from src.chatbot import RAGAssistant

# ------------------------------------------------------------------------------
# Test Ingestion & Loaders
# ------------------------------------------------------------------------------
def test_text_loader():
    """Checks that the text loader correctly parses content and builds Document metadata."""
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write("Hello SafeX Solutions Team!")
        tmp_path = Path(tmp.name)
        
    try:
        docs = load_text_file(tmp_path)
        assert len(docs) == 1
        assert docs[0].text == "Hello SafeX Solutions Team!"
        assert docs[0].metadata["source"] == tmp_path.name
        assert docs[0].metadata["type"] == "txt"
    finally:
        os.remove(tmp_path)


def test_json_faq_loader():
    """Checks that JSON loaders correctly extract QA pairs into combined text documents."""
    faq_data = [
        {"question": "What is SafeX?", "answer": "SafeX is an AI agency."},
        {"question": "Is it remote?", "answer": "Yes."}
    ]
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w", encoding="utf-8") as tmp:
        json.dump(faq_data, tmp)
        tmp_path = Path(tmp.name)
        
    try:
        docs = load_json_faq_file(tmp_path)
        assert len(docs) == 2
        assert "Question: What is SafeX?" in docs[0].text
        assert "Answer: SafeX is an AI agency." in docs[0].text
        assert docs[0].metadata["item_index"] == 0
    finally:
        os.remove(tmp_path)


# ------------------------------------------------------------------------------
# Test Text Cleaning
# ------------------------------------------------------------------------------
def test_html_cleaning():
    """Verifies regex removes scripts, styles, HTML tags, and whitespace."""
    raw_html = """
    <html>
        <head>
            <style>body {color: red;}</style>
            <script>console.log('hi');</script>
        </head>
        <body>
            <h1>SafeX Solutions</h1>
            <p>Welcome to the <b>AI/ML internship</b> program.</p>
        </body>
    </html>
    """
    cleaned = clean_html_boilerplate(raw_html)
    assert "body {color: red;}" not in cleaned
    assert "console.log" not in cleaned
    assert "SafeX Solutions" in cleaned
    assert "Welcome to the AI/ML internship program." in cleaned
    assert "<p>" not in cleaned


# ------------------------------------------------------------------------------
# Test Text Chunking
# ------------------------------------------------------------------------------
def test_text_splitting():
    """Verifies character-based sliding-window split sizes and overlap boundaries."""
    sample_text = "abcdefghij"  # 10 chars
    # Size 5, Overlap 2 -> Step = 3
    # Chunk 1: indices 0-5 (abcde)
    # Chunk 2: indices 3-8 (defgh)
    # Chunk 3: indices 6-10 (ghij)
    chunks = split_text(sample_text, chunk_size=5, chunk_overlap=2)
    assert len(chunks) == 3
    assert chunks[0] == "abcde"
    assert chunks[1] == "defgh"
    assert chunks[2] == "ghij"


# ------------------------------------------------------------------------------
# Test Vector Store similarity searches
# ------------------------------------------------------------------------------
def test_vector_store_numpy():
    """Verifies Numpy vector calculations and cosine similarity matching matches expected outputs."""
    mock_provider = MockEmbeddingProvider(dimension=3)
    vstore = VectorStore(mock_provider)
    
    doc1 = Document("Python RAG app", {"source": "doc1"})
    doc2 = Document("Cooking recipes", {"source": "doc2"})
    
    # Hand-craft deterministic embeddings
    # A = [1.0, 0.0, 0.0]  (Python RAG)
    # B = [0.0, 1.0, 0.0]  (Cooking)
    # Query = [0.9, 0.1, 0.0] (Should closely match doc1)
    embeddings = [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0]
    ]
    vstore.add_documents([doc1, doc2], embeddings)
    
    # Mock search execution embedding
    class DeterministicQueryProvider(MockEmbeddingProvider):
        def embed_text(self, text: str):
            return [1.0, 0.0, 0.0]
            
    vstore.embedding_provider = DeterministicQueryProvider(dimension=3)
    
    results = vstore.similarity_search("Python RAG", top_k=1)
    assert len(results) == 1
    assert results[0][0].metadata["source"] == "doc1"
    assert results[0][1] == pytest.approx(1.0) # Cosine similarity of identical vectors is 1.0
