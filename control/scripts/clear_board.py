#!/usr/bin/env python3
"""Tool 2 helper — same clear as setup (shared behavior)."""
from __future__ import annotations

import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parents[2] / "setup" / "scripts" / "clear_board.py"),
    run_name="__main__",
)
