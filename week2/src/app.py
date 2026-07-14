# ==============================================================================
# SafeX AI & Automation Suite
# Premium ChatGPT / Claude / Copilot-style Hub
# ------------------------------------------------------------------------------
# Tech Stack : Python + Streamlit
# Author     : Group 54 Lead
# ==============================================================================

import os
import sys
import importlib

# Ensure the project root directory is in the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="SafeX AI & Automation Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.modules.registry import MODULE_REGISTRY


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
    """Render the main navigation and active workspace sub-menus in the sidebar."""
    with st.sidebar:
        # ---- Brand header ----
        st.markdown(
            """
            <div class="brand-wrap">
                <div class="brand-icon">🛡️</div>
                <div>
                    <div class="brand-text-title">SafeX Platform</div>
                    <div class="brand-text-sub">AI & Automation Hub</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---- Workspace Navigation ----
        st.markdown('<div class="sidebar-section-label">Active Workspace</div>', unsafe_allow_html=True)
        workspaces = [
            "⚙️ Week 2: Automation Suite",
            "👥 Team Dashboard"
        ]
        
        # Initialize default workspace if not present
        if "active_workspace_sel" not in st.session_state:
            st.session_state.active_workspace_sel = workspaces[0]

        active_ws = st.selectbox(
            "Active Workspace",
            workspaces,
            index=workspaces.index(st.session_state.active_workspace_sel),
            key="workspace_select_widget",
            label_visibility="collapsed"
        )
        
        if active_ws != st.session_state.active_workspace_sel:
            st.session_state.active_workspace_sel = active_ws
            st.rerun()

        # ---- Workspace Specific Controls ----
        if False:
            pass
            
        elif st.session_state.active_workspace_sel == "⚙️ Week 2: Automation Suite":
            st.markdown('<div class="sidebar-section-label">Automation Prototypes</div>', unsafe_allow_html=True)
            module_keys = list(MODULE_REGISTRY["week2"].keys())
            module_titles = [
                f"{MODULE_REGISTRY['week2'][k]['icon']} {MODULE_REGISTRY['week2'][k]['title']}"
                for k in module_keys
            ]

            if "active_module_key" not in st.session_state:
                st.session_state.active_module_key = module_keys[0]

            curr_idx = module_keys.index(st.session_state.active_module_key) if st.session_state.active_module_key in module_keys else 0
            
            selected_title = st.radio(
                "Select Module",
                module_titles,
                index=curr_idx,
                label_visibility="collapsed",
                key="week2_module_radio"
            )
            
            selected_key = module_keys[module_titles.index(selected_title)]
            if selected_key != st.session_state.active_module_key:
                st.session_state.active_module_key = selected_key
                st.rerun()
                
            st.markdown('<div class="sidebar-section-label">General Info</div>', unsafe_allow_html=True)
            st.caption("Each prototype serves as a modular task assigned to Group 54 members for Week 2 Business Automation Research.")

        elif st.session_state.active_workspace_sel == "👥 Team Dashboard":
            st.markdown('<div class="sidebar-section-label">Team Summary</div>', unsafe_allow_html=True)
            st.caption("Group 54 consists of 1 Leader and 7 Members collaborating on modular business automation stubs for SafeX Solutions.")
            
        # ---- Preferences & Settings ----
        st.markdown('<div class="sidebar-section-label">Global Settings</div>', unsafe_allow_html=True)
        with st.expander("🎨  Theme", expanded=False):
            theme_choice = st.radio(
                "Appearance Theme",
                ["Dark", "Light"],
                index=0 if st.session_state.theme == "Dark" else 1,
                label_visibility="collapsed",
                horizontal=True,
                key="theme_radio_widget",
            )
            if theme_choice != st.session_state.theme:
                st.session_state.theme = theme_choice
                st.rerun()

        # ---- Footer ----
        st.markdown(
            f"""
            <div class="sidebar-footer">
                SafeX Suite · © 2026<br>
                Group 54 Collaboration
            </div>
            """,
            unsafe_allow_html=True,
        )

def render_team_dashboard() -> None:
    """Renders the Team Dashboard display showing developers, tasks, and progress."""
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-badge">👥 Team Registry & Contributor Hub</div>
            <div class="hero-title">Group 54 Task Allocation</div>
            <div class="hero-subtitle">
                Comprehensive tracking registry for Week 1 & Week 2 module assignments, roles, and status details.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Progress Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Group Members", "8 Members")
    with m2:
        st.metric("Week 1 Progress", "100% Completed", help="Semantic FAQ Chatbot collaboration")
    with m3:
        st.metric("Week 2 Status", "Scaffolding Active", help="Individual Business Automation Research stubs")

    st.markdown("<br><h3>👥 Contributor Matrix</h3>", unsafe_allow_html=True)

    # Week 1 Row Card
    w1_meta = MODULE_REGISTRY["week1"]["faq_chatbot"]
    st.markdown(f"""
    <div class="team-card" style="
        background: rgba(56, 139, 253, 0.05);
        border: 1px solid rgba(56, 139, 253, 0.25);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 20px;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 1.2em; font-weight: bold; color: #58A6FF;">{w1_meta['title']} (Week 1)</span>
            <span style="font-size: 0.85em; background: rgba(88, 166, 255, 0.2); color: #58A6FF; padding: 4px 10px; border-radius: 12px; font-weight: bold;">{w1_meta['role']}</span>
        </div>
        <div style="margin-top: 8px; font-size: 0.9em; color: #8B949E;">
            <strong>Assigned Developer:</strong> {w1_meta['developer']} &nbsp;|&nbsp;
            <strong>Status:</strong> <span style="color: #56D364; font-weight: bold;">{w1_meta['status']}</span> &nbsp;|&nbsp;
            <strong>Required Stack:</strong> {', '.join(w1_meta['tech'])}
        </div>
        <div style="margin-top: 8px; font-size: 0.9em; color: #C9D1D9;">
            {w1_meta['description']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h4>Week 2 Task Allocation & Module Stubs</h4>", unsafe_allow_html=True)

    # Week 2 grid cards
    for key, member in MODULE_REGISTRY["week2"].items():
        st.markdown(f"""
        <div class="team-card" style="
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 1.1em; font-weight: bold; color: #E3B341;">{member['title']}</span>
                <span style="font-size: 0.85em; background: rgba(227, 179, 65, 0.1); color: #E3B341; padding: 2px 8px; border-radius: 12px;">{member['role']}</span>
            </div>
            <div style="margin-top: 8px; font-size: 0.9em; color: #8B949E;">
                <strong>Assigned Developer:</strong> {member['developer']} &nbsp;|&nbsp;
                <strong>Contact:</strong> <a href="mailto:{member['email']}" style="color: #58A6FF; text-decoration: none;">{member['email']}</a> &nbsp;|&nbsp;
                <strong>Status:</strong> <span style="color: #AEB1B5; font-style: italic;">{member['status']}</span>
            </div>
            <div style="margin-top: 6px; font-size: 0.85em; color: #8B949E;">
                <strong>Required Stack:</strong> {', '.join(member['tech'])} &nbsp;|&nbsp;
                <strong>Difficulty:</strong> {member['difficulty']}
            </div>
            <div style="margin-top: 8px; font-size: 0.9em; color: #C9D1D9;">
                {member['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_footer() -> None:
    """Render a slim, professional credit bar pinned at the bottom."""
    st.markdown(
        """
        <div class="pinned-footer">
            SafeX AI & Automation Suite&nbsp;&nbsp;·&nbsp;&nbsp;Modular Refactoring Hub&nbsp;&nbsp;·&nbsp;&nbsp;© 2026 SafeX Solutions
        </div>
        """,
        unsafe_allow_html=True,
    )

def main() -> None:
    """Application entry point — routes between Week 1, Week 2 and Dashboard workspaces."""
    # Ensure theme is initialized in session state
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"

    inject_css(st.session_state.theme)
    render_sidebar()

    # Routing main container
    active_ws = st.session_state.get("active_workspace_sel", "📚 Week 1: FAQ Assistant")
    
    if False:
        pass
        
    elif active_ws == "⚙️ Week 2: Automation Suite":
        # Load and run the selected Week 2 stub module UI dynamically
        active_key = st.session_state.get("active_module_key")
        if active_key in MODULE_REGISTRY["week2"]:
            module_meta = MODULE_REGISTRY["week2"][active_key]
            try:
                module_ui = importlib.import_module(module_meta["import_path"])
                module_ui.render_ui()
            except Exception as e:
                st.error(f"Failed to load UI module for '{active_key}'. Detail: {str(e)}")
        else:
            st.error("No active automation module selected.")
            
    elif active_ws == "👥 Team Dashboard":
        render_team_dashboard()

    render_footer()

if __name__ == "__main__":
    main()
