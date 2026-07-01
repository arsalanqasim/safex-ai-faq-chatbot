# System Architecture - SafeX AI Knowledge Assistant (RAG)

This document describes the design, architecture, and data flow of the Retrieval-Augmented Generation (RAG) assistant for SafeX Solutions.

---

## 1. Overall System Architecture

The SafeX AI Knowledge Assistant is split into two distinct operational environments:
1. **The Ingestion Pipeline (Offline/Batch)**: Loads, cleans, chunks, embeds, and saves document indexes into a file-based vector store.
2. **The Chatbot Runtime (Online/Interactive)**: Loads the saved index, accepts user questions, retrieves the most relevant content chunks, and queries Google's Gemini API to generate accurate answers.

```mermaid
graph TD
    %% Define Subgraphs for Clarity
    subgraph Ingestion_Pipeline ["Ingestion Pipeline (Runs Once)"]
        A[Raw Sources] --> B[load_documents.py]
        B --> C[clean.py]
        C --> D[chunk.py]
        D --> E[embeddings.py]
        E --> F[vector_store.py]
        F --> G[Vector Store Index File]
    end

    subgraph Chatbot_Runtime ["Chatbot Runtime (Interactive)"]
        H[Streamlit UI app.py] --> I[Chatbot Engine chatbot.py]
        G -.-> |Loads index on startup| I
        I --> J[Similarity Matcher]
        J --> K[LLM Orchestration Layer]
        K --> |System + User Prompt| L[Gemini API / Mock LLM]
        L --> |Generated Text| K
        K --> H
    end
    
    %% Style adjustments
    classDef pipeline fill:#e0f2fe,stroke:#0284c7,stroke-width:2px;
    classDef runtime fill:#f0fdf4,stroke:#16a34a,stroke-width:2px;
    class A,B,C,D,E,F,G pipeline;
    class H,I,J,K,L runtime;
```

---

## 2. Document Ingestion Pipeline Flow

The ingestion pipeline converts raw source files of multiple formats into mathematical vector embeddings, storing them alongside their textual content and metadata.

```mermaid
flowchart TD
    %% Ingestion Pipeline Flow
    SourceWeb[Web Pages HTML] --> Loader
    SourcePDF[PDF Documents] --> Loader
    SourceMD[Markdown Files] --> Loader
    SourceTXT[Plain Text Files] --> Loader
    SourceJSON[JSON FAQ Files] --> Loader

    Loader[load_documents.py] -->|Consolidated Documents| Clean["clean.py (Normalize text, strip HTML tags)"]
    Clean -->|Clean Text & Metadata| Chunk["chunk.py (Sliding character-window division)"]
    Chunk -->|Document Chunks| Embedder["embeddings.py (Gemini Embedding Client)"]
    Embedder -->|768-Dim Vectors| Indexer["vector_store.py (Compile Numpy Matrix)"]
    Indexer -->|Pickle Serialization| Storage[data/vector_store/vector_index.pkl]
```

---

## 3. Runtime Query Flow

When a user submits a question through the Streamlit web interface, the runtime performs real-time retrieval and generation to formulate an answer.

```mermaid
flowchart TD
    %% Runtime Query Pipeline Flow
    UserQuery([User inputs question in app.py]) --> EmbedQuery[Embed question using Gemini Embedding API]
    EmbedQuery --> FetchIndex[Load local vector_index.pkl]
    FetchIndex --> CosineSimilarity[Compute Cosine Similarity via Numpy]
    CosineSimilarity --> ScoreFilter{Is similarity >= threshold?}
    
    ScoreFilter -->|Yes| ExtractContext[Retrieve Top-K matching chunks and source URLs]
    ScoreFilter -->|No| FallbackContext[Supply 'No relevant context found' system instruction]
    
    ExtractContext --> FormulatePrompt[Synthesize RAG prompt template]
    FallbackContext --> FormulatePrompt
    
    FormulatePrompt --> SendLLM[Send prompt and system guidelines to Gemini LLM]
    SendLLM --> ParseResponse[LLM processes context and returns response or 'I do not know']
    ParseResponse --> RenderUI[Render answer, referenced sources, and latency on Streamlit]
```

---

## 4. End-to-End Data Flow Matrix

This flowchart maps how data flows from its raw ingestion format down to its representation in the user's interface.

```mermaid
sequenceDiagram
    autonumber
    actor Intern as Intern / Leader
    actor User as Web Client User
    participant Loader as load_documents.py
    participant DB as vector_index.pkl
    participant Engine as chatbot.py
    participant Gemini as Google Gemini API

    Note over Intern, DB: Ingestion Phase (Runs on Setup)
    Intern->>Loader: Place raw data files & run indexer
    Loader->>Loader: Read raw file -> Clean -> Split into chunks
    Loader->>Gemini: Request embeddings for chunks
    Gemini-->>Loader: Return text embeddings
    Loader->>DB: Save chunks, metadata, and embeddings array

    Note over User, Gemini: Runtime Query Phase (User Interactive)
    User->>Engine: Enter query "What is SafeX?"
    Engine->>DB: Load vector_index.pkl (Cached)
    Engine->>Gemini: Generate embedding for user query
    Gemini-->>Engine: Return query vector
    Engine->>Engine: Run numpy cosine similarity search
    Engine->>Gemini: Call LLM (System prompts + Context chunks + Query)
    Gemini-->>Engine: Generate final answer text
    Engine-->>User: Return answer text + Source references + Latency logs
```
