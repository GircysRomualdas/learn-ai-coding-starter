from sloperator.runner import check_program


def test_check_program_accepts_valid_syntax():
    assert check_program("slop x = 1✨\nhallucinate(x)✨") is None


def test_check_program_reports_lexical_errors():
    error = check_program('hallucinate("hi")✨')
    assert error is not None
    assert error.kind == "lexical"


def test_check_program_reports_syntax_errors():
    error = check_program("slop x✨")
    assert error is not None
    assert error.kind == "syntax"
    assert str(error) == (
        "SlopLang syntax error at line 1: expected '=' after variable name, "
        "an initializer is required, found '✨'"
    )


def test_check_program_ignores_runtime_errors():
    assert check_program("hallucinate(missing)✨") is None
