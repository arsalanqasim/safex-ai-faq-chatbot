"""Streamlit UI for AI Social Media Scheduler (Ali Ammar Haider)."""

import streamlit as st
from src.modules.registry import MODULE_REGISTRY
from src.modules.social_media_scheduler.engine import SocialMediaSchedulerEngineStub


def render_ui() -> None:
    """Render scaffolding screen for Ali Ammar Haider's module."""
    metadata = MODULE_REGISTRY["week3"]["social_media_scheduler"]
    stub = SocialMediaSchedulerEngineStub()
    info = stub.get_info()

    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">⏳ Assigned Module Scaffolding</div>
            <div class="hero-title">{metadata["title"]}</div>
            <div class="hero-subtitle">
                Assigned to: <strong>{info["developer"]}</strong> ({metadata["role"]})<br/>
                Status: <code>{info["status"]}</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(f"**Developer Contact:** {metadata['email']}  \n**Tech Stack:** {' · '.join(metadata['tech'])}")
    st.subheader("Assigned Task Details")
    st.write(info["task_details"])
    st.warning("⚠️ **Implementation Status:** Placeholder scaffolding ready. Pending individual code contribution.")
