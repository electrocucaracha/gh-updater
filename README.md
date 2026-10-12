# gh-updater

Keep GitHub Actions up to date without maintaining repository-specific scripts.
gh-updater finds remote action references,
updates them to the latest stable version's commit SHA,
and leaves the changes for you to review.

## How it works

Run the CLI from your repository to update workflows,
reusable workflows,
and composite actions.
It preserves YAML formatting and comments,
and leaves local actions and Docker references unchanged.

Preview updates with `--dry-run`
or keep selected actions pinned with `--exclude`.
The tool does not create commits.

## Run

Requires [uv](https://docs.astral.sh/uv/),
Python 3.10+,
and Git on `PATH`.
From the repository you want to update,
run directly from the GitHub source:

```bash
uv run --no-project --with git+https://github.com/electrocucaracha/gh-updater.git gh-updater "$PWD"
```

uv installs gh-updater and its runtime dependencies in a temporary environment.
No local source checkout or global installation is needed.
`--no-project` avoids using the target repository's Python project configuration;
`"$PWD"` explicitly selects the repository to update.

**Review the diff before committing.**
Updates include new major versions,
which may require changes to action inputs or runners.

## Documentation

- [User documentation](docs/index.md)
- [CLI options and behavior](docs/references/cli.md)
- [Contributing and development setup](CONTRIBUTING.md)
- [GitHub Actions workflows](.github/workflows/README.md)
- [Architecture and design decisions](docs/explanations/architecture.md)
