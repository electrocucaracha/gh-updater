# Contributing to gh-updater

## Set up

Install Git, Python 3.10 or newer,
and [uv](https://docs.astral.sh/uv/).
From this project's root directory,
install the locked development environment:

```sh
uv sync --locked --all-groups
```

If this directory is a Git checkout,
optionally install the local quality hooks:

```sh
uv run pre-commit install
```

The hooks use the tools from the development environment.
There is no commit-message generation hook.

## Make changes

Application code lives in `src/gh_updater/`,
tests in `tests/`,
and user documentation in `docs/`.
Keep runtime dependencies small,
preserve existing workflow formatting,
and add regression tests when changing behavior.
Use semantic line breaks in Markdown.

## Validate

| Command         | Purpose                                              |
| --------------- | ---------------------------------------------------- |
| `make setup`    | Install all locked dependency groups                 |
| `make fmt`      | Format Python and sort imports with Ruff             |
| `make lint`     | Check Python style and repository YAML               |
| `make test`     | Run pytest and the installed CLI help command        |
| `make coverage` | Require at least 80% line coverage                   |
| `make build`    | Build a wheel and source distribution with Hatchling |

Make delegates to uv and the tox environments in `pyproject.toml`.
The lockfile pins the uv development environment;
tox installs its isolated environments from the dependency-group version ranges.
No container, Node.js installation, or global package installation is needed.
Without Make,
run the corresponding commands directly:

```sh
uv run --frozen tox -e fmt,lint,test,coverage
uv build
```

Select a test while iterating:

```sh
uv run --frozen tox -e test -- tests/test_cli.py -k no_tags
```

The existing unittest cases are collected by pytest without modification.
Keep automated tests offline;
mock `git ls-remote` rather than relying on GitHub state or credentials.
The unittest runner is also supported:

```sh
uv run python -m unittest discover -s tests -v
```

## Dependencies and pull requests

After editing dependencies in `pyproject.toml`,
run `uv lock` and commit the updated `uv.lock` with the manifest.
Use `uv lock --upgrade` only for deliberate dependency upgrades.
Do not add environment-specific index URLs or credentials to project configuration.

Run formatting, lint, tests, coverage, and the build before submitting a pull request.
Describe the behavior change and the checks you ran.
Update the [workflow inventory](.github/workflows/README.md)
when changing CI,
and the [CLI reference](docs/references/cli.md)
when changing options or exit codes.
