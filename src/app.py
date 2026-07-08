# ==============================================================================
# SafeX AI Knowledge Assistant
# Premium ChatGPT / Claude / Copilot-style Frontend
# ------------------------------------------------------------------------------
# Tech Stack : Python + Streamlit (frontend only)
# Backend    : Placeholder — to be replaced with chatbot.py -> FAQChatbot
# Author     : Frontend Engineering Team
# ==============================================================================

import os
import sys

# Ensure the project root directory is in the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import uuid
from datetime import datetime

import streamlit as st

from src.chatbot import FAQChatbot
from src.config import FAQ_PATH


# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="SafeX AI Knowledge Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================================
# 2. BACKEND PLACEHOLDER
# ------------------------------------------------------------------------------
# This is the ONLY function that talks to the "backend". Replace its body with
# the real implementation later:
#
#   from chatbot import FAQChatbot
#   bot = FAQChatbot()
#
#   def get_chatbot_response(query, threshold):
#       return bot.ask(query, threshold)
#
# Nothing else in this file needs to change.
# ==============================================================================

@st.cache_resource
def get_chatbot_instance() -> FAQChatbot:
    """Load and train the chatbot orchestrator exactly once using Streamlit caching."""
    return FAQChatbot(FAQ_PATH)

def get_chatbot_response(query: str, threshold: float) -> str:
    """
    Queries the actual backend similarity-based FAQ chatbot orchestrator.

    Args:
        query (str): The user's question.
        threshold (float): Similarity threshold from the sidebar slider.

    Returns:
        str: The chatbot's answer based on local knowledge retrieval.
    """
    bot = get_chatbot_instance()
    response = bot.query(query, threshold)
    return response["answer"]


# ==============================================================================
# 3. SESSION STATE INITIALIZATION
# ==============================================================================

def init_session_state() -> None:
    """Initialize all required keys in st.session_state exactly once."""

    if "chats" not in st.session_state:
        first_id = str(uuid.uuid4())
        st.session_state.chats = {
            first_id: {
                "title": "New Conversation",
                "messages": [],
                "created_at": datetime.now(),
            }
        }
        st.session_state.current_chat_id = first_id

    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = next(iter(st.session_state.chats))

    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"

    if "threshold" not in st.session_state:
        st.session_state.threshold = 0.30

    if "search_term" not in st.session_state:
        st.session_state.search_term = ""

    if "renaming_chat_id" not in st.session_state:
        st.session_state.renaming_chat_id = None

    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None


# ==============================================================================
# 4. CHAT MANAGEMENT HELPERS
# ==============================================================================

def get_current_chat() -> dict:
    """Return the dict for the currently active chat."""
    return st.session_state.chats[st.session_state.current_chat_id]


def create_new_chat() -> None:
    """Create a fresh, empty chat and make it the active one."""
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {
        "title": "New Conversation",
        "messages": [],
        "created_at": datetime.now(),
    }
    st.session_state.current_chat_id = new_id
    st.session_state.renaming_chat_id = None


def switch_chat(chat_id: str) -> None:
    """Switch the active chat pointer."""
    st.session_state.current_chat_id = chat_id
    st.session_state.renaming_chat_id = None


def delete_chat(chat_id: str) -> None:
    """Delete a chat. Ensures at least one chat always exists."""
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]

    if not st.session_state.chats:
        create_new_chat()
        return

    if st.session_state.current_chat_id == chat_id:
        st.session_state.current_chat_id = next(iter(st.session_state.chats))


def start_rename(chat_id: str) -> None:
    """Put a given chat into rename mode."""
    st.session_state.renaming_chat_id = chat_id


def confirm_rename(chat_id: str, new_title: str) -> None:
    """Persist a new title for a chat and exit rename mode."""
    clean_title = new_title.strip()
    if clean_title:
        st.session_state.chats[chat_id]["title"] = clean_title[:40]
    st.session_state.renaming_chat_id = None


def auto_title_from_first_message(chat_id: str, text: str) -> None:
    """Auto-generate a chat title from the first user message."""
    chat = st.session_state.chats[chat_id]
    if chat["title"] == "New Conversation":
        title = text.strip()
        chat["title"] = (title[:32] + "…") if len(title) > 32 else title


def filter_chats(search_term: str) -> list:
    """
    Return chat ids sorted by most-recent first, optionally filtered by a
    case-insensitive substring match on the chat title.
    """
    items = list(st.session_state.chats.items())
    items.sort(key=lambda kv: kv[1]["created_at"], reverse=True)

    if search_term.strip():
        term = search_term.strip().lower()
        items = [(cid, c) for cid, c in items if term in c["title"].lower()]

    return items


# ==============================================================================
# 5. CSS — PREMIUM SAAS THEME (DARK / LIGHT)
# ==============================================================================

def inject_css(theme: str) -> None:
    """Inject the full custom CSS for the selected theme."""

    if theme == "Dark":
        vars_css = """
        --bg-app:#0D1117;
        --bg-app-2:#161B22;
        --bg-sidebar:#010409;
        --bg-sidebar-hover:#161B22;
        --bg-sidebar-active:rgba(56,139,253,0.12);
        --border-soft:#21262D;
        --border-strong:#30363D;
        --text-primary:#E6EDF3;
        --text-secondary:#8B949E;
        --text-muted:#484F58;
        --bubble-user-bg:#1F6FEB;
        --bubble-user-text:#FFFFFF;
        --bubble-bot-bg:#161B22;
        --bubble-bot-border:#21262D;
        --bubble-bot-text:#E6EDF3;
        --accent:#388BFD;
        --accent-hover:#1F6FEB;
        --accent-soft:rgba(56,139,253,0.1);
        --card-bg:#161B22;
        --card-border:#21262D;
        --success:#3FB950;
        --warning:#D29922;
        --error:#F85149;
        --shadow-soft:0 8px 32px rgba(1,4,9,0.6);
        --shadow-card:0 2px 8px rgba(1,4,9,0.5);
        --shadow-btn:0 4px 14px rgba(31,111,235,0.4);
        --glass-bg:rgba(1,4,9,0.85);
        --scrollbar-thumb:#21262D;
        """
    else:
        vars_css = """
        --bg-app:#FFFFFF;
        --bg-app-2:#F6F8FA;
        --bg-sidebar:#F6F8FA;
        --bg-sidebar-hover:#EAEEF2;
        --bg-sidebar-active:rgba(9,105,218,0.08);
        --border-soft:#D0D7DE;
        --border-strong:#BCC0C5;
        --text-primary:#1F2328;
        --text-secondary:#656D76;
        --text-muted:#9198A1;
        --bubble-user-bg:#0969DA;
        --bubble-user-text:#FFFFFF;
        --bubble-bot-bg:#F6F8FA;
        --bubble-bot-border:#D0D7DE;
        --bubble-bot-text:#1F2328;
        --accent:#0969DA;
        --accent-hover:#0860CA;
        --accent-soft:rgba(9,105,218,0.08);
        --card-bg:#FFFFFF;
        --card-border:#D0D7DE;
        --success:#1A7F37;
        --warning:#9A6700;
        --error:#CF222E;
        --shadow-soft:0 4px 16px rgba(31,35,40,0.08);
        --shadow-card:0 1px 4px rgba(31,35,40,0.06);
        --shadow-btn:0 4px 12px rgba(9,105,218,0.2);
        --glass-bg:rgba(255,255,255,0.9);
        --scrollbar-thumb:#D0D7DE;
        """

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,300;0,14..32,400;0,14..32,500;0,14..32,600;0,14..32,700&display=swap');

        :root {{
            {vars_css}
        }}

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            -webkit-font-smoothing: antialiased;
        }}

        /* ---------- Hide default Streamlit chrome ---------- */
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        div[data-testid="stDecoration"] {{ display: none; }}
        div[data-testid="stStatusWidget"] {{ display: none; }}

        header[data-testid="stHeader"] {{
            background: transparent;
            box-shadow: none;
            height: 2.5rem;
        }}
        .stDeployButton,
        div[data-testid="stAppDeployButton"],
        [data-testid="stToolbarActions"] {{
            display: none !important;
        }}

        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"] {{
            visibility: visible !important;
            display: flex !important;
            opacity: 1 !important;
        }}
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="stSidebarCollapseButton"] svg path,
        [data-testid="collapsedControl"] svg,
        [data-testid="collapsedControl"] svg path,
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="stSidebarCollapsedControl"] svg path,
        [data-testid="stSidebarCollapseButton"] button,
        [data-testid="collapsedControl"] button,
        [data-testid="stSidebarCollapsedControl"] button,
        header[data-testid="stHeader"] svg,
        header[data-testid="stHeader"] svg path,
        header[data-testid="stHeader"] button svg,
        button[aria-label*="sidebar" i] svg,
        button[aria-label*="sidebar" i] svg path,
        button[title*="sidebar" i] svg,
        [data-testid*="Sidebar" i] svg,
        [data-testid*="Sidebar" i] svg path {{
            color: var(--text-primary) !important;
            fill: var(--text-primary) !important;
            stroke: var(--text-primary) !important;
            opacity: 1 !important;
        }}
        [data-testid="stSidebarCollapseButton"] button:hover svg,
        [data-testid="collapsedControl"] button:hover svg,
        [data-testid="stSidebarCollapsedControl"] button:hover svg,
        header[data-testid="stHeader"] button:hover svg {{
            color: var(--accent) !important;
            fill: var(--accent) !important;
            stroke: var(--accent) !important;
        }}
        header[data-testid="stHeader"] *,
        [data-testid="stSidebarCollapseButton"] *,
        [data-testid="collapsedControl"] *,
        [data-testid="stSidebarCollapsedControl"] * {{
            color: var(--text-primary) !important;
        }}

        section[data-testid="stSidebar"][aria-expanded="true"] {{
            min-width: 260px !important;
            max-width: 280px !important;
        }}
        section[data-testid="stSidebar"] {{
            transition: min-width 0.2s ease, max-width 0.2s ease;
        }}

        .stApp {{
            background: var(--bg-app);
        }}

        .stButton button,
        button[kind="secondary"],
        button[kind="primary"],
        div[data-testid="stPopover"] button {{
            background: var(--card-bg) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-soft) !important;
        }}
        .stButton button p, .stButton button span, .stButton button div {{
            color: inherit !important;
        }}

        div[data-testid="stBottom"],
        div[data-testid="stBottomBlockContainer"] {{
            background: var(--bg-app) !important;
        }}

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        .main {{
            background: var(--bg-app) !important;
        }}
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        label, p, span {{
            color: var(--text-primary);
        }}
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p,
        .stCaption {{
            color: var(--text-muted) !important;
        }}

        input[type="text"], textarea {{
            background: var(--card-bg) !important;
            color: var(--text-primary) !important;
            border-color: var(--border-soft) !important;
            caret-color: var(--accent) !important;
        }}
        input[type="text"]::placeholder, textarea::placeholder {{
            color: var(--text-muted) !important;
            opacity: 1 !important;
        }}

        /* Expanders */
        div[data-testid="stExpander"] {{
            background: var(--card-bg) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 8px !important;
            box-shadow: none;
        }}
        div[data-testid="stExpander"] summary,
        div[data-testid="stExpander"] details,
        div[data-testid="stExpander"] > details > summary {{
            background: var(--card-bg) !important;
            color: var(--text-primary) !important;
            border-radius: 8px !important;
        }}
        div[data-testid="stExpander"] summary:hover {{
            color: var(--accent) !important;
        }}
        div[data-testid="stExpander"] summary p,
        div[data-testid="stExpander"] summary span {{
            color: var(--text-primary) !important;
        }}
        div[data-testid="stExpander"] svg {{
            fill: var(--text-secondary) !important;
        }}
        div[data-testid="stExpanderDetails"] {{
            background: var(--card-bg) !important;
            color: var(--text-secondary) !important;
        }}
        div[data-testid="stExpanderDetails"] p,
        div[data-testid="stExpanderDetails"] li {{
            color: var(--text-secondary) !important;
        }}

        /* Slider */
        .stSlider [data-baseweb="slider"] > div {{
            background: var(--border-strong) !important;
        }}
        .stSlider [data-baseweb="slider"] div[role="slider"] {{
            background: var(--accent) !important;
            border-color: var(--accent) !important;
        }}
        .stSlider [data-testid="stTickBar"],
        .stSlider [data-testid="stTickBarMin"],
        .stSlider [data-testid="stTickBarMax"] {{
            color: var(--text-muted) !important;
        }}
        .stSlider div[data-baseweb="slider"] + div {{
            color: var(--text-primary) !important;
        }}

        /* Radio buttons */
        .stRadio label, .stRadio p, .stRadio span {{
            color: var(--text-secondary) !important;
        }}
        div[data-baseweb="radio"] div:first-child {{
            border-color: var(--border-strong) !important;
        }}
        div[data-baseweb="radio"] div[aria-checked="true"] div:first-child {{
            border-color: var(--accent) !important;
        }}
        div[data-baseweb="radio"] div[aria-checked="true"] div:first-child div {{
            background: var(--accent) !important;
        }}

        /* Tooltips */
        div[data-baseweb="tooltip"] {{
            background: var(--card-bg) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-soft) !important;
        }}

        /* Scrollbars */
        ::-webkit-scrollbar {{ width: 4px; height: 4px; }}
        ::-webkit-scrollbar-thumb {{
            background: var(--scrollbar-thumb);
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-track {{ background: transparent; }}

        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 6.5rem;
            max-width: 820px;
        }}

        /* ==========================================================
           SIDEBAR — Minimal GitHub-inspired
        ========================================================== */
        section[data-testid="stSidebar"] {{
            background: var(--bg-sidebar);
            border-right: 1px solid var(--border-soft);
        }}
        section[data-testid="stSidebar"] .block-container {{
            padding: 1rem 0.85rem 1rem 0.85rem;
        }}

        .brand-wrap {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 4px 2px 16px 2px;
            border-bottom: 1px solid var(--border-soft);
            margin-bottom: 16px;
        }}
        .brand-icon {{
            width: 32px; height: 32px;
            border-radius: 8px;
            background: var(--accent);
            display: flex; align-items: center; justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
        }}
        .brand-text-title {{
            color: var(--text-primary);
            font-weight: 600;
            font-size: 14px;
            line-height: 1.2;
            letter-spacing: -0.01em;
        }}
        .brand-text-sub {{
            color: var(--text-muted);
            font-size: 11px;
            font-weight: 400;
            margin-top: 1px;
        }}

        .sidebar-section-label {{
            color: var(--text-muted);
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 20px 2px 8px 2px;
        }}

        /* New Chat button */
        .new-chat-btn button {{
            background: var(--accent) !important;
            color: #fff !important;
            font-weight: 500 !important;
            font-size: 13px !important;
            border: none !important;
            border-radius: 6px !important;
            padding: 0.5rem 0.8rem !important;
            box-shadow: none !important;
            transition: opacity 0.15s ease !important;
        }}
        .new-chat-btn button:hover {{
            opacity: 0.88 !important;
        }}

        /* Search input */
        section[data-testid="stSidebar"] input[type="text"] {{
            background: var(--bg-app) !important;
            border: 1px solid var(--border-soft) !important;
            color: var(--text-primary) !important;
            border-radius: 6px !important;
            font-size: 12.5px !important;
            transition: border-color 0.15s ease !important;
        }}
        section[data-testid="stSidebar"] input[type="text"]:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 2px var(--accent-soft) !important;
        }}

        /* Chat history rows */
        .chat-row {{
            display: flex;
            align-items: center;
            gap: 2px;
            margin-bottom: 2px;
            border-radius: 6px;
        }}
        section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {{
            align-items: center !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="column"] {{
            display: flex !important;
            align-items: center !important;
        }}
        section[data-testid="stSidebar"] .stButton button {{
            background: transparent !important;
            border: 1px solid transparent !important;
            color: var(--text-secondary) !important;
            text-align: left;
            border-radius: 6px;
            font-size: 12.5px;
            font-weight: 400;
            padding: 6px 8px;
            transition: background-color 0.12s ease, color 0.12s ease;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        section[data-testid="stSidebar"] .stButton button:hover {{
            background: var(--bg-sidebar-hover) !important;
            color: var(--text-primary) !important;
        }}
        .chat-row.active .stButton button {{
            background: var(--bg-sidebar-active) !important;
            color: var(--accent) !important;
            font-weight: 500 !important;
        }}

        /* Three-dot context menu */
        .menu-trigger {{
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100%;
        }}
        .menu-trigger div[data-testid="stPopover"] {{
            display: flex;
            justify-content: center;
            width: 100%;
        }}
        .menu-trigger div[data-testid="stPopover"] button {{
            background: transparent !important;
            border: 1px solid transparent !important;
            color: var(--text-muted) !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            width: 24px !important;
            height: 24px !important;
            min-width: 24px !important;
            padding: 0 !important;
            margin: 0 auto !important;
            border-radius: 4px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            line-height: 1 !important;
            transition: all 0.15s ease !important;
        }}
        .menu-trigger div[data-testid="stPopover"] button:hover {{
            color: var(--text-primary) !important;
            background: var(--bg-sidebar-hover) !important;
        }}

        div[data-baseweb="popover"] {{
            z-index: 999999 !important;
        }}
        div[data-baseweb="popover"] [data-testid="stPopoverBody"],
        div[data-baseweb="popover"] > div > div {{
            background: var(--card-bg) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 8px !important;
            box-shadow: var(--shadow-soft) !important;
            padding: 4px !important;
            min-width: 160px !important;
            overflow: visible !important;
        }}
        div[data-testid="stPopoverBody"] .stButton button,
        [data-testid="stPopoverBody"] .stButton button {{
            background: transparent !important;
            border: none !important;
            color: var(--text-primary) !important;
            text-align: left !important;
            font-size: 13px !important;
            font-weight: 400 !important;
            padding: 7px 10px !important;
            border-radius: 6px !important;
            width: 100% !important;
            transition: background-color 0.12s ease !important;
        }}
        div[data-testid="stPopoverBody"] .stButton button:hover,
        [data-testid="stPopoverBody"] .stButton button:hover {{
            background: var(--bg-sidebar-hover) !important;
        }}
        .popover-danger .stButton button:hover {{
            background: rgba(248,81,73,0.08) !important;
            color: var(--error) !important;
        }}

        /* Settings expander */
        section[data-testid="stSidebar"] details {{
            background: transparent;
            border: 1px solid var(--border-soft);
            border-radius: 6px;
            margin-bottom: 8px;
        }}
        section[data-testid="stSidebar"] summary {{
            color: var(--text-secondary) !important;
            font-size: 12.5px !important;
            font-weight: 500 !important;
            padding: 4px 2px;
        }}
        section[data-testid="stSidebar"] label {{
            color: var(--text-secondary) !important;
            font-size: 12px !important;
        }}

        /* Footer inside sidebar */
        .sidebar-footer {{
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid var(--border-soft);
            color: var(--text-muted);
            font-size: 10.5px;
            text-align: center;
        }}

        /* ==========================================================
           HERO SECTION — Clean, minimal
        ========================================================== */
        .hero-wrap {{
            text-align: center;
            padding: 32px 10px 28px 10px;
        }}
        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--accent-soft);
            color: var(--accent);
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            padding: 4px 12px;
            border-radius: 999px;
            margin-bottom: 18px;
            border: 1px solid var(--accent-soft);
        }}
        .hero-title {{
            font-size: 32px;
            font-weight: 600;
            letter-spacing: -0.025em;
            line-height: 1.2;
            color: var(--text-primary);
            margin-bottom: 10px;
        }}
        .hero-subtitle {{
            font-size: 14px;
            color: var(--text-secondary);
            max-width: 480px;
            margin: 0 auto;
            line-height: 1.65;
            font-weight: 400;
        }}

        /* ==========================================================
           SUGGESTED PROMPT CARDS
        ========================================================== */
        .suggested-label {{
            color: var(--text-muted);
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 8px 2px 12px 2px;
        }}
        div[data-testid="column"] .stButton button {{
            background: var(--card-bg) !important;
            border: 1px solid var(--card-border) !important;
            color: var(--text-primary) !important;
            border-radius: 8px !important;
            text-align: left;
            padding: 12px 14px;
            font-size: 13px;
            font-weight: 400;
            width: 100%;
            min-height: 64px;
            box-shadow: none;
            transition: border-color 0.15s ease, background 0.15s ease;
        }}
        div[data-testid="column"] .stButton button:hover {{
            border-color: var(--accent) !important;
            background: var(--bg-app-2) !important;
        }}
        div[data-testid="column"] .stButton button p {{
            color: var(--text-primary) !important;
        }}

        /* ==========================================================
           EMPTY STATE
        ========================================================== */
        .empty-state {{
            text-align: center;
            padding: 28px 20px 10px 20px;
            color: var(--text-muted);
        }}
        .empty-state .icon-circle {{
            width: 44px; height: 44px;
            border-radius: 10px;
            margin: 0 auto 14px auto;
            background: var(--card-bg);
            border: 1px solid var(--border-soft);
            display: flex; align-items: center; justify-content: center;
            font-size: 20px;
        }}
        .empty-state p {{ font-size: 13px; color: var(--text-muted); margin: 0; }}

        /* ==========================================================
           CHAT MESSAGES
        ========================================================== */
        div[data-testid="stChatMessage"] {{
            background: transparent;
            padding: 8px 2px;
            margin-bottom: 2px;
            animation: msgIn 0.2s ease;
        }}

        @keyframes msgIn {{
            from {{ opacity: 0; transform: translateY(4px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}

        /* User message bubble */
        div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {{
            justify-content: flex-end;
        }}
        div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) .stMarkdown {{
            background: var(--bubble-user-bg);
            color: var(--bubble-user-text);
            padding: 10px 16px;
            border-radius: 12px 12px 2px 12px;
            max-width: 600px;
            font-size: 14px;
            line-height: 1.6;
        }}

        /* Assistant message bubble */
        div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) .stMarkdown {{
            background: var(--bubble-bot-bg);
            border: 1px solid var(--bubble-bot-border);
            color: var(--bubble-bot-text);
            padding: 12px 16px;
            border-radius: 12px 12px 12px 2px;
            max-width: 620px;
            font-size: 14px;
            line-height: 1.65;
        }}

        div[data-testid="chatAvatarIcon-user"] {{
            background: var(--accent) !important;
            border-radius: 6px !important;
        }}
        div[data-testid="chatAvatarIcon-assistant"] {{
            background: var(--card-bg) !important;
            border: 1px solid var(--border-soft) !important;
            border-radius: 6px !important;
        }}

        /* Typing indicator dots */
        .typing-dots span {{
            display: inline-block;
            width: 5px; height: 5px;
            margin-right: 3px;
            background: var(--text-muted);
            border-radius: 50%;
            animation: blink 1.2s infinite ease-in-out both;
        }}
        .typing-dots span:nth-child(1) {{ animation-delay: -0.24s; }}
        .typing-dots span:nth-child(2) {{ animation-delay: -0.12s; }}
        @keyframes blink {{
            0%, 80%, 100% {{ opacity: 0.2; transform: scale(0.8); }}
            40% {{ opacity: 1; transform: scale(1); }}
        }}

        /* ==========================================================
           CHAT INPUT
        ========================================================== */
        div[data-testid="stChatInput"] {{
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-top: 1px solid var(--border-soft);
            padding: 12px 0 8px 0;
        }}
        div[data-testid="stChatInput"] textarea {{
            background: var(--card-bg) !important;
            border: 1px solid var(--border-soft) !important;
            color: var(--text-primary) !important;
            border-radius: 8px !important;
            font-size: 14px !important;
            transition: border-color 0.15s ease !important;
        }}
        div[data-testid="stChatInput"] textarea:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 2px var(--accent-soft) !important;
        }}
        div[data-testid="stChatInput"] button {{
            background: var(--accent) !important;
            border-radius: 6px !important;
            transition: opacity 0.15s ease !important;
        }}
        div[data-testid="stChatInput"] button:hover {{
            opacity: 0.85 !important;
        }}

        div[data-testid="stBottom"] {{
            bottom: 28px !important;
        }}

        .pinned-footer {{
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 999999;
            text-align: center;
            font-size: 10.5px;
            color: var(--text-muted);
            background: var(--bg-app);
            padding: 5px 0;
            border-top: 1px solid var(--border-soft);
        }}

        hr {{ border-color: var(--border-soft); }}
        .stSlider [data-baseweb="slider"] {{ padding-top: 4px; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 6. SIDEBAR RENDERING
# ==============================================================================

def render_sidebar() -> None:
    """Render the full ChatGPT-style sidebar: brand, new chat, search,
    conversation history (with a three-dot rename/delete menu), settings,
    and about/footer."""

    with st.sidebar:

        # ---- Brand header -------------------------------------------------
        st.markdown(
            """
            <div class="brand-wrap">
                <div class="brand-icon">🛡️</div>
                <div>
                    <div class="brand-text-title">SafeX AI</div>
                    <div class="brand-text-sub">Knowledge Assistant</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---- New Chat -------------------------------------------------------
        st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
        if st.button("➕  New Chat", use_container_width=True, key="btn_new_chat"):
            create_new_chat()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # ---- Search chats -----------------------------------------------
        st.markdown('<div class="sidebar-section-label">Search</div>', unsafe_allow_html=True)
        st.session_state.search_term = st.text_input(
            "Search chats",
            value=st.session_state.search_term,
            placeholder="🔍  Search conversations...",
            label_visibility="collapsed",
            key="search_input",
        )

        # ---- Conversation history -----------------------------------------
        st.markdown('<div class="sidebar-section-label">Conversations</div>', unsafe_allow_html=True)

        visible_chats = filter_chats(st.session_state.search_term)

        if not visible_chats:
            st.caption("No conversations found.")

        for chat_id, chat in visible_chats:
            is_active = chat_id == st.session_state.current_chat_id
            row_class = "chat-row active" if is_active else "chat-row"

            if st.session_state.renaming_chat_id == chat_id:
                # ---- Inline rename mode ----
                st.markdown(f'<div class="{row_class} rename-mode">', unsafe_allow_html=True)
                new_title = st.text_input(
                    "Rename",
                    value=chat["title"],
                    key=f"rename_input_{chat_id}",
                    label_visibility="collapsed",
                )
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.markdown('<div class="rename-action save">', unsafe_allow_html=True)
                    if st.button("✓ Save", key=f"save_{chat_id}", use_container_width=True):
                        confirm_rename(chat_id, new_title)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown('<div class="rename-action cancel">', unsafe_allow_html=True)
                    if st.button("✕ Cancel", key=f"cancel_{chat_id}", use_container_width=True):
                        st.session_state.renaming_chat_id = None
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="{row_class}">', unsafe_allow_html=True)
                col_title, col_menu = st.columns([7, 1])

                with col_title:
                    icon = "💬" if not is_active else "🟢"
                    if st.button(
                        f"{icon}  {chat['title']}",
                        key=f"select_{chat_id}",
                        use_container_width=True,
                    ):
                        switch_chat(chat_id)
                        st.rerun()

                with col_menu:
                    # ---- Three-dot context menu (native popover) ----
                    # st.popover renders a floating panel anchored to the
                    # trigger button and handled by Streamlit itself, so
                    # positioning, clipping, and z-index are all correct
                    # out of the box - no custom dropdown hacks needed.
                    st.markdown('<div class="menu-trigger">', unsafe_allow_html=True)
                    with st.popover("⋮", use_container_width=False):
                        if st.button(
                            "✏️  Rename Chat",
                            key=f"rename_{chat_id}",
                            use_container_width=True,
                        ):
                            start_rename(chat_id)
                            st.rerun()

                        st.markdown('<div class="popover-danger">', unsafe_allow_html=True)
                        if st.button(
                            "🗑️  Delete Chat",
                            key=f"delete_{chat_id}",
                            use_container_width=True,
                        ):
                            delete_chat(chat_id)
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

        # ---- Settings -------------------------------------------------------
        st.markdown('<div class="sidebar-section-label">Settings</div>', unsafe_allow_html=True)

        with st.expander("⚙️  Preferences", expanded=False):

            st.markdown("**Appearance**")
            theme_choice = st.radio(
                "Theme",
                ["Dark", "Light"],
                index=0 if st.session_state.theme == "Dark" else 1,
                label_visibility="collapsed",
                horizontal=True,
                key="theme_radio",
            )
            if theme_choice != st.session_state.theme:
                st.session_state.theme = theme_choice
                st.rerun()

            st.markdown("**Similarity Threshold**")
            st.session_state.threshold = st.slider(
                "Similarity Threshold",
                min_value=0.0,
                max_value=1.0,
                value=st.session_state.threshold,
                step=0.05,
                label_visibility="collapsed",
                key="threshold_slider",
            )
            st.caption(
                "Controls how closely a question must match the knowledge "
                "base before an answer is returned."
            )

        with st.expander("ℹ️  About", expanded=False):
            st.markdown(
                """
                **SafeX AI Knowledge Assistant**

                An internal FAQ assistant for SafeX Solutions, built with
                TF-IDF + Cosine Similarity over a local knowledge base.
                """
            )

        # ---- Footer -----------------------------------------------------
        st.markdown(
            f"""
            <div class="sidebar-footer">
                SafeX AI · © {datetime.now().year}<br>
                Built with Streamlit
            </div>
            """,
            unsafe_allow_html=True,
        )


# ==============================================================================
# 7. HERO SECTION
# ==============================================================================

def render_hero() -> None:
    """Render the gradient hero header shown at the top of the main area."""
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-badge">🛡️ SafeX Solutions · Internal AI</div>
            <div class="hero-title">SafeX AI Knowledge Assistant</div>
            <div class="hero-subtitle">
                Ask anything about internships, HR policies, onboarding,
                IT support, or company FAQs — answered instantly.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 8. SUGGESTED PROMPT CARDS
# ==============================================================================

SUGGESTED_PROMPTS = [
    ("🏢", "What is SafeX?", "Learn about the company"),
    ("🕐", "Office timings", "Check working hours"),
    ("📝", "Leave policy", "How to apply for leave"),
    ("🔑", "Reset password", "IT support steps"),
    ("👥", "Contact HR", "Get in touch with HR"),
    ("🎓", "Internship rules", "Guidelines & expectations"),
]


def render_suggested_prompts() -> None:
    """Render a responsive 3-column grid of clickable suggested-question cards."""
    st.markdown('<div class="suggested-label">Try asking one of these</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (icon, title, subtitle) in enumerate(SUGGESTED_PROMPTS):
        with cols[i % 3]:
            if st.button(
                f"{icon}  **{title}**\n\n{subtitle}",
                key=f"suggested_{i}",
                use_container_width=True,
            ):
                st.session_state.pending_prompt = title
                st.rerun()


# ==============================================================================
# 9. EMPTY STATE
# ==============================================================================

def render_empty_state() -> None:
    """Render the friendly empty-state placeholder shown before any messages."""
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon-circle">💬</div>
            <p>Ask a question above, or type below to start chatting.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 10. CHAT MESSAGE RENDERING
# ==============================================================================

def render_chat_messages(messages: list) -> None:
    """Render the full conversation using native st.chat_message bubbles."""
    for message in messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "🛡️"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])


def render_typing_animation(placeholder, final_text: str) -> None:
    """
    Show a brief animated 'typing' indicator, then progressively reveal the
    final answer word-by-word inside the given placeholder container.
    """
    with placeholder.container():
        with st.chat_message("assistant", avatar="🛡️"):
            dots_area = st.empty()
            for _ in range(2):
                dots_area.markdown(
                    '<div class="typing-dots"><span></span><span></span><span></span></div>',
                    unsafe_allow_html=True,
                )
                time.sleep(0.35)

            # Word-by-word reveal for a natural "streaming" feel
            words = final_text.split(" ")
            revealed = ""
            text_area = dots_area
            for word in words:
                revealed += word + " "
                text_area.markdown(revealed + "▌")
                time.sleep(0.03)
            text_area.markdown(revealed.strip())


def scroll_to_bottom() -> None:
    """Inject a tiny invisible HTML component that auto-scrolls the page to
    the bottom, keeping the latest message in view.
    """
    st.components.v1.html(
        """
        <script>
            var mainEl = window.parent.document.querySelector('section.main');
            if (mainEl) { mainEl.scrollTo({top: mainEl.scrollHeight, behavior: 'smooth'}); }
        </script>
        """,
        height=0,
    )


# ==============================================================================
# 11. FOOTER
# ==============================================================================

def render_footer() -> None:
    """Render a slim, professional credit bar pinned directly beneath the
    chat input box, in the exact style of a production SaaS product."""
    st.markdown(
        """
        <div class="pinned-footer">
            SafeX AI Knowledge Assistant&nbsp;&nbsp;·&nbsp;&nbsp;Powered by TF-IDF & Cosine Similarity&nbsp;&nbsp;·&nbsp;&nbsp;© 2026 SafeX Solutions
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 12. MAIN APPLICATION FLOW
# ==============================================================================

def main() -> None:
    """Application entry point — wires together state, sidebar, and chat UI."""

    init_session_state()
    inject_css(st.session_state.theme)
    render_sidebar()

    current_chat = get_current_chat()
    messages = current_chat["messages"]

    # ---- Hero + suggestions only shown on an empty conversation ----------
    if len(messages) == 0:
        render_hero()
        render_suggested_prompts()
        st.markdown("<br>", unsafe_allow_html=True)
        render_empty_state()
    else:
        render_chat_messages(messages)

    response_placeholder = st.empty()

    # ---- Chat input ---------------------------------------------------------
    prompt = st.chat_input("Message SafeX AI...")

    if st.session_state.pending_prompt:
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    # ---- Handle a new user message ------------------------------------------
    if prompt:
        messages.append({"role": "user", "content": prompt})
        auto_title_from_first_message(st.session_state.current_chat_id, prompt)

        # Re-render the user's message immediately for instant feedback
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # Generate (placeholder) response with a typing animation
        answer = get_chatbot_response(prompt, st.session_state.threshold)
        render_typing_animation(response_placeholder, answer)

        messages.append({"role": "assistant", "content": answer})
        scroll_to_bottom()
        st.rerun()

    render_footer()


# ==============================================================================
# ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    main()
