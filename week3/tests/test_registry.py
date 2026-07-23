"""Tests for Week 3 Module Registry consistency."""

import importlib
from src.modules.registry import MODULE_REGISTRY


def test_week3_registry_keys():
    """Verify registry contains all 9 group members for Week 3."""
    assert "week3" in MODULE_REGISTRY
    week3_modules = MODULE_REGISTRY["week3"]
    assert len(week3_modules) == 9

    expected_keys = [
        "customer_support_chatbot",
        "email_auto_reply",
        "meeting_summarizer",
        "report_generation_agent",
        "social_media_scheduler",
        "lead_qualification",
        "resume_interview_assistant",
        "doc_knowledge_assistant",
        "proposal_invoice_generator"
    ]
    for key in expected_keys:
        assert key in week3_modules, f"Missing key: {key}"


def test_week3_modules_importable():
    """Verify all import_path definitions in registry resolve to valid python modules."""
    for key, item in MODULE_REGISTRY["week3"].items():
        import_path = item["import_path"]
        mod = importlib.import_module(import_path)
        assert hasattr(mod, "render_ui"), f"Module {import_path} missing render_ui function"
