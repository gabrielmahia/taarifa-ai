"""Smoke test: app.py is valid Python. (The previous test imported modules and then asserted True, so it could not fail.)"""
import ast
from pathlib import Path


def test_app_parses():
    ast.parse((Path(__file__).resolve().parents[1] / "app.py").read_text(encoding="utf-8"))
