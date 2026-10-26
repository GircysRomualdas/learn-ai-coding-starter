import pytest

from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("1 + 2 * 3", "7"),
        ("2 * 3 + 4", "10"),
        ("3 + 4 * 5 - 6", "17"),
        ("(1 + 2) * 3", "9"),
    ],
)
def test_multiplication_before_addition(expression: str, expected: str):
    assert run(f"hallucinate({expression})✨") == f"{expected}\n"


def test_comparison_binds_tighter_than_equality():
    assert run("hallucinate(1 == 2 < 3)✨") == "❌\n"
    assert run("hallucinate(2 < 3 == ✅)✨") == "✅\n"
