# safex-ai-faq-chatbot — System Architecture

This document outlines the system architecture and data-flow pipelines for the SafeX Semantic FAQ Chatbot. The design follows strict modular guidelines where each component carries exactly one responsibility.

---

## 1. Overall System Architecture

The system uses a classic decoupled Model-View-Controller (MVC) architectural design, where:
- **View:** The Streamlit dashboard (`app.py`) provides the interface for user input and visualizes similarity analytics.
- **Controller/Orchestrator:** The `FAQChatbot` class (`chatbot.py`) coordinates loading the database and dispatching similarity matching.
- **Model/Engine:** The similarity module (`similarity.py`) holds the TF-IDF and cosine similarity logic, utilizing `scikit-learn`.

```mermaid
graph TD
    User([User]) <-->|1. Input Query / View Results| StreamlitApp[Streamlit Dashboard: app.py]
    StreamlitApp <-->|2. Dispatches Query| FAQChatbot[Chatbot Orchestrator: chatbot.py]
    FAQChatbot -->|3. Loads JSON Data| KB[Knowledge Base Loader: knowledge_base.py]
    KB -->|Reads| JSON[(data/faq.json)]
    FAQChatbot <-->|4. Processes Text & Matches Vectors| SimilarityModel[Similarity Engine: similarity.py]
    SimilarityModel -->|Uses| Utils[Text Utilities: utils.py]
```

---

## 2. Knowledge Base Loading Flow

This sequence occurs once during the initialization of the chatbot, fitting the vectorizer on the verified FAQ dataset:

```mermaid
sequenceDiagram
    participant App as Streamlit app.py
    participant Bot as FAQChatbot (chatbot.py)
    participant KB as KB Loader (knowledge_base.py)
    participant Model as SimilarityModel (similarity.py)
    participant File as FAQ Dataset (data/faq.json)

    App->>Bot: Instantiate FAQChatbot(faq_path)
    Bot->>KB: load_faq_data(faq_path)
    KB->>File: Open & Parse JSON File
    File-->>KB: Raw JSON List
    KB->>KB: Validate Structure (check question/answer keys)
    KB-->>Bot: List of FAQ Dictionaries
    Bot->>Model: fit(questions)
    Model->>Model: fit_transform(questions) with TF-IDF Vectorizer
    Model-->>Bot: TF-IDF Vector Space fitted
    Bot-->>App: Chatbot Ready
```

---

## 3. Question Processing Pipeline

Every user query undergoes normalization before calculation to ensure matches are spelling-case and punctuation independent:

```mermaid
graph LR
    RawQuery["Raw User Query (e.g. 'Who founded SafeX?')"]
    --> Lowercase["1. Lowercase conversion ('who founded safex?')"]
    --> RemovePunctuation["2. Remove Punctuation & Special Chars ('who founded safex')"]
    --> NormalizeWhitespace["3. Collapse Whitespace ('who founded safex')"]
    --> CleanQuery["Normalized Query String"]
```

---

## 4. Similarity Matching Engine

The core similarity algorithm uses a local Vector Space Model. We compute the Cosine Similarity between the normalized user query vector and all FAQ question vectors:

```mermaid
graph TD
    CleanQuery[Normalized Query String] --> Vectorize[Transform to TF-IDF Query Vector]
    Vectorize --> SimilarityDot[Dot Product: Query Vector • FAQ Vectors]
    FittedMatrix[(Fitted FAQ TF-IDF Matrix)] --> SimilarityDot
    SimilarityDot --> CosineScore[Calculate Cosine Similarity Scores]
    CosineScore --> FindMax[Identify Highest Score and Index]
    FindMax --> MatchResult[Return: matched_index, similarity_score]
```

Cosine Similarity is calculated as:
$$\text{Similarity}(\mathbf{q}, \mathbf{d}) = \cos(\theta) = \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\| \|\mathbf{d}\|} = \frac{\sum_{i=1}^{n} q_i d_i}{\sqrt{\sum_{i=1}^{n} q_i^2} \sqrt{\sum_{i=1}^{n} d_i^2}}$$

---

## 5. Response Generation & Threshold Logic

Once a match is returned, the orchestrator evaluates whether the similarity score exceeds the configured minimum threshold before returning the answer:

```mermaid
graph TD
    MatchResult[Match Result: score & index] --> ThresholdCheck{Similarity Score >= Threshold?}
    ThresholdCheck -->|Yes| FetchAnswer[Retrieve Verified FAQ Answer]
    FetchAnswer --> ReturnResponse[Return FAQ Answer + Matched Question + Score]
    ThresholdCheck -->|No| FetchFallback[Retrieve Fallback Message]
    FetchFallback --> ReturnFallback[Return Fallback Message + Matched Question + Score]
    ReturnResponse --> RenderUI[Render Response Panel in Dashboard]
    ReturnFallback --> RenderUI
```
