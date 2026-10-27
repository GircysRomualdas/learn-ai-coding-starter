"""Exact stdout tests for programs in examples/."""

from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

CASES = [
    ("arithmetic", "7\n"),
    ("equality", "✅\n❌\n❌\n✅\n❌\n✅\n"),
    ("short-circuit", "❌\n✅\n"),
    ("scope-repro", "3\n1\n"),
]


@pytest.mark.parametrize(("name", "expected"), CASES, ids=[name for name, _ in CASES])
def test_example_output(name: str, expected: str):
    source = (EXAMPLES / f"{name}.slop").read_text(encoding="utf-8")
    result = run_source(source)
    assert result.stdout == expected
    assert result.stderr == ""
    assert result.exit_code == 0
