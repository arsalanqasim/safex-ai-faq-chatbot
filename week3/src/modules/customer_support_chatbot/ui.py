"""Streamlit UI for AI Customer Support Chatbot Module (Arsalan Qasim - Leader Module)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.modules.customer_support_chatbot.engine import BENCHMARK_TEST_SUITE, CustomerSupportEngine
from src.modules.registry import MODULE_REGISTRY


def render_ui() -> None:
    """Render Arsalan Qasim's submission-ready AI Customer Support Chatbot module."""
    metadata = MODULE_REGISTRY["week3"]["customer_support_chatbot"]
    engine = CustomerSupportEngine()

    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">🛡️ Submission Ready · Group Leader Module</div>
            <div class="hero-title">{metadata["title"]}</div>
            <div class="hero-subtitle">
                Developer: <strong>{metadata["developer"]}</strong> ({metadata["role"]}) · <code>{metadata["email"]}</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("📌 Module Overview & Specifications", expanded=False):
        st.write(f"**Objective:** {metadata['description']}")
        st.write(f"**Tech Stack:** {' · '.join(metadata['tech'])}")
        st.write("**Target Company:** ThreadStyle Co. / SafeX Apparel (E-Commerce Clothing Brand)")
        st.write("**Scope Handled:** 12 Top Repetitive Queries, Intent Classifier, Human Escalation Triggers, Accuracy Evaluation, Report Export.")

    tab1, tab2, tab3, tab4 = st.tabs(["💬 Live Chat Prototype", "🎯 10+ Query Accuracy Benchmark", "🗺️ Conversation Flow & Rules", "📥 Audit & Report Export"])

    with tab1:
        st.subheader("Interactive Customer Support Chat Assistant")
        st.caption("Ask any question regarding clothing orders, sizing, returns, shipping, or store locations.")

        st.markdown("**Sample Quick Prompts:**")
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        if col_p1.button("📦 Where is order #TS-98421?"):
            st.session_state.chat_input_val = "Where is order #TS-98421?"
        if col_p2.button("👕 What size for chest 40?"):
            st.session_state.chat_input_val = "What size for chest 40?"
        if col_p3.button("🔄 How to exchange a shirt?"):
            st.session_state.chat_input_val = "How to exchange a shirt?"
        if col_p4.button("🚨 Received torn dress!"):
            st.session_state.chat_input_val = "I received a torn dress in my parcel!"

        query_input = st.text_input(
            "Enter customer query",
            value=st.session_state.get("chat_input_val", ""),
            placeholder="e.g. Do you ship to Dubai?",
            key="query_text_input",
        )

        if st.button("Send Query", type="primary", key="send_chat_query_btn"):
            if query_input:
                result = engine.classify_query(query_input)
                st.session_state.last_chat_result = result

        res = st.session_state.get("last_chat_result")
        if res:
            st.divider()
            res_col1, res_col2 = st.columns([2, 1])
            with res_col1:
                st.markdown("### Assistant Response")
                if res["escalated"]:
                    st.warning(f"🚨 **Escalated to Human Agent**\n\n{res['response']}")
                    st.caption(f"**Escalation Reason:** {res['escalation_reason']}")
                else:
                    st.success(f"🤖 **Bot Response:**\n\n{res['response']}")

            with res_col2:
                st.markdown("### Intent Diagnostics")
                st.metric("Detected Intent", res["intent"])
                st.metric("Confidence Score", f"{res['confidence']:.2f}")
                st.write(f"**Category:** {res['category']}")
                if res.get("matched_pattern"):
                    st.caption(f"**Matched Pattern:** {res['matched_pattern']}")

    with tab2:
        st.subheader("10+ Customer Query Benchmark & Accuracy Test Log")
        st.caption("Runs automated accuracy evaluation over 12 standard customer test queries mapped for ThreadStyle Co.")

        if st.button("Run Accuracy Evaluation Suite", type="primary", key="run_benchmark_btn"):
            benchmark_res = engine.run_benchmark()
            st.session_state.benchmark_res = benchmark_res

        b_res = st.session_state.get("benchmark_res") or engine.run_benchmark()

        m1, m2, m3 = st.columns(3)
        m1.metric("Total Test Queries", b_res["total_queries"])
        m2.metric("Passed Queries", b_res["passed_queries"])
        m3.metric("Classification Accuracy", f"{b_res['accuracy_percent']}%")

        df = pd.DataFrame(b_res["test_results"])
        st.dataframe(
            df,
            column_config={
                "query": st.column_config.TextColumn("Customer Query", width="large"),
                "expected": st.column_config.TextColumn("Expected Intent"),
                "predicted": st.column_config.TextColumn("Predicted Intent"),
                "confidence": st.column_config.NumberColumn("Confidence", format="%.2f"),
                "escalated": st.column_config.CheckboxColumn("Escalated?"),
                "passed": st.column_config.CheckboxColumn("Passed?"),
            },
            use_container_width=True,
            hide_index=True,
        )

    with tab3:
        st.subheader("Conversation Flow & Human Escalation Rules")
        st.markdown(
            """
            ```mermaid
            graph TD
                A[Customer Inquiry] --> B[TF-IDF & Intent Matching]
                B -->|Confidence >= 0.25| C{Requires Escalation?}
                B -->|Confidence < 0.25| D[Trigger Low-Confidence Escalation]
                C -->|No| E[Return Auto FAQ Answer]
                C -->|Yes: Damaged Item / High Frustration| F[Assign Support Ticket & Escalate to Human Agent]
                D --> F
            ```
            """
        )
        st.subheader("Mapped Intent Knowledge Base")
        kb_df = pd.DataFrame([
            {
                "Category": item["category"],
                "Intent": item["intent"],
                "Sample Pattern": item["patterns"][0],
                "Auto Response": item["response"],
                "Auto Escalation": "Yes" if item["requires_escalation"] else "No"
            }
            for item in engine.knowledge_base
        ])
        st.dataframe(kb_df, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("Audit & Documentation Export")
        st.caption("Download full JSON audit report of the chatbot performance and intent benchmark.")
        json_report = engine.export_test_report_json()
        st.download_button(
            "Download Benchmark Audit JSON",
            data=json_report,
            file_name="customer_support_chatbot_benchmark.json",
            mime="application/json",
        )
