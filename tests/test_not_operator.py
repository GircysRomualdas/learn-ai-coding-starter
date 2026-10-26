import pytest

from sloperator.runner import run_source


def test_not_flips_booleans_and_double_negation():
    result = run_source("hallucinate(!✅, !❌, !!✅)✨")

    assert result.exit_code == 0
    assert result.stdout == "❌ ✅ ✅\n"
    assert result.stderr == ""


def test_not_works_in_conditions():
    result = run_source("vibe !❌ {\n    hallucinate(“yes”)✨\n}")

    assert result.exit_code == 0
    assert result.stdout == "yes\n"
    assert result.stderr == ""


@pytest.mark.parametrize(
    "source, value_type",
    [
        ("hallucinate(!1)✨", "number"),
        ("hallucinate(!“hello”)✨", "string"),
    ],
)
def test_not_rejects_non_booleans(source, value_type):
    result = run_source(source)

    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr == (
        f"SlopLang runtime error at line 1: operand of unary '!' must be a boolean, "
        f"got {value_type}\n"
    )
