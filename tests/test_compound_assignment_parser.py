import pytest

from sloperator.errors import SlopSyntaxError
from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Assign, ExprStmt, Literal, VarDecl


def parse_source(source: str):
    return parse(tokenize(source))


def test_plus_equal_is_a_single_token():
    tokens = tokenize("x += 1✨")
    assert [token.type for token in tokens] == [
        TokenType.IDENTIFIER,
        TokenType.PLUS_EQUAL,
        TokenType.NUMBER,
        TokenType.SPARKLES,
        TokenType.EOF,
    ]
    assert tokens[1].lexeme == "+="


def test_plus_alone_is_still_plus():
    tokens = tokenize("1 + 2✨")
    assert [token.type for token in tokens[:3]] == [
        TokenType.NUMBER,
        TokenType.PLUS,
        TokenType.NUMBER,
    ]


def test_compound_assignment_is_a_statement():
    (statement,) = parse_source("x += 1✨")
    assert isinstance(statement, Assign)
    assert statement.name.lexeme == "x"
    assert statement.operator.type is TokenType.PLUS_EQUAL
    assert statement.operator.lexeme == "+="
    assert isinstance(statement.value, Literal) and statement.value.value == 1


def test_compound_assignment_value_can_be_an_expression():
    (statement,) = parse_source("total += (1 + 2) * 3✨")
    assert isinstance(statement, Assign)
    assert statement.operator.type is TokenType.PLUS_EQUAL


def test_compound_assignment_is_parsed_in_blocks():
    (block,) = parse_source("{ x += 1✨ }")
    (statement,) = block.statements
    assert isinstance(statement, Assign) and statement.operator.type is TokenType.PLUS_EQUAL


def test_compound_assignment_is_not_an_expression():
    (statement,) = parse_source("x += 1✨")
    assert not isinstance(statement, ExprStmt)


def test_plus_equal_requires_a_terminator():
    with pytest.raises(SlopSyntaxError) as info:
        parse_source("x += 1")
    assert info.value.line == 1
    assert info.value.message == "expected ✨ after assignment, but reached end of file"


def test_plus_equal_requires_a_value():
    with pytest.raises(SlopSyntaxError) as info:
        parse_source("x += ✨")
    assert info.value.line == 1
    assert info.value.message == "expected an expression, found '✨'"


def test_plus_equal_cannot_target_a_non_identifier():
    with pytest.raises(SlopSyntaxError) as info:
        parse_source("1 += 2✨")
    assert info.value.line == 1
    assert info.value.message == "expected ✨ after expression, found '+='"


def test_declaration_does_not_accept_plus_equal():
    with pytest.raises(SlopSyntaxError) as info:
        parse_source("slop x += 1✨")
    assert info.value.line == 1
    assert info.value.message == (
        "expected '=' after variable name, an initializer is required, found '+='"
    )


def test_compound_assignment_after_a_declaration():
    (declaration, statement) = parse_source("slop x = 1✨ x += 2✨")
    assert isinstance(declaration, VarDecl) and declaration.name.lexeme == "x"
    assert isinstance(statement, Assign) and statement.name.lexeme == "x"
