# ==============================================================================
# SafeX RAG Pipeline - Source-Agnostic Document Loader
# ==============================================================================
import os
import json
from typing import List, Dict, Any
from pathlib import Path
from src.config.settings import logger

class Document:
    """
    Standardized internal representation of a document.
    """
    def __init__(self, text: str, metadata: Dict[str, Any]):
        self.text = text
        self.metadata = metadata  # e.g., {"source": "filename", "type": "pdf/html/md", "id": "unique-id"}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "metadata": self.metadata
        }

    def __repr__(self) -> str:
        return f"Document(type={self.metadata.get('type')}, source={self.metadata.get('source')}, chars={len(self.text)})"


def load_text_file(filepath: Path) -> List[Document]:
    """Loads plain text file."""
    logger.debug(f"Loading plain text file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    metadata = {
        "source": filepath.name,
        "type": "txt",
        "path": str(filepath)
    }
    return [Document(text=content, metadata=metadata)]


def load_markdown_file(filepath: Path) -> List[Document]:
    """Loads markdown file."""
    logger.debug(f"Loading markdown file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    metadata = {
        "source": filepath.name,
        "type": "md",
        "path": str(filepath)
    }
    return [Document(text=content, metadata=metadata)]


def load_html_file(filepath: Path) -> List[Document]:
    """Loads HTML file (extracted from website pages)."""
    logger.debug(f"Loading HTML file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    metadata = {
        "source": filepath.name,
        "type": "html",
        "path": str(filepath)
    }
    return [Document(text=content, metadata=metadata)]


def load_pdf_file(filepath: Path) -> List[Document]:
    """Loads PDF file. Interns can extend this using PyPDF, pdfplumber, or pypdf2."""
    logger.debug(f"Attempting to load PDF file: {filepath}")
    
    # Placeholder implementation
    # TODO (Intern Task): Install 'pypdf' and replace this code with actual PDF text extraction.
    # Example snippet:
    #   from pypdf import PdfReader
    #   reader = PdfReader(filepath)
    #   text = ""
    #   for page in reader.pages:
    #       text += page.extract_text() + "\n"
    
    fallback_text = f"[PDF PLURAL PLACEHOLDER] Content from {filepath.name}. Implement PDF extraction in load_documents.py."
    logger.warning(f"PDF extraction not implemented. Using fallback for {filepath.name}")
    
    metadata = {
        "source": filepath.name,
        "type": "pdf",
        "path": str(filepath)
    }
    return [Document(text=fallback_text, metadata=metadata)]


def load_json_faq_file(filepath: Path) -> List[Document]:
    """
    Loads JSON FAQ file.
    Expected format: 
    [
      {"question": "What is SafeX?", "answer": "SafeX is..."},
      {"question": "How to contact?", "answer": "Contact at..."}
    ]
    """
    logger.debug(f"Loading JSON FAQ file: {filepath}")
    documents = []
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if isinstance(data, list):
        for idx, item in enumerate(data):
            q = item.get("question", "")
            a = item.get("answer", "")
            combined_text = f"Question: {q}\nAnswer: {a}"
            
            metadata = {
                "source": filepath.name,
                "type": "json_faq",
                "item_index": idx,
                "path": str(filepath)
            }
            documents.append(Document(text=combined_text, metadata=metadata))
    else:
        logger.error(f"Invalid JSON FAQ format in {filepath.name}. Expected a list of QA dicts.")
        
    return documents


def load_all_documents(directory: Path) -> List[Document]:
    """
    Scans the raw data directory, detects file types, loads content,
    and returns a consolidated list of standardized Document objects.
    """
    logger.info(f"Scanning directory for raw documents: {directory}")
    documents = []
    
    if not directory.exists():
        logger.error(f"Directory does not exist: {directory}")
        return []
        
    for filename in os.listdir(directory):
        filepath = directory / filename
        if filepath.is_dir():
            continue
            
        suffix = filepath.suffix.lower()
        try:
            if suffix == ".txt":
                documents.extend(load_text_file(filepath))
            elif suffix == ".md":
                documents.extend(load_markdown_file(filepath))
            elif suffix in [".html", ".htm"]:
                documents.extend(load_html_file(filepath))
            elif suffix == ".pdf":
                documents.extend(load_pdf_file(filepath))
            elif suffix == ".json":
                documents.extend(load_json_faq_file(filepath))
            else:
                logger.warning(f"Unsupported file type '{suffix}' for {filename}. Skipping.")
        except Exception as e:
            logger.error(f"Failed to load document {filename}: {e}")
            
    logger.info(f"Successfully loaded {len(documents)} document entries from {directory}")
    return documents
