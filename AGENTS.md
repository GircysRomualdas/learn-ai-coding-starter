# AGENTS.md

Sloperator is a Python 3.13 tree-walking interpreter for SlopLang. Run commands from the repo root with `uv`.

## Project layout

- `sloperator.py` — CLI entrypoint.
- `sloperator/lexer/` — source text to tokens.
- `sloperator/parser/` — tokens to the AST via a recursive-descent parser.
- `sloperator/evaluator/` — AST evaluation, values, and environments.
- `sloperator/runner.py` — tokenize/parse/run pipeline and error handling.
- `tests/` — pytest suite; `examples/` — runnable `.slop` programs.
- `playground/` — local web editor; start it with `uv run playground/server.py` (port 8080 by default).

## Validation

Run all four from the repo root:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

## Regression tests

Add a regression test whenever you fix a bug or change observable language or parser behavior. Cover the specific failing case, including exact stdout, stderr, and exit status for errors. Run a focused test with `uv run pytest tests/test_file.py::test_name`.

Run comparison regression tests with `uv run pytest tests/test_comparisons.py`; add future comparison/precedence cases there.

New `examples/*.slop` files are automatically picked up by `tests/test_examples.py`; each must exit 0 and print non-empty stdout.

## Language behavior

See [docs/spec.md](docs/spec.md) for SlopLang syntax, semantics, grammar, operators, and error messages. Update the spec alongside behavior changes.
