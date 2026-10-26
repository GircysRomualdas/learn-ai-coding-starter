# AGENTS.md

Sloperator is a tree-walking interpreter for SlopLang (the Boot.dev "Learn AI Coding" starter). Python 3.13, managed by `uv`; no runtime dependencies.

## Commands

Run these from the repo root; use `uv run`, not a bare `python`/`pytest`, since the package is only importable from the project root.

- Run a program: `uv run sloperator.py path/to/program.slop`
- Parse without executing: `uv run sloperator.py --check path/to/program.slop`
- One test: `uv run pytest tests/test_evaluator.py::test_arithmetic`
- Full validation (all four must pass): `uv run pytest && uv run ruff format --check && uv run ruff check && uv run ty check`
- Apply automatic fixes: `uv run ruff format` and `uv run ruff check --fix`
- Playground: `uv run playground/server.py [port]` (default 8080; appends to `logs/runs.log`).

The repo's `validate` skill covers pytest/format/lint but not `ty check`; include the typecheck when validating.

## Pipeline

`sloperator.py` (CLI) -> `sloperator/runner.py` (tokenize -> parse -> interpret) -> `lexer/`, `parser/`, `evaluator/`.

- `runner.run_program` raises Python's recursion limit to 20,000; `run_source` is the test helper returning `RunResult(stdout, stderr, exit_code)`.
- Errors are `SlopError` subclasses in `sloperator/errors.py`, always formatted as `SlopLang <lexical|syntax|runtime> error at line N: ...`. CLI exit codes: 0 success, 1 SlopLang error, 2 usage/file error. Python tracebacks must never escape.
- The evaluator uses parent-linked `Environment`s; each function call's parent is globals, so there are no closures. `ship` unwinds via the `ShipSignal` exception, and `MAX_CALL_DEPTH` is 500.
- AST nodes are frozen dataclasses in `sloperator/parser/ast.py`; the parser is recursive descent and enforces top-level-only `clanker` and `ship`-inside-`clanker`.

## SlopLang and tests

- Source uses non-ASCII syntax: smart quotes `“ ”`, em dash `—` comments, `✨` statements, `✅`/`❌` booleans. Keep these exact in code, tests, examples, and docs; straight quotes and semicolons are deliberately rejected with helpful lexical errors.
- `tests/test_examples.py` automatically parametrizes every `examples/*.slop`; each example must exit 0 and print non-empty stdout. Add examples there rather than creating a separate fixture.
- Many tests assert exact diagnostics or exact stdout, including emoji; when changing language behavior, update `docs/spec.md` and the matching tests together.
- Booleans must not behave as numbers (Python's `True == 1`). `is_number()` excludes bool, and equality uses type identity. Use these helpers for new operators/builtins.

## Known deviation

- `ralph` executes its body once before checking its condition (`interpreter.py`, `While`), so a loop with a false initial condition still runs once. `docs/spec.md` says the condition is checked before each iteration, and no current test covers zero iterations. Confirm intent before relying on or "fixing" this.

## Commits

- Keep commit messages to a single line; do not add a body.

## OpenCode integration

- `.opencode/plugins/run-slop.ts` registers the `run_slop` tool. It accepts a `.slop` path relative to the project root and runs `uv run --no-active sloperator.py`.
