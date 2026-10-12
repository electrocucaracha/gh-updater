# Available workflows

| Workflow                             | Purpose                                                          | Triggers                            |
| ------------------------------------ | ---------------------------------------------------------------- | ----------------------------------- |
| [on-demand_ci.yml](on-demand_ci.yml) | Tests, 80% coverage gate, CLI smoke test, and distribution build | Push, pull request, manual dispatch |
| [linter.yml](linter.yml)             | Ruff lint, formatting checks, and YAML lint                      | Push, pull request, manual dispatch |

The test matrix covers Python 3.10 through 3.14 on Linux
and Python 3.14 on macOS.
All tests mock Git network requests.
Both workflows install their initial development environment from `uv.lock`,
pin external actions to commit SHAs,
use read-only permissions,
and disable persisted checkout credentials.
Tox then builds isolated environments from the dependency-group version ranges.

These workflows adapt the validation conventions from
[ai-prepare-commit-msg](https://github.com/electrocucaracha/ai-prepare-commit-msg).
They do not require Copilot tokens, Docker, Go, Node.js, or shared release services.
No scheduled updates, publishing, or automatic pull requests are configured.
The updater can maintain these action references with `uv run gh-updater`.

Local equivalents are documented in [CONTRIBUTING.md](../../CONTRIBUTING.md).
