---
name: create-test-program
description: Add a SlopLang example program and an exact-output test for a language feature
---

# Create Test Program

Use this skill when asked to add an example and regression coverage for a SlopLang
language feature.

## Workflow

1. Read `docs/spec.md` from the project root. Find the sections that define the
   feature, including its syntax, semantics, operators, and error behavior. Treat
   the spec as the source of truth. If the spec is wrong or incomplete, update it
   alongside the test.
2. Inspect `examples/` and `tests/` for existing coverage. Do not duplicate an
   example or test that already covers the feature.
3. Create a focused example at `examples/<feature>.slop`, where `<feature>` is a
   short, descriptive name such as `string_escapes.slop`. Use real SlopLang
   syntax: smart quotes (`“ ”`), em dash comments (`—`), sparkle terminators
   (`✨`), and no terminator after a block's closing brace.
4. Run the example to capture its exact stdout:

   ```bash
   uv run sloperator.py examples/<feature>.slop
   ```

   The example must exit `0` and print non-empty stdout because
   `tests/test_examples.py` automatically checks every file in `examples/`.
5. Add the example to `tests/test_example_outputs.py`. If the file does not exist,
   create it with this structure and include the new case:

   ```python
   """Exact stdout tests for programs in examples/."""

   from pathlib import Path

   import pytest

   from sloperator.runner import run_source

   EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

   CASES = [
       ("<feature>", "<exact stdout>"),
   ]


   @pytest.mark.parametrize(("name", "expected"), CASES, ids=[name for name, _ in CASES])
   def test_example_output(name: str, expected: str):
       source = (EXAMPLES / f"{name}.slop").read_text(encoding="utf-8")
       result = run_source(source)
       assert result.stdout == expected
       assert result.stderr == ""
       assert result.exit_code == 0
   ```

   If the file already exists, append `("<feature>", "<exact stdout>"),` to `CASES`.
   The expected value must match stdout exactly, including spaces, Unicode, and
   trailing newlines. Do not trim or normalize it.
6. Run the focused test, then validate the project:

   ```bash
   uv run pytest tests/test_example_outputs.py
   uv run pytest
   uv run ruff format
   uv run ruff format --check
   uv run ruff check
   uv run ty check
   ```

   Report failures before proposing fixes.
