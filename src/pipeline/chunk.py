# ==============================================================================
# SafeX RAG Pipeline - Text Chunking & Splitting
# ==============================================================================
from typing import List
from src.pipeline.load_documents import Document
from src.config.settings import CHUNK_SIZE, CHUNK_OVERLAP, logger

def split_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    Splits text into chunks of character length `chunk_size` with `chunk_overlap` characters of overlap.
    A basic sliding-window approach that is easy to read and debug.
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        
        # Advance sliding window by (chunk_size - overlap)
        # Avoid infinite loop if overlap is larger than size
        step = max(1, chunk_size - chunk_overlap)
        start += step
        
    return chunks


def chunk_document(doc: Document, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[Document]:
    """
    Splits a single Document into multiple smaller Document chunks.
    Maintains parent metadata and appends chunk-specific metadata (index and total count).
    """
    logger.debug(f"Chunking document '{doc.metadata.get('source')}' with size={chunk_size}, overlap={chunk_overlap}")
    
    raw_chunks = split_text(doc.text, chunk_size, chunk_overlap)
    chunked_documents = []
    
    total_chunks = len(raw_chunks)
    for idx, text_chunk in enumerate(raw_chunks):
        metadata = doc.metadata.copy()
        metadata.update({
            "chunk_index": idx,
            "total_chunks": total_chunks,
            # Create a unique ID for indexing lookup
            "chunk_id": f"{metadata.get('source')}_c{idx}"
        })
        chunked_documents.append(Document(text=text_chunk, metadata=metadata))
        
    return chunked_documents


def chunk_all_documents(documents: List[Document], chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[Document]:
    """
    Splits a list of Document objects into a larger list of smaller chunked Document objects.
    """
    logger.info(f"Chunking {len(documents)} cleaned documents...")
    all_chunks = []
    
    for doc in documents:
        chunks = chunk_document(doc, chunk_size, chunk_overlap)
        all_chunks.extend(chunks)
        
    logger.info(f"Generated {len(all_chunks)} chunks from {len(documents)} parent documents.")
    return all_chunks
