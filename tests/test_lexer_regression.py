import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


# Regression: the generic "unexpected character" fallback in the scanner
# (scanner.py) had no test coverage, so a change that routed an unknown
# character elsewhere or dropped the error would go unnoticed.
@pytest.mark.parametrize("char", ["@", "#", "%", "$", ".", ":"])
def test_unexpected_character_reports_lexical_error(char: str):
    source = f"x {char} y"
    with pytest.raises(LexicalError) as info:
        tokenize(source)

    assert info.value.line == 1
    assert info.value.message == f"unexpected character '{char}'"
    assert str(info.value) == (f"SlopLang lexical error at line 1: unexpected character '{char}'")


# Regression: consuming a comment's terminating newline did not advance the
# scanner's line counter, so anything after a comment was attributed to the
# comment's line.
@pytest.mark.parametrize(
    ("source", "line"),
    [
        ("— a comment\n@", 2),
        ("— a comment\r\n@", 2),
        ("— a comment\n— another\n@", 3),
    ],
)
def test_line_after_comment_is_counted(source: str, line: int):
    with pytest.raises(LexicalError) as info:
        tokenize(source)

    assert info.value.line == line
    assert info.value.message == "unexpected character '@'"
