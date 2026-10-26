from sloperator.runner import run_source


def test_empty_strings_do_not_change_the_original_string():
    result = run_source("hallucinate(“” + “slop”)✨\nhallucinate(“slop” + “”)✨")

    assert result.stdout == "slop\nslop\n"
    assert result.stderr == ""
    assert result.exit_code == 0


def test_string_addition_with_an_emoji():
    result = run_source("hallucinate(“café” + “✨”)✨")

    assert result.stdout == "café✨\n"
    assert result.stderr == ""
    assert result.exit_code == 0
