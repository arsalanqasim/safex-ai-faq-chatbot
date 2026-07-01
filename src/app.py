# ==============================================================================
# SafeX AI Knowledge Assistant - Streamlit Application Interface
# ==============================================================================
import os
import sys
from pathlib import Path
import streamlit as st

# Setup python path to import from 'src' correctly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config.settings import (
    VECTOR_STORE_DIR, 
    RAW_DATA_DIR, 
    GEMINI_API_KEY, 
    logger
)
from src.chatbot import RAGAssistant
from src.pipeline.vector_store import build_and_save_index

# Page Styling and Page Config
st.set_page_config(
    page_title="SafeX AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling for SafeX Branding
st.markdown("""
<style>
    /* Gradient headers and brand consistency */
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    /* Source chunk formatting */
    .source-card {
        background-color: #F3F4F6;
        border-left: 5px solid #3B82F6;
        padding: 1rem;
        border-radius: 0.375rem;
        margin-bottom: 1rem;
    }
    .source-meta {
        font-weight: 600;
        color: #1F2937;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .source-score {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 0.1rem 0.4rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# State Initialization
# ------------------------------------------------------------------------------
logger.info("Initializing Streamlit Application Session...")

# Path to the compiled vector index file
INDEX_FILE_PATH = VECTOR_STORE_DIR / "vector_index.pkl"

# Initialize RAG Assistant (cached in Streamlit session state)
if "rag_assistant" not in st.session_state:
    st.session_state.rag_assistant = RAGAssistant(INDEX_FILE_PATH, provider_type="gemini")

# Chat message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------------------------------------
# Sidebar - Brand, Settings & Team Details
# ------------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=70)
    st.markdown("### SafeX Solutions")
    st.markdown("AI/ML Internship Project")
    st.divider()
    
    # Credentials Status check
    st.markdown("#### System Configuration")
    if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
        st.success("API Credentials: **Gemini Connected**")
    else:
        st.warning("API Credentials: **Mock/Offline Mode**")
        st.caption("Please configure `GEMINI_API_KEY` in your `.env` to execute live API calls.")
        
    st.divider()

    # Re-indexing operations for Interns to refresh dataset
    st.markdown("#### Database Administration")
    if st.button("🔄 Build/Refresh Vector Index", use_container_width=True):
        with st.spinner("Processing documents, cleaning, and creating embeddings..."):
            try:
                logger.info("Triggering vector index rebuild from UI.")
                build_and_save_index(RAW_DATA_DIR, INDEX_FILE_PATH, provider_type="gemini")
                
                # Reload assistant with updated database
                st.session_state.rag_assistant = RAGAssistant(INDEX_FILE_PATH, provider_type="gemini")
                st.success("Vector Database refreshed successfully!")
            except Exception as e:
                logger.error(f"Failed to refresh index from UI: {e}")
                st.error(f"Error rebuilding index: {e}")
                
    st.caption("Runs ingestion pipeline (`load` -> `clean` -> `chunk` -> `embed` -> `index` -> `save`) on local raw data files.")
    
    st.divider()

    # Internship Team Metadata (Group 54)
    st.markdown("#### Group 54 Roster")
    st.markdown("**Group Leader:**\n- **Arsalan Qasim** (AI/ML Intern)")
    
    with st.expander("Team Members (7)", expanded=False):
        st.markdown("""
        - **MUHAMMAD WASIM**
          *(AI, Data Science, ML)*
        - **Muhammed Faizan Mujtaba**
          *(AI/ML)*
        - **Shahidullah**
          *(Web Dev, AI/ML)*
        - **Ali Ammar Haider**
          *(Data Analytics, BI)*
        - **Abdul Haseeb**
          *(AI/ML)*
        - **Hammad Abbas**
          *(Data Analysis, Data Science)*
        - **Ali Zaib**
          *(AI/ML)*
        """)

# ------------------------------------------------------------------------------
# Main Page Header
# ------------------------------------------------------------------------------
st.markdown('<div class="main-header">SafeX AI Knowledge Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">RAG-driven retrieval assistant answering questions using indexed internal documents.</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Conversation Feed
# ------------------------------------------------------------------------------
# Render existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        # If there are sources attached, render them
        if "sources" in message and message["sources"]:
            with st.expander("🔍 View References"):
                for idx, src in enumerate(message["sources"]):
                    st.markdown(f"""
                    <div class="source-card">
                        <div class="source-meta">
                            Reference #{idx+1}: <code>{src['source']}</code> ({src['type'].upper()}) 
                            <span class="source-score">Relevance: {src['score']:.2f}</span>
                        </div>
                        <div style="font-size:0.875rem; color:#374151;">
                            <i>"{src['text'].strip()}"</i>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Chat Input & RAG Execution
# ------------------------------------------------------------------------------
if user_query := st.chat_input("Ask a question about SafeX Solutions..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)
        
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base and formulating response..."):
            logger.info(f"Querying assistant from UI: {user_query}")
            try:
                response = st.session_state.rag_assistant.query(user_query)
                answer = response["answer"]
                sources = response["sources"]
                latency = response["latency"]
                
                # Write answer
                st.write(answer)
                
                # Render sources
                if sources:
                    with st.expander("🔍 View References"):
                        for idx, src in enumerate(sources):
                            st.markdown(f"""
                            <div class="source-card">
                                <div class="source-meta">
                                    Reference #{idx+1}: <code>{src['source']}</code> ({src['type'].upper()}) 
                                    <span class="source-score">Relevance: {src['score']:.2f}</span>
                                </div>
                                <div style="font-size:0.875rem; color:#374151;">
                                    <i>"{src['text'].strip()}"</i>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                    # Display response latency details in page sub-caption
                    st.caption(f"Latency: Retrieval **{latency['retrieval_seconds']:.3f}s** | Generation **{latency['generation_seconds']:.3f}s** | Total **{latency['total_seconds']:.3f}s**")
                else:
                    st.caption(f"Latency: Retrieval **{latency['retrieval_seconds']:.3f}s** | Generation **{latency['generation_seconds']:.3f}s** | Total **{latency['total_seconds']:.3f}s** (No references found)")

                # Save assistant message to state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": sources
                })
                
            except Exception as e:
                logger.error(f"UI query execution failed: {e}")
                err_msg = f"Sorry, an internal error occurred: {e}. Please check the system logs."
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})
