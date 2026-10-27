"""Regression: identifiers may contain digits after the first character.

The spec allows `[A-Za-z_][A-Za-z0-9_]*`, but the scanner only consumed
identifier-start characters, so `score2` lexed as `score` followed by the
number `2` and the parser reported a syntax error.
"""

import pytest

from sloperator.lexer import TokenType, tokenize
from sloperator.runner import run_source


def test_identifier_may_end_with_digit():
    tokens = tokenize("score2")
    assert tokens[0].type is TokenType.IDENTIFIER
    assert tokens[0].lexeme == "score2"
    assert tokens[1].type is TokenType.EOF


def test_identifier_may_contain_inner_digit():
    tokens = tokenize("v2_score9x")
    assert tokens[0].type is TokenType.IDENTIFIER
    assert tokens[0].lexeme == "v2_score9x"


def test_identifier_cannot_start_with_digit():
    tokens = tokenize("2score")
    assert [token.type for token in tokens] == [
        TokenType.NUMBER,
        TokenType.IDENTIFIER,
        TokenType.EOF,
    ]
    assert tokens[0].literal == 2
    assert tokens[1].lexeme == "score"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("score", "42\n"),
        ("score2", "42\n"),
        ("score_v2", "42\n"),
        ("sc0re9", "42\n"),
    ],
)
def test_variable_names_with_digits_run(name: str, expected: str):
    source = f"slop {name} = 40✨\n{name} = {name} + 2✨\nhallucinate({name})✨\n"
    result = run_source(source)

    assert result.stdout == expected
    assert result.stderr == ""
    assert result.exit_code == 0


def test_function_and_parameter_names_with_digits_run():
    source = "clanker add2(a1, b2) {\n    ship a1 + b2✨\n}\nhallucinate(add2(40, 2))✨\n"
    result = run_source(source)

    assert result.stdout == "42\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_variable_name_cannot_start_with_digit():
    result = run_source("slop 2score = 5✨\n")

    assert result.stdout == ""
    assert result.stderr == (
        "SlopLang syntax error at line 1: expected a variable name after 'slop', found '2'\n"
    )
    assert result.exit_code == 1
