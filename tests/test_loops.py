from sloperator.runner import run_source


def test_while_loop_with_false_condition_does_not_run():
    result = run_source(
        """\
ralph ❌ {
    hallucinate(“never”)✨
}
"""
    )

    assert result.stdout == ""
    assert result.stderr == ""
    assert result.exit_code == 0
