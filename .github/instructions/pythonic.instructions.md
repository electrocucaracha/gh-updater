---
description: "Python implementation and test conventions for gh-updater."
applyTo: "**/*.py"
---

# Python conventions

Use Python 3.10-compatible syntax and keep application code in `src/gh_updater/`.
Prefer the standard library unless an existing dependency is needed.
Use pathlib for paths and type annotations for public interfaces.
Keep stdout update output separate from stderr progress and diagnostics.
Use Click for CLI parsing and logging for diagnostic verbosity.

Use Ruff for formatting, import sorting, and linting.
Run `make fmt`, `make lint`, and `make test` after Python changes.
Run `make coverage` when changing discovery, parsing, resolution, or file writes.
Report failures explicitly rather than bypassing checks.

Keep tests in `tests/test_*.py`.
Pytest runs the existing unittest tests;
do not rewrite working tests merely to change frameworks.
Mock Git lookups in automated tests so tests need no network or credentials.

Preserve YAML source formatting, human comments, quotes, and line endings.
Resolve every upstream before writing any file.
Never introduce shell execution, token logging, or implicit credential setup.
See [contributor guidance](../../CONTRIBUTING.md)
and [architecture](../../docs/explanations/architecture.md).
