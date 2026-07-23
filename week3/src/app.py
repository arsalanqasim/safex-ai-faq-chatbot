"""Shared Streamlit shell for Week 3 AI Agent Automation Proposal Suite."""

from __future__ import annotations

import importlib
import os
import sys

import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.modules.registry import MODULE_REGISTRY


st.set_page_config(page_title="SafeX AI Agent Suite · Week 3", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")


def inject_css() -> None:
    """Style the shared shell matching Week 1 and Week 2 design aesthetics."""
    st.markdown(
        """
        <style>
        :root { --ink: #172033; --muted: #64748b; --line: #dce3ec; --soft: #f6f8fb; --accent: #0f766e; --accent-dark: #0b5e58; }
        #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
        header[data-testid="stHeader"] { background: var(--soft); }
        .stApp, [data-testid="stAppViewContainer"] { background: var(--soft); color: var(--ink); }
        section[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid var(--line); }
        section[data-testid="stSidebar"] > div { padding-top: 1.25rem; }
        .block-container { max-width: 1180px; padding-top: 3.5rem; padding-bottom: 4rem; }
        html, body, [class*="css"] { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
        h1, h2, h3, p { color: var(--ink); }
        .app-mark { display: flex; gap: 10px; align-items: center; margin-bottom: 1.6rem; }
        .app-mark__square { display: grid; place-items: center; width: 34px; height: 34px; border-radius: 8px; background: var(--accent); color: white; font-weight: 700; font-size: 1.1rem; }
        .app-mark__name { font-size: 0.95rem; font-weight: 700; color: var(--ink); }
        .app-mark__caption { font-size: 0.75rem; color: var(--muted); }
        .side-heading { color: var(--muted); font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin: 1.35rem 0 0.4rem; }
        .sidebar-note { color: var(--muted); font-size: 0.8rem; line-height: 1.45; margin-top: 1rem; }
        .stButton > button { border-radius: 6px; border: 1px solid var(--line); background: #ffffff; color: var(--ink); font-weight: 600; min-height: 2.45rem; box-shadow: none; }
        .stButton > button:hover { border-color: var(--accent); color: var(--accent); background: #f0fdfa; }
        .stButton > button[kind="primary"] { background: var(--accent); color: #ffffff; border-color: var(--accent); }
        .stButton > button[kind="primary"]:hover { background: var(--accent-dark); color: #ffffff; }
        [data-testid="stMetric"] { background: #ffffff; border: 1px solid var(--line); border-radius: 7px; padding: 0.85rem; }
        div[data-testid="stExpander"] { border: 1px solid var(--line); border-radius: 6px; background: #ffffff; }
        [data-testid="stDataFrame"], [data-testid="stDataEditor"] { border: 1px solid var(--line); border-radius: 7px; overflow: hidden; }
        [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea, [data-baseweb="select"] > div { border-radius: 6px; border-color: var(--line); background: #ffffff; color: var(--ink); }
        .hero-wrap { background: #ffffff; border: 1px solid var(--line); border-radius: 10px; padding: 1.5rem 1.75rem; margin-bottom: 1.5rem; }
        .hero-badge { display: inline-block; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent); background: #e6f5f2; padding: 0.25rem 0.6rem; border-radius: 4px; margin-bottom: 0.5rem; }
        .hero-title { font-size: 1.6rem; font-weight: 800; color: var(--ink); margin-bottom: 0.25rem; }
        .hero-subtitle { font-size: 0.95rem; color: var(--muted); line-height: 1.5; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> str:
    """Render shared module navigation and return the selected module key."""
    modules = MODULE_REGISTRY["week3"]
    active_key = st.session_state.get("active_module_key", "customer_support_chatbot")
    if active_key not in modules:
        active_key = "customer_support_chatbot"
    with st.sidebar:
        st.markdown(
            """
            <div class="app-mark">
                <div class="app-mark__square">S</div>
                <div><div class="app-mark__name">SafeX Group 54</div><div class="app-mark__caption">AI Agent Proposals · Week 3</div></div>
            </div>
            <div class="side-heading">Modules Roster</div>
            """,
            unsafe_allow_html=True,
        )
        for key, module in modules.items():
            icon = module.get("icon", "📦")
            label = f"{icon} {module['title']}"
            if st.button(label, key=f"module_{key}", use_container_width=True):
                active_key = key
                st.session_state.active_module_key = key
                st.rerun()
        st.divider()
        st.markdown('<div class="side-heading">Workspace Info</div>', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-note">Week 3 AI Agent Automation Proposal suite for SafeX Solutions. Each member module is independently owned.</p>', unsafe_allow_html=True)
    return active_key


def apply_active_module_style(active_key: str) -> None:
    """Highlight the module currently displayed in the workspace."""
    st.markdown(
        f"""
        <style>
        div.st-key-module_{active_key} button {{
            background: #e6f5f2;
            border-color: var(--accent);
            color: var(--accent-dark);
            box-shadow: inset 3px 0 0 var(--accent);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_module(active_key: str) -> None:
    metadata = MODULE_REGISTRY["week3"][active_key]
    try:
        module_lib = importlib.import_module(metadata["import_path"])
        module_lib.render_ui()
    except Exception as exc:
        st.error(f"The {metadata['title']} module could not be loaded.")
        st.exception(exc)


def main() -> None:
    inject_css()
    active_key = render_sidebar()
    apply_active_module_style(active_key)
    render_module(active_key)


if __name__ == "__main__":
    main()
