# Sloperator

A SlopLang interpreter and the starter code for Boot.dev's [Learn AI Coding](https://www.boot.dev/courses/learn-ai-coding) course.

## Quick Start

Run a `.slop` program:

```bash
uv run sloperator.py examples/fib.slop
uv run sloperator.py --check path/to/program.slop
```

Validate changes:

```bash
uv run pytest              # tests
uv run ruff format --check # formatting
uv run ruff check          # linting
uv run ty check            # type checking
```

## Language Reference

See [docs/spec.md](docs/spec.md) for the complete SlopLang specification, including syntax, semantics, grammar, and errors. Ready-to-run examples live in [`examples/`](examples/).

## Layout

| Path                    | What it is                                             |
| ----------------------- | ------------------------------------------------------ |
| `sloperator.py`         | Command-line entrypoint                                |
| `sloperator/lexer/`     | Source text to tokens                                  |
| `sloperator/parser/`    | Tokens to AST (`ast.py` holds the node definitions)    |
| `sloperator/evaluator/` | Walks the AST: values, environments, the interpreter   |
| `sloperator/runner.py`  | Runs source through all three stages                   |
| `docs/spec.md`          | The language specification                             |
| `examples/`             | Example programs                                       |
| `tests/`                | Pytest suite                                           |
| `playground/`           | A tiny web server and editor page for running programs |

## Playground

```bash
uv run playground/server.py
```

Then open <http://localhost:8080>.
