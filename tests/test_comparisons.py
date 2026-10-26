from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def test_comparison_binds_tighter_than_equality():
    result = run_source("hallucinate(1 < 2 == ✅)✨")

    assert result.stdout == "✅\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_equality_and_comparison_chain_without_manual_grouping():
    assert run("hallucinate(1 == 2 < 3)✨") == "❌\n"
    assert run("hallucinate(2 < 3 == ✅)✨") == "✅\n"
