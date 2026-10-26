import pytest

from sloperator.runner import run_source


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("hallucinate(“” + “slop”)✨", "slop\n"),
        ("hallucinate(“slop” + “”)✨", "slop\n"),
        ("hallucinate(“café” + “✨”)✨", "café✨\n"),
    ],
)
def test_string_concatenation_with_empty_strings_and_emoji(source: str, expected: str):
    result = run_source(source)

    assert result.stdout == expected
    assert result.stderr == ""
    assert result.exit_code == 0
