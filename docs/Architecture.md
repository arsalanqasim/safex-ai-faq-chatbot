# Technical Architecture & Design Decisions - SafeX RAG

This document details the software engineering design decisions made during the construction of the SafeX AI Knowledge Assistant (RAG) boilerplate.

---

## 1. Key Architectural Decisions

### A. Source-Agnostic Document Loader (`load_documents.py`)
- **Problem**: Document indexing is often coupled with specific scrapers or parsing structures. If the team switches from text files to website scrapes or PDFs, the entire backend usually breaks.
- **Solution**: We implemented a unified `Document` abstraction. The loading module reads diverse formats (HTML, PDF, MD, TXT, JSON) and converts them into standardized `Document` objects containing `text` and `metadata` dictionary fields.
- **Result**: The cleaning, chunking, and embedding stages remain identical regardless of the input data source. Interns can add support for extra formats (e.g., DOCX, SQL databases) by simply adding a loading function in `load_documents.py`.

### B. Dependency-Free Vector Database (`vector_store.py`)
- **Problem**: Popular vector databases like ChromaDB or FAISS can be challenging to install on Windows machines due to C++ compilation dependencies (e.g., Microsoft Visual C++ Build Tools). This creates friction for interns during onboarding.
- **Solution**: We built a lightweight custom vector store using standard `numpy` array operations for Cosine Similarity:
  $$\text{Similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$
  The database is saved to disk as a serialized binary file using Python's native `pickle` module.
- **Result**: Zero installation issues. The code runs out-of-the-box on any OS with `numpy` installed. If the project scales, the vector store interface is structured so they can replace the similarity search with ChromaDB or FAISS with minimal modifications.

### C. Swappable Provider Interfaces (`embeddings.py` & `chatbot.py`)
- **Problem**: Being locked into a single API provider (like Google Gemini) risks downtime or breaking changes. However, implementing heavy frameworks like LangChain adds unnecessary complexity.
- **Solution**: We created thin abstract base classes (`EmbeddingProvider` and `LLMProvider`) and factory functions. By default, the app uses Google's Gemini SDK.
- **Result**:
  1. Interns can easily write a new subclass (e.g., `OpenAILLMProvider` or `HuggingFaceEmbeddingProvider`) and swap it in the configurations.
  2. The project includes a `MockEmbeddingProvider` and `MockLLMProvider` that generate dummy values. This allows the team to work on the UI, cleaning, and formatting pipelines completely offline without an API key.

---

## 2. RAG Logic Flow

```text
       [ User Query ]
             │
             ▼
     ┌───────────────┐
     │ Query Embed   │  ◄── (embeddings.py: Gemini/Mock embedding API)
     └───────┬───────┘
             │ Vector
             ▼
     ┌───────────────┐
     │ Cosine Search │  ◄── (vector_store.py: numpy matrix math)
     └───────┬───────┘
             │ Top-K Chunks
             ▼
     ┌───────────────┐
     │ Prompt Synthes│  ◄── (config/prompts.py: system restrictions)
     └───────┬───────┘
             │ Prompt
             ▼
     ┌───────────────┐
     │ LLM Generation│  ◄── (chatbot.py: Gemini LLM query)
     └───────┬───────┘
             │ Response
             ▼
      [ User Answer ]
```

---

## 3. Preventative Guardrails (Hallucination Control)
To make the chatbot production-inspired, it must not hallucinate answers if data is missing. We enforce this through two distinct layers:
1. **System Prompt Guardrails**: The system instructions in `src/config/prompts.py` explicitly instruct the model to only use the context provided and reply with:
   > *"I am sorry, but I do not have information to answer that question based on my current knowledge base."*
   if the facts are missing from the context.
2. **Relevance Threshold**: Chunks retrieved with cosine similarity scores below `RETRIEVAL_THRESHOLD` (defined in `settings.py`) are filtered out. If no chunks exceed this threshold, the system passes an empty context flag, forcing the LLM to output the "I do not know" response.
