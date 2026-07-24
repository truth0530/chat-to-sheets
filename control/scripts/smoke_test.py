#!/usr/bin/env python3
"""Tool 2 helper — re-export setup smoke (connectivity check)."""
from __future__ import annotations

import runpy
from pathlib import Path

runpy.run_path(
    str(Path(__file__).resolve().parents[2] / "setup" / "scripts" / "smoke_test.py"),
    run_name="__main__",
)
