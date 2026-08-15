"""Repository-only test support for experimental agents and harness modules.

The distributable wheel intentionally contains only ``ace_lab``. These tests also
exercise the research-only ``agents`` and ``harness`` trees, so make the checkout
root explicit instead of accidentally relying on an editable-install layout.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
