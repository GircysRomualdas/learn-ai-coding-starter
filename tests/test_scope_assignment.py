"""Assignment must resolve to the nearest enclosing block scope."""

from sloperator.runner import run_source


def test_nested_block_assignment_targets_nearest_enclosing_scope():
    source = """slop score = 1✨
{
    slop score = 2✨
    {
        score = 3✨
    }
    hallucinate(score)✨
}
hallucinate(score)✨"""
    result = run_source(source)

    assert result.stdout == "3\n1\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_sibling_blocks_do_not_share_an_assignment_target():
    source = """slop score = 1✨
{
    slop score = 2✨
    score = 20✨
}
{
    score = 30✨
}
hallucinate(score)✨
"""
    result = run_source(source)

    assert result.stdout == "30\n"
    assert result.stderr == ""
    assert result.exit_code == 0
