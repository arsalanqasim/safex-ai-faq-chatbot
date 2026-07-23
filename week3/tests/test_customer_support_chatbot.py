"""Tests for Arsalan Qasim's AI Customer Support Chatbot engine."""

from src.modules.customer_support_chatbot.engine import CustomerSupportEngine


def test_intent_classification_order_tracking():
    """Verify order tracking intent is identified correctly."""
    engine = CustomerSupportEngine()
    res = engine.classify_query("Where is my order #TS-98421?")
    assert res["intent"] == "Track Order Status"
    assert res["confidence"] > 0.3
    assert not res["escalated"]


def test_intent_classification_sizing():
    """Verify size guide intent returns sizing recommendation."""
    engine = CustomerSupportEngine()
    res = engine.classify_query("What size shirt for chest size 40?")
    assert res["intent"] == "Sizing & Fit Guide"
    assert "Medium" in res["response"] or "Large" in res["response"]


def test_escalation_damaged_goods():
    """Verify damaged item query triggers automatic human escalation."""
    engine = CustomerSupportEngine()
    res = engine.classify_query("I received a torn and damaged dress!")
    assert res["escalated"] is True
    assert "escalation" in res["response"].lower() or "agent" in res["response"].lower()


def test_benchmark_suite_accuracy():
    """Verify engine achieves high accuracy on 12-query test suite."""
    engine = CustomerSupportEngine()
    b_res = engine.run_benchmark()
    assert b_res["total_queries"] == 12
    assert b_res["accuracy_percent"] >= 90.0
