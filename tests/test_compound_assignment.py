from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def fails(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


def test_plus_equal_adds_the_evaluated_expression():
    source = """slop n = 2✨
n += 3 * 4✨
hallucinate(n)✨"""
    assert run(source) == "14\n"


def test_plus_equal_accumulates_across_statements():
    source = """slop n = 1✨
n += 2✨
n += 3✨
hallucinate(n)✨"""
    assert run(source) == "6\n"


def test_plus_equal_concatenates_strings():
    assert run("slop s = “a”✨\ns += “b”✨\nhallucinate(s)✨") == "ab\n"


def test_plus_equal_targets_the_nearest_binding():
    source = """slop score = 1✨
{
    slop score = 10✨
    score += 2✨
    hallucinate(score)✨
}
hallucinate(score)✨"""
    assert run(source) == "12\n1\n"


def test_plus_equal_inside_a_loop_body_accumulates_in_the_outer_scope():
    source = """slop total = 0✨
slop i = 0✨
ralph i < 3 {
    total += i✨
    i += 1✨
}
hallucinate(total)✨"""
    assert run(source) == "3\n"


def test_plus_equal_to_a_loadbearing_fails():
    assert fails("loadbearing LIMIT = 1✨\nLIMIT += 1✨") == (
        "SlopLang runtime error at line 2: cannot assign to loadbearing 'LIMIT'"
    )


def test_plus_equal_to_an_undefined_variable_fails():
    assert fails("missing += 1✨") == (
        "SlopLang runtime error at line 1: undefined variable 'missing'"
    )


def test_plus_equal_with_mismatched_types_fails():
    assert fails("slop s = “a”✨\ns += 1✨") == (
        "SlopLang runtime error at line 2: operands of '+=' must both be numbers or both be "
        "strings, got string and number"
    )
