"""Pytest configuration and sys.path setup for Week 3 tests."""

import os
import sys
from pathlib import Path

WEEK3_DIR = Path(__file__).resolve().parent.parent
if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))
