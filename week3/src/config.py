"""Configuration constants and path resolvers for Week 3 workspace."""

from pathlib import Path

WEEK3_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = WEEK3_DIR / "outputs"
DOCS_DIR = WEEK3_DIR / "docs"

OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
