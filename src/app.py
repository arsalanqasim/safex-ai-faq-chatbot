# ==============================================================================
# SafeX AI FAQ Chatbot - Streamlit Dashboard Interface
# ==============================================================================
import os
import sys
from pathlib import Path
import streamlit as st

# Ensure root directory is on python path for clean imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import FAQ_PATH, APP_TITLE, APP_SUBTITLE
from src.chatbot import FAQChatbot

# Configure Streamlit page layout and theme properties
st.set_page_config(
    page_title="SafeX FAQ Chatbot Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium styling for a cohesive dashboard look
st.markdown("""
<style>
    /* Gradient headers and brand consistency */
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #6B7280;
        margin-bottom: 1.5rem;
    }
    /* Metric Cards */
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    .metric-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #1E293B;
    }
    /* Chatbot response card */
    .response-card {
        background-color: #F1F5F9;
        border-left: 6px solid #2563EB;
        padding: 1.25rem;
        border-radius: 0.375rem;
        margin-bottom: 1.5rem;
    }
    .response-header {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .response-text {
        font-size: 1.1rem;
        color: #0F172A;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Session State & Model Initialization
# ------------------------------------------------------------------------------
if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = FAQChatbot(FAQ_PATH)
        st.session_state.kb_status = "Loaded Successfully"
    except Exception as e:
        st.session_state.chatbot = None
        st.session_state.kb_status = f"Initialization Error: {e}"

# ------------------------------------------------------------------------------
# Sidebar - Branding, Settings, Team & Task Distribution
# ------------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/shield.png", width=65)
    st.markdown("### SafeX Solutions")
    st.caption("Week 1 AI/ML Internship Prototype")
    st.divider()

    st.markdown("#### Model Settings")
    
    # Dynamic Similarity Threshold slider
    threshold_val = st.slider(
        "Similarity Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.35,
        step=0.05,
        help="Queries scoring below this threshold will return the fallback message."
    )
    
    st.divider()

    # Knowledge Base Status
    st.markdown("#### System Integrity")
    if st.session_state.chatbot is not None:
        st.success(f"FAQ KB: **{len(st.session_state.chatbot.faqs)} Items Loaded**")
    else:
        st.error(f"FAQ KB: **{st.session_state.kb_status}**")
        
    st.divider()

    # Internship Team & Task Distribution (Group 54)
    st.markdown("#### Team & Tasks Distribution")
    st.markdown("**Group Leader:**\n- **Arsalan Qasim** (Project Lead, Github/Release Mgr)")
    
    with st.expander("Cohort Members (7) & Modules", expanded=False):
        st.markdown("""
        - **Muhammad Wasim**
          *(Similarity matching model)*
        - **Muhammad Faozan Mujtaba**
          *(Knowledge base preparation)*
        - **Shahidullah**
          *(Streamlit dashboard UI)*
        - **Ali Ammar Haider**
          *(Backend integration & configs)*
        - **Abdul Haseeb**
          *(Unit tests / QA engineer)*
        - **Hammad Abbas**
          *(Evaluation runs & reporting)*
        - **Ali Zaib**
          *(Technical documentation)*
        """)
        
# ------------------------------------------------------------------------------
# Main Dashboard Panel
# ------------------------------------------------------------------------------
st.markdown(f'<div class="main-header">{APP_TITLE}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{APP_SUBTITLE} — Internal query verification dashboard.</div>', unsafe_allow_html=True)

# Layout: Form on top, details on bottom
if st.session_state.chatbot is None:
    st.error("Cannot run dashboard. The knowledge base is missing or corrupt. Check data/faq.json.")
else:
    # Query Form Section
    with st.container():
        st.subheader("Query the Knowledge Base")
        with st.form(key="query_form", clear_on_submit=False):
            col_in, col_btn = st.columns([5, 1])
            with col_in:
                user_input = st.text_input(
                    label="Enter your internal question about SafeX Solutions...",
                    placeholder="e.g., Who is the founder of SafeX Solutions?",
                    label_visibility="collapsed"
                )
            with col_btn:
                submit_button = st.form_submit_button(
                    label="🔍 Find Answer",
                    use_container_width=True
                )

    st.divider()

    # Process and display result
    if submit_button and user_input.strip():
        # Query Chatbot
        result = st.session_state.chatbot.query(user_input, threshold=threshold_val)
        
        # Display response
        st.subheader("Response Output")
        
        # Determine container styling based on fallback trigger
        if result["is_fallback"]:
            st.warning(result["answer"])
        else:
            st.markdown(f"""
            <div class="response-card">
                <div class="response-header">🛡️ VERIFIED FAQ RESPONSE</div>
                <div class="response-text">{result["answer"]}</div>
            </div>
            """, unsafe_allow_html=True)

        # Matched FAQ & Algorithmic Scores
        st.subheader("Algorithmic Matching Analysis")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Similarity Score</div>
                <div class="metric-value">{result["similarity_score"]:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Execution Latency</div>
                <div class="metric-value">{result["latency_seconds"]*1000:.2f} ms</div>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">KB Category</div>
                <div class="metric-value">{result["category"]}</div>
            </div>
            """, unsafe_allow_html=True)

        # Details expansion panel for debugging
        with st.expander("🔍 Show Similarity Matching Metadata", expanded=True):
            st.markdown(f"**User Query:** `{result['query']}`")
            st.markdown(f"**Best Matched FAQ Question:** `{result['matched_question']}`")
            st.markdown(f"**Configured Threshold:** `{threshold_val}`")
            st.markdown(f"**FAQ ID:** `{result['faq_id']}`")
            
            # Progress bar for score visualization
            st.markdown("**Similarity Visualizer:**")
            st.progress(result["similarity_score"])
            
    elif submit_button:
        st.info("Please enter a valid query to search the FAQ database.")

    # Side-panel / bottom panel: FAQ Reference List
    st.divider()
    with st.expander("📚 Browse Entire Knowledge Base FAQ List", expanded=False):
        for item in st.session_state.chatbot.faqs:
            st.markdown(f"**[{item['category']}] Q: {item['question']}**")
            st.markdown(f"A: {item['answer']}")
            st.divider()
