"""Streamlit UI for Invoice / Proposal Generator Agent (Malik Sudais)."""

import streamlit as st
from src.modules.proposal_invoice_generator.engine import ProposalInvoiceGeneratorEngineStub
from src.modules.registry import MODULE_REGISTRY


def render_ui() -> None:
    """Render scaffolding screen for Malik Sudais's module."""
    metadata = MODULE_REGISTRY["week3"]["proposal_invoice_generator"]
    stub = ProposalInvoiceGeneratorEngineStub()
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
