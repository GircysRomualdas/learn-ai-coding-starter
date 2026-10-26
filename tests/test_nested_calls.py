from sloperator.lexer import tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Call, ExprStmt, FunctionDecl, Literal, Variable
from sloperator.runner import run_source

SOURCE = """clanker add(left, right) {
    ship left + right✨
}
hallucinate(add(1, 2))✨"""


def test_call_as_argument_to_another_call():
    declaration, statement = parse(tokenize(SOURCE))

    assert isinstance(declaration, FunctionDecl)
    assert isinstance(statement, ExprStmt)
    outer_call = statement.expression
    assert isinstance(outer_call, Call)
    assert isinstance(outer_call.callee, Variable)
    assert outer_call.callee.name.lexeme == "hallucinate"

    (inner_call,) = outer_call.arguments
    assert isinstance(inner_call, Call)
    assert isinstance(inner_call.callee, Variable)
    assert inner_call.callee.name.lexeme == "add"

    first, second = inner_call.arguments
    assert isinstance(first, Literal) and first.value == 1
    assert isinstance(second, Literal) and second.value == 2


def test_nested_call_program_prints_result():
    result = run_source(SOURCE)

    assert result.exit_code == 0
    assert result.stdout == "3\n"
    assert result.stderr == ""
