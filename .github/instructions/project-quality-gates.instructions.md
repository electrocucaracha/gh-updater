---
description: "Validation requirements for project tooling and GitHub workflows."
applyTo: "pyproject.toml,uv.lock,Makefile,.pre-commit-config.yaml,.yamllint.yml,.github/workflows/*.yml"
---

# Project quality gates

Use the commands in [CONTRIBUTING.md](../../CONTRIBUTING.md).
Run `make lint` for tooling or workflow changes.
Run `make test` and `make coverage` when changing dependency or test configuration.
Regenerate `uv.lock` with `uv lock` after dependency changes;
do not edit the lockfile manually.

Pin remote GitHub Actions to full commit SHAs with version comments.
Use read-only workflow permissions and disable persisted checkout credentials.
Keep tests deterministic and avoid live GitHub lookups in CI.
Update the [workflow inventory](../workflows/README.md)
whenever workflow behavior or triggers change.
