"""Tests for week3 app.py helper functions."""

from src.app import MODULE_REGISTRY


def test_app_registry_available():
    """Verify registry is accessible from main app."""
    assert "week3" in MODULE_REGISTRY
