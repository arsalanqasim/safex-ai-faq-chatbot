# ==============================================================================
# SafeX AI Knowledge Assistant
# Premium ChatGPT / Claude / Copilot-style Frontend
# ------------------------------------------------------------------------------
# Tech Stack : Python + Streamlit (frontend only)
# Backend    : Placeholder — to be replaced with chatbot.py -> FAQChatbot
# Author     : Frontend Engineering Team
# ==============================================================================

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
        st.session_state.threshold = 0.60

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
        --bg-app:#0F172A;
        --bg-app-2:#1E293B;
        --bg-sidebar:#020617;
        --bg-sidebar-hover:#0B1220;
        --bg-sidebar-active:rgba(59,130,246,0.15);
        --border-soft:#334155;
        --border-strong:#475569;
        --text-primary:#F8FAFC;
        --text-secondary:#CBD5E1;
        --text-muted:#94A3B8;
        --bubble-user-bg:#2563EB;
        --bubble-user-text:#FFFFFF;
        --bubble-bot-bg:#1E293B;
        --bubble-bot-border:#334155;
        --bubble-bot-text:#F8FAFC;
        --accent:#3B82F6;
        --accent-hover:#2563EB;
        --accent-soft:rgba(59,130,246,0.15);
        --card-bg:#1E293B;
        --card-border:#334155;
        --success:#10B981;
        --warning:#F59E0B;
        --error:#EF4444;
        --shadow-soft:0 8px 24px rgba(0,0,0,0.35);
        --shadow-card:0 4px 14px rgba(0,0,0,0.28);
        --shadow-btn:0 6px 18px rgba(37,99,235,0.35);
        --glass-bg:rgba(2,6,23,0.72);
        --scrollbar-thumb:#334155;
        """
    else:
        vars_css = """
        --bg-app:#F8FAFC;
        --bg-app-2:#F1F5F9;
        --bg-sidebar:#FFFFFF;
        --bg-sidebar-hover:#F1F5F9;
        --bg-sidebar-active:rgba(37,99,235,0.08);
        --border-soft:#E2E8F0;
        --border-strong:#CBD5E1;
        --text-primary:#0F172A;
        --text-secondary:#64748B;
        --text-muted:#94A3B8;
        --bubble-user-bg:#2563EB;
        --bubble-user-text:#FFFFFF;
        --bubble-bot-bg:#FFFFFF;
        --bubble-bot-border:#E2E8F0;
        --bubble-bot-text:#0F172A;
        --accent:#2563EB;
        --accent-hover:#1D4ED8;
        --accent-soft:rgba(37,99,235,0.08);
        --card-bg:#FFFFFF;
        --card-border:#E2E8F0;
        --success:#10B981;
        --warning:#F59E0B;
        --error:#EF4444;
        --shadow-soft:0 4px 14px rgba(15,23,42,0.06);
        --shadow-card:0 2px 8px rgba(15,23,42,0.05);
        --shadow-btn:0 6px 16px rgba(37,99,235,0.22);
        --glass-bg:rgba(255,255,255,0.78);
        --scrollbar-thumb:#CBD5E1;
        """

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@700;800&display=swap');

        :root {{
            {vars_css}
        }}

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        /* ---------- Hide default Streamlit chrome ---------- */
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        div[data-testid="stDecoration"] {{ display: none; }}
        div[data-testid="stStatusWidget"] {{ display: none; }}

        /* Keep the header bar itself (it contains the sidebar
           expand/collapse arrow) fully intact and functional. Only the
           "Deploy" button and the "⋮" menu are hidden individually, using
           their own stable identifiers - never the shared toolbar
           container, which is also where the sidebar toggle lives. */
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

        /* Sidebar collapse / expand arrows must always stay visible and
           clickable - never touched by the rules above. Also force the
           arrow icon's color so it's visible on light backgrounds too
           (it defaults to a very pale color that disappears on white).
           These selectors are intentionally broad/redundant since the
           exact DOM testid for this control varies across Streamlit
           versions - better to over-match than to miss it. */
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
        /* Catch-all: if the arrow is a font glyph instead of an SVG,
           `fill`/`stroke` won't touch it, but `color` will. */
        header[data-testid="stHeader"] *,
        [data-testid="stSidebarCollapseButton"] *,
        [data-testid="collapsedControl"] *,
        [data-testid="stSidebarCollapsedControl"] * {{
            color: var(--text-primary) !important;
        }}

        /* Sidebar: fixed usable width while expanded. When the user
           collapses it, let Streamlit's default behavior take over so the
           main content area reclaims the full page width instead of
           leaving an empty gap. */
        section[data-testid="stSidebar"][aria-expanded="true"] {{
            min-width: 300px !important;
            max-width: 340px !important;
        }}
        section[data-testid="stSidebar"] {{
            transition: min-width 0.2s ease, max-width 0.2s ease, margin-left 0.2s ease;
        }}

        .stApp {{
            background: var(--bg-app);
        }}

        /* Safety-net default: ANY native Streamlit button (any "kind",
           any nesting depth) starts themed correctly. More specific rules
           below (accent buttons, sidebar rows, danger hovers, etc.) then
           override this as needed. This prevents Streamlit's own default
           button skin from ever showing through unstyled. */
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

        /* The fixed bottom bar wrapping the chat input must follow the
           theme too - otherwise it defaults to Streamlit's own dark skin
           regardless of the app's selected theme. */
        div[data-testid="stBottom"],
        div[data-testid="stBottomBlockContainer"] {{
            background: var(--bg-app) !important;
        }}

        /* Global widget theming so every native Streamlit control
           (expanders, sliders, radios, inputs, captions) follows the
           selected theme instead of staying on Streamlit's own defaults. */
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

        /* Text inputs (search box, rename box) everywhere, not just the
           sidebar - fully themed background, border, text and caret. */
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

        /* Expanders (Preferences / About) */
        div[data-testid="stExpander"] {{
            background: var(--card-bg) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 14px !important;
            box-shadow: var(--shadow-card);
        }}
        div[data-testid="stExpander"] summary,
        div[data-testid="stExpander"] details,
        div[data-testid="stExpander"] > details > summary {{
            background: var(--card-bg) !important;
            color: var(--text-primary) !important;
            border-radius: 14px !important;
        }}
        div[data-testid="stExpander"] summary:hover {{
            color: var(--accent-hover) !important;
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

        /* Slider: track, filled portion, handle, and the min/max/value
           numbers Streamlit renders above/below the handle. */
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

        /* Radio buttons (theme selector) */
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

        /* Tooltips shown on hover */
        div[data-baseweb="tooltip"] {{
            background: var(--bg-sidebar-active) !important;
            color: var(--text-primary) !important;
        }}

        /* ---------- Scrollbars ---------- */
        ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
        ::-webkit-scrollbar-thumb {{
            background: var(--scrollbar-thumb);
            border-radius: 10px;
        }}
        ::-webkit-scrollbar-track {{ background: transparent; }}

        .block-container {{
            padding-top: 1.6rem;
            padding-bottom: 6.5rem;
            max-width: 880px;
        }}

        /* ==========================================================
           SIDEBAR
        ========================================================== */
        section[data-testid="stSidebar"] {{
            background: var(--bg-sidebar);
            border-right: 1px solid var(--border-soft);
        }}
        section[data-testid="stSidebar"] .block-container {{
            padding: 1.25rem 1rem 1.1rem 1rem;
        }}

        .brand-wrap {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 2px 4px 18px 4px;
            border-bottom: 1px solid var(--border-soft);
            margin-bottom: 18px;
        }}
        .brand-icon {{
            width: 40px; height: 40px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent), #7c3aed);
            display: flex; align-items: center; justify-content: center;
            font-size: 19px;
            box-shadow: var(--shadow-btn);
        }}
        .brand-text-title {{
            color: var(--text-primary);
            font-family: 'Manrope', sans-serif;
            font-weight: 800;
            font-size: 15.5px;
            line-height: 1.15;
            letter-spacing: -0.01em;
        }}
        .brand-text-sub {{
            color: var(--text-muted);
            font-size: 11px;
            font-weight: 500;
            margin-top: 2px;
        }}

        .sidebar-section-label {{
            color: var(--text-muted);
            font-size: 10.5px;
            font-weight: 700;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            margin: 22px 4px 10px 4px;
        }}

        /* New Chat button */
        .new-chat-btn button {{
            background: var(--accent) !important;
            color: #fff !important;
            font-weight: 600 !important;
            font-size: 13.5px !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.65rem 0.9rem !important;
            box-shadow: var(--shadow-btn);
            transition: all 0.25s ease !important;
        }}
        .new-chat-btn button:hover {{
            background: var(--accent-hover) !important;
            transform: translateY(-2px);
            box-shadow: 0 10px 22px rgba(37,99,235,0.32);
        }}

        /* Search input */
        section[data-testid="stSidebar"] input[type="text"] {{
            background: var(--bg-app-2) !important;
            border: 1px solid var(--border-soft) !important;
            color: var(--text-primary) !important;
            border-radius: 11px !important;
            font-size: 13px !important;
            transition: all 0.25s ease !important;
        }}
        section[data-testid="stSidebar"] input[type="text"]:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px var(--accent-soft) !important;
        }}

        /* Chat history rows */
        .chat-row {{
            display: flex;
            align-items: center;
            gap: 4px;
            margin-bottom: 4px;
            border-radius: 12px;
        }}
        /* Vertically align every column in a sidebar chat row (title +
           three-dot menu) so nothing looks offset. */
        section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {{
            align-items: center !important;
        }}
        section[data-testid="stSidebar"] div[data-testid="column"] {{
            display: flex !important;
            align-items: center !important;
        }}
        section[data-testid="stSidebar"] .stButton button {{
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-secondary);
            text-align: left;
            border-radius: 10px;
            font-size: 13.2px;
            font-weight: 500;
            padding: 8px 10px;
            transition: background-color 0.25s ease, color 0.25s ease;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        section[data-testid="stSidebar"] .stButton button:hover {{
            background: var(--bg-sidebar-hover);
            color: var(--text-primary);
        }}
        .chat-row.active .stButton button {{
            background: var(--bg-sidebar-active) !important;
            color: var(--accent) !important;
            font-weight: 600 !important;
        }}

        /* ---- Three-dot context menu (st.popover) ---- */
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
            font-size: 15px !important;
            font-weight: 700 !important;
            width: 30px !important;
            height: 30px !important;
            min-width: 30px !important;
            padding: 0 !important;
            margin: 0 auto !important;
            border-radius: 9px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            line-height: 1 !important;
            transition: all 0.25s ease !important;
        }}
        .menu-trigger div[data-testid="stPopover"] button:hover {{
            color: var(--accent) !important;
            background: var(--bg-sidebar-hover) !important;
            border-color: var(--border-soft) !important;
        }}

        /* Popover panel itself: perfectly centered under the trigger,
           proper width/padding, rounded corners, shadow, high z-index,
           no clipping or overflow. Streamlit renders this via a floating
           portal (BaseWeb popover), so we only need to style its body. */
        div[data-baseweb="popover"] {{
            z-index: 999999 !important;
        }}
        div[data-baseweb="popover"] [data-testid="stPopoverBody"],
        div[data-baseweb="popover"] > div > div {{
            background: var(--card-bg) !important;
            border: 1px solid var(--card-border) !important;
            border-radius: 14px !important;
            box-shadow: var(--shadow-soft) !important;
            padding: 6px !important;
            min-width: 190px !important;
            overflow: visible !important;
        }}
        div[data-testid="stPopoverBody"] .stButton button,
        [data-testid="stPopoverBody"] .stButton button {{
            background: transparent !important;
            border: none !important;
            color: var(--text-primary) !important;
            text-align: left !important;
            font-size: 13.5px !important;
            font-weight: 500 !important;
            padding: 9px 12px !important;
            border-radius: 10px !important;
            width: 100% !important;
            transition: background-color 0.2s ease !important;
        }}
        div[data-testid="stPopoverBody"] .stButton button:hover,
        [data-testid="stPopoverBody"] .stButton button:hover {{
            background: var(--bg-sidebar-hover) !important;
        }}
        .popover-danger .stButton button:hover {{
            background: rgba(239, 68, 68, 0.1) !important;
            color: var(--error) !important;
        }}

        /* Settings expander */
        section[data-testid="stSidebar"] details {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            margin-bottom: 10px;
        }}
        section[data-testid="stSidebar"] summary {{
            color: var(--text-primary) !important;
            font-size: 13.3px !important;
            font-weight: 600 !important;
            padding: 6px 4px;
        }}

        section[data-testid="stSidebar"] label {{
            color: var(--text-secondary) !important;
            font-size: 12.5px !important;
        }}

        /* Footer inside sidebar */
        .sidebar-footer {{
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid var(--border-soft);
            color: var(--text-muted);
            font-size: 11px;
            text-align: center;
        }}

        /* ==========================================================
           HERO SECTION
        ========================================================== */
        .hero-wrap {{
            text-align: center;
            padding: 20px 10px 30px 10px;
        }}
        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--accent-soft);
            color: var(--accent);
            font-size: 11.5px;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            padding: 6px 14px;
            border-radius: 999px;
            margin-bottom: 20px;
            border: 1px solid var(--accent-soft);
        }}
        .hero-title {{
            font-family: 'Manrope', sans-serif;
            font-size: 40px;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1.15;
            background: linear-gradient(90deg, var(--text-primary) 30%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
        }}
        .hero-subtitle {{
            font-size: 15.5px;
            color: var(--text-secondary);
            max-width: 560px;
            margin: 0 auto;
            line-height: 1.7;
        }}

        /* ==========================================================
           SUGGESTED PROMPT CARDS
        ========================================================== */
        .suggested-label {{
            color: var(--text-muted);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 10px 2px 14px 2px;
        }}
        div[data-testid="column"] .stButton button {{
            background: var(--card-bg) !important;
            border: 1px solid var(--card-border) !important;
            color: var(--text-primary) !important;
            border-radius: 14px !important;
            text-align: left;
            padding: 16px 18px;
            font-size: 13.6px;
            font-weight: 500;
            width: 100%;
            min-height: 72px;
            box-shadow: var(--shadow-card);
            transition: all 0.25s ease;
        }}
        div[data-testid="column"] .stButton button:hover {{
            border-color: var(--accent) !important;
            background: var(--bg-app-2) !important;
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(37,99,235,0.15);
        }}
        div[data-testid="column"] .stButton button p {{
            color: var(--text-primary) !important;
        }}

        /* ==========================================================
           EMPTY STATE
        ========================================================== */
        .empty-state {{
            text-align: center;
            padding: 34px 20px 12px 20px;
            color: var(--text-muted);
        }}
        .empty-state .icon-circle {{
            width: 56px; height: 56px;
            border-radius: 16px;
            margin: 0 auto 16px auto;
            background: linear-gradient(135deg, var(--accent), #7c3aed);
            display: flex; align-items: center; justify-content: center;
            font-size: 26px;
            box-shadow: var(--shadow-btn);
        }}
        .empty-state p {{ font-size: 13.5px; }}

        /* ==========================================================
           CHAT MESSAGES (st.chat_message overrides)
        ========================================================== */
        div[data-testid="stChatMessage"] {{
            background: transparent;
            padding: 12px 4px;
            margin-bottom: 6px;
            border-radius: 16px;
            animation: fadeInUp 0.35s ease;
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}

        /* User message bubble */
        div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {{
            justify-content: flex-end;
        }}
        div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) .stMarkdown {{
            background: var(--bubble-user-bg);
            color: var(--bubble-user-text);
            padding: 13px 18px;
            border-radius: 18px 18px 4px 18px;
            box-shadow: 0 6px 18px rgba(37,99,235,0.25);
            max-width: 620px;
            font-size: 14.5px;
            line-height: 1.6;
        }}

        /* Assistant message bubble */
        div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) .stMarkdown {{
            background: var(--bubble-bot-bg);
            border: 1px solid var(--bubble-bot-border);
            color: var(--bubble-bot-text);
            padding: 14px 19px;
            border-radius: 18px 18px 18px 4px;
            box-shadow: var(--shadow-card);
            max-width: 640px;
            font-size: 14.5px;
            line-height: 1.65;
        }}

        div[data-testid="chatAvatarIcon-user"] {{
            background: var(--accent) !important;
            box-shadow: 0 4px 10px rgba(37,99,235,0.3);
        }}
        div[data-testid="chatAvatarIcon-assistant"] {{
            background: linear-gradient(135deg, #8b5cf6, #6d28d9) !important;
            box-shadow: 0 4px 10px rgba(124,58,237,0.3);
        }}

        /* Typing indicator dots */
        .typing-dots span {{
            display: inline-block;
            width: 6px; height: 6px;
            margin-right: 3px;
            background: var(--text-muted);
            border-radius: 50%;
            animation: blink 1.3s infinite ease-in-out both;
        }}
        .typing-dots span:nth-child(1) {{ animation-delay: -0.28s; }}
        .typing-dots span:nth-child(2) {{ animation-delay: -0.14s; }}
        @keyframes blink {{
            0%, 80%, 100% {{ opacity: 0.25; transform: scale(0.85); }}
            40% {{ opacity: 1; transform: scale(1); }}
        }}

        /* ==========================================================
           CHAT INPUT (fixed bottom, glass effect)
        ========================================================== */
        div[data-testid="stChatInput"] {{
            background: var(--glass-bg);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border-top: 1px solid var(--border-soft);
            padding: 14px 0 10px 0;
        }}
        div[data-testid="stChatInput"] textarea {{
            background: var(--card-bg) !important;
            border: 1.5px solid var(--border-soft) !important;
            color: var(--text-primary) !important;
            border-radius: 16px !important;
            font-size: 14.5px !important;
            box-shadow: var(--shadow-card);
            transition: all 0.25s ease !important;
        }}
        div[data-testid="stChatInput"] textarea:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px var(--accent-soft) !important;
        }}
        div[data-testid="stChatInput"] button {{
            background: var(--accent) !important;
            border-radius: 12px !important;
            transition: all 0.25s ease !important;
        }}
        div[data-testid="stChatInput"] button:hover {{
            background: var(--accent-hover) !important;
        }}

        /* Push Streamlit's fixed bottom input container up so our footer
           bar can sit directly underneath it without overlapping. */
        div[data-testid="stBottom"] {{
            bottom: 30px !important;
        }}

        /* Slim footer bar, pinned to the very bottom of the viewport,
           directly below the chat input. */
        .pinned-footer {{
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 999999;
            text-align: center;
            font-size: 11px;
            color: var(--text-muted);
            background: var(--bg-app);
            padding: 6px 0;
            border-top: 1px solid var(--border-soft);
        }}

        /* ==========================================================
           MISC
        ========================================================== */
        hr {{ border-color: var(--border-soft); }}

        .app-footer {{
            text-align: center;
            color: var(--text-muted);
            font-size: 11.5px;
            padding: 18px 0 4px 0;
        }}

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
    """Inject a tiny invisible iframe that auto-scrolls the page to
    the bottom, keeping the latest message in view.

    Uses st.iframe instead of the deprecated st.components.v1.html.
    """
    st.iframe(
        html="""
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
