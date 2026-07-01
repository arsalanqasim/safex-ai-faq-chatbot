# ==============================================================================
# SafeX RAG Pipeline - Document Cleaning Utility
# ==============================================================================
import re
from src.pipeline.load_documents import Document
from src.config.settings import logger

def clean_html_boilerplate(text: str) -> str:
    """
    Cleans HTML tags, script blocks, styling tags, and normalizes spacing.
    """
    # 1. Remove style and script blocks
    text = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', text, flags=re.IGNORECASE)
    text = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', text, flags=re.IGNORECASE)
    
    # 2. Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    
    # 3. Clean up excessive whitespace and duplicate newlines
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    return text.strip()


def clean_markdown_boilerplate(text: str) -> str:
    """
    Strips out markdown table markup, excessive hashes, links, etc.
    """
    # Simply normalize whitespace for the first iteration (let interns expand on markdown cleaning)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()


def clean_document(doc: Document) -> Document:
    """
    Selects the cleaning strategy based on the document type and returns a cleaned Document.
    """
    doc_type = doc.metadata.get("type", "txt")
    raw_text = doc.text
    
    logger.debug(f"Cleaning document '{doc.metadata.get('source')}' of type '{doc_type}'")
    
    if doc_type == "html":
        cleaned_text = clean_html_boilerplate(raw_text)
    elif doc_type == "md":
        cleaned_text = clean_markdown_boilerplate(raw_text)
    else:
        # For txt, pdf, json_faq, perform basic space normalization
        cleaned_text = re.sub(r'[ \t]+', ' ', raw_text)
        cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text).strip()
        
    # Return a new Document instance with cleaned text
    return Document(text=cleaned_text, metadata=doc.metadata.copy())


def clean_all_documents(documents: list[Document]) -> list[Document]:
    """
    Iterates through a list of Document objects and cleans each one.
    """
    logger.info(f"Cleaning {len(documents)} loaded documents...")
    cleaned_docs = [clean_document(doc) for doc in documents]
    logger.info(f"Successfully cleaned {len(cleaned_docs)} documents.")
    return cleaned_docs
