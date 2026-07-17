# AI Email Assistant Prototype - Streamlit UI
# Assigned Developer: Shahidullah (Group Member)
# For SafeX Solutions Business Automation Research
#
# Renders the customer-facing / demo Streamlit interface for the AI Email
# Assistant module. All heavy lifting (analysis + reply generation) lives in
# ``engine.py``; this file is purely presentational.

from __future__ import annotations

import json
from typing import Dict, Optional, Tuple

import streamlit as st
import streamlit.components.v1 as components

from src.modules.email_assistant.engine import EmailAssistantEngine

# ------------------------------------------------------------------------
# Static display config
# ------------------------------------------------------------------------

#: Emoji badge shown next to each detected priority level.
_PRIORITY_BADGE: Dict[str, str] = {
    "High": "🔴 High Priority",
    "Medium": "🟠 Medium Priority",
    "Low": "🟢 Low Priority",
}

#: Emoji badge shown next to each detected sentiment.
_SENTIMENT_BADGE: Dict[str, str] = {
    "Positive": "😊 Positive",
    "Neutral": "😐 Neutral",
    "Negative": "☹️ Negative",
}

#: Emoji shown next to each detected category.
_CATEGORY_ICON: Dict[str, str] = {
    "Order Status": "📦",
    "Refund": "💵",
    "Complaint": "⚠️",
    "Replacement": "🔄",
    "Shipping": "🚚",
    "Payment": "💳",
    "Product Inquiry": "🔎",
    "General Inquiry": "✉️",
}

#: Reply tone options offered to the user.
_REPLY_STYLES = ["Professional", "Friendly", "Formal", "Empathetic"]

#: Reply language options offered to the user (AI mode only).
_LANGUAGES = ["English", "Urdu", "Spanish", "French"]


def _render_header() -> None:
    """Render the clean, modern SaaS-style header."""
    st.markdown(
        """
        <div style="text-align:center; padding: 18px 10px 22px 10px;">
            <div style="font-size:30px; font-weight:700; letter-spacing:-0.02em;">
                📧 AI Email Assistant
            </div>
            <div style="font-size:14.5px; color:var(--text-secondary,#8B949E); margin-top:6px;">
                Generate intelligent, professional customer support email replies using AI.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")


def _render_input_section() -> Tuple[str, str, str, Optional[str]]:
    """Render the customer-email input, reply style/language, and API key.

    Returns:
        A tuple of (email_text, style, language, api_key_or_none).
    """
    st.markdown("**Customer Email**")
    email = st.text_area(
        "Customer Email",
        height=220,
        placeholder=(
            "Example: Hi, I ordered a wireless keyboard last week and it "
            "arrived damaged. I need a replacement urgently, please advise."
        ),
        label_visibility="collapsed",
    )

    col_a, col_b = st.columns(2)
    with col_a:
        style = st.selectbox("Reply Style", _REPLY_STYLES, index=0)
    with col_b:
        language = st.selectbox("Language", _LANGUAGES, index=0)

    api_key: Optional[str] = None
    with st.expander("⚙️ Advanced: Use your own Gemini API key", expanded=False):
        key_input = st.text_input(
            "Gemini API Key (Optional)",
            type="password",
            placeholder="AIza...",
            help=(
                "Provide a Gemini API key to generate AI-written replies. "
                "Leave empty to use built-in professional templates instead."
            ),
        )
        api_key = key_input.strip() if key_input else None
        if api_key:
            st.success("Gemini AI mode enabled ✨", icon="✅")
        else:
            st.caption("💡 No key provided — smart template replies will be used.")

    return email, style, language, api_key


def _render_analysis(result: dict) -> None:
    """Render the Analysis section: category, priority, sentiment, confidence."""
    st.markdown("---")
    st.subheader("📊 Analysis")

    category = result["category"]
    priority = result["priority"]
    sentiment = result["sentiment"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        icon = _CATEGORY_ICON.get(category, "✉️")
        st.metric("Category", f"{icon} {category}")
    with c2:
        st.metric("Priority", _PRIORITY_BADGE.get(priority, priority))
    with c3:
        st.metric("Sentiment", _SENTIMENT_BADGE.get(sentiment, sentiment))
    with c4:
        st.metric("Confidence", f"{result['confidence']:.0f}%")

    with st.expander("🔍 More Details (subject line, summary, keywords)", expanded=False):
        st.markdown(f"**Suggested Subject Line:** {result['suggested_subject']}")
        st.markdown(f"**Issue Summary:** {result['summary']}")
        if result["keywords"]:
            keyword_chips = " ".join(f"`{kw}`" for kw in result["keywords"])
            st.markdown(f"**Detected Keywords:** {keyword_chips}")
        else:
            st.markdown("**Detected Keywords:** _None detected_")


def _render_copy_button(text: str, key: str = "copy_reply_btn") -> None:
    """Render a small 'Copy Reply' button that copies text to the clipboard.

    The reply text is passed through a ``<script>`` block as a JSON-encoded
    JS variable (never inlined into an HTML attribute), so quotes,
    newlines, or any other special characters in the reply can never break
    the surrounding markup.
    """
    safe_text = json.dumps(text)
    button_id = f"btn-{key}"
    components.html(
        f"""
        <div style="margin-top:6px;">
            <button id="{button_id}"
                style="background:#0969DA; color:#fff; border:none;
                       padding:8px 18px; border-radius:6px; cursor:pointer;
                       font-size:13.5px; font-weight:600; font-family:inherit;">
                📋 Copy Reply
            </button>
        </div>
        <script>
            (function() {{
                const replyText = {safe_text};
                const btn = document.getElementById("{button_id}");
                btn.addEventListener("click", function() {{
                    navigator.clipboard.writeText(replyText).then(function() {{
                        const original = btn.innerText;
                        btn.innerText = "✅ Copied!";
                        setTimeout(function() {{ btn.innerText = original; }}, 1500);
                    }});
                }});
            }})();
        </script>
        """,
        height=50,
    )


def _render_reply_section(result: dict) -> None:
    """Render the generated reply, copy button, metrics, and technical details."""
    st.markdown("---")
    st.subheader("✉️ AI Generated Reply")

    if result.get("used_ai"):
        st.success("Reply generated using the Gemini AI model.", icon="🤖")
    else:
        st.info("Reply generated using a professional built-in template.", icon="📋")
        if result.get("api_note"):
            st.warning(result["api_note"], icon="⚠️")

    st.text_area(
        "Reply",
        value=result["reply"],
        height=260,
        label_visibility="collapsed",
    )

    _render_copy_button(result["reply"])

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Character Count", result["reply_char_count"])
    with c2:
        st.metric("Word Count", result["reply_word_count"])

    with st.expander("🛠️ Technical Details", expanded=False):
        st.json(
            {
                "category": result["category"],
                "priority": result["priority"],
                "sentiment": result["sentiment"],
                "confidence_score": result["confidence"],
                "keywords": result["keywords"],
                "ai_reply_used": bool(result.get("used_ai")),
                "reply_char_count": result["reply_char_count"],
                "reply_word_count": result["reply_word_count"],
            }
        )


def render_ui() -> None:
    """Render the Streamlit frontend tab for the AI Email Assistant Prototype.

    This is the single entry point invoked by the SafeX Suite host
    application (``app.py``) via ``importlib`` — its signature must remain
    ``render_ui() -> None`` to stay compatible with the module registry.
    """
    _render_header()
    email, style, language, api_key = _render_input_section()

    generate_clicked = st.button(
        "🚀 Generate Reply", use_container_width=True, type="primary"
    )

    if not generate_clicked:
        return

    if not email or not email.strip():
        st.error("Please enter a customer email before generating a reply.", icon="🚫")
        return

    with st.spinner("Analyzing email and drafting a reply..."):
        try:
            engine = EmailAssistantEngine(api_key=api_key)
            result = engine.process_email(email, style=style, language=language)
        except ValueError as exc:
            st.error(f"Invalid input: {exc}", icon="🚫")
            return
        except Exception as exc:  # noqa: BLE001 - keep the demo resilient
            st.error(f"Something went wrong while processing the email: {exc}", icon="❌")
            return

    st.success("Email analyzed and reply generated successfully!", icon="✅")

    _render_analysis(result)
    _render_reply_section(result)