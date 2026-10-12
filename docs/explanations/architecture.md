# Architecture and technology choices

## Application

The application uses Python 3.10+,
a `src` package layout,
Click,
pathlib,
subprocess,
and PyYAML.
The installed entry point calls `gh_updater.cli.main`;
module execution uses the same function.

The `files` module discovers workflow YAML under `.github`
and composite action metadata throughout the target directory.
The `actions` module uses PyYAML to identify job and step `uses` scalars
and their source positions.
Edits apply to those spans rather than serializing the entire YAML document.
This keeps comments, quotes, anchors, and line endings intact.

The `resolver` module runs `git ls-remote` with an argument list,
never through a shell.
Results are cached per upstream repository for one command invocation.
After parsing all files,
the upstreams are split round-robin into one bucket per worker,
and a bounded standard-library thread pool resolves the buckets in parallel.
The `progress` module renders one progress bar per worker on interactive terminals
and plain lines otherwise.
Workers return their results,
and only the main thread populates the resolver cache,
while `files` handles discovery and atomic writes.
The `cli` module coordinates parsing, resolution, and writes.
Resolution selects numeric tags
and dereferences annotated tags to immutable commits.
The command stages all edits in memory before writing.
Each changed file is replaced atomically in its original directory.
Click sends progress to stderr and update reports to stdout.
Standard-library logging supplies diagnostics,
with verbosity controlled by `--log-level`.

## Reuse from ai-prepare-commit-msg

The reference project was reviewed at commit
[`193efa7`](https://github.com/electrocucaracha/ai-prepare-commit-msg/tree/193efa78e031763174041cc46eddb7bbee7bcfa8).

| Area | Adaptation |
| --- | --- |
| CLI | Click provides option parsing, help, and progress output |
| Packaging | Hatchling builds the existing src-layout package |
| Development | uv dependency groups and a committed lockfile |
| Checks | tox commands behind familiar Make targets |
| Tests | pytest collects existing unittest cases; pytest-cov enforces 80% coverage |
| Python style | Ruff handles lint, imports, and formatting instead of overlapping Black/isort/Ruff passes |
| Hooks | Local pre-commit hooks reuse locked tools without AI commit generation |
| Copilot | Scoped Python, quality-gate, and Markdown instruction files |
| CI | Separate test and lint workflows with pinned actions and manual execution |
| Documentation | Contributor guide, workflow inventory, and task/reference/explanation navigation |

Runtime AI providers, GitPython, and provider plugins are not reused:
this CLI does not generate text with an LLM
and its standard-library interfaces already cover those needs.
Container-based Super-Linter and Node/Go tooling are also unnecessary here.
Ruff and yamllint run locally and in CI with the same configuration.

The reference's mutation and BDD environments are not introduced
because the current integration tests already exercise the CLI update flow.
Its release, update-PR, and AI improvement workflows require additional policy,
permissions, or secrets,
so this project does not enable them implicitly.
The workflow inventory documents only the two implemented validation workflows.

## Review of the Bash implementations

The action-update sections in
[ai-prepare-commit-msg](https://github.com/electrocucaracha/ai-prepare-commit-msg/blob/main/ci/update_versions.sh),
[kubevirt-actions-runner](https://github.com/electrocucaracha/kubevirt-actions-runner/blob/master/ci/update_versions.sh),
[krd](https://github.com/electrocucaracha/krd/blob/master/ci/update_versions.sh),
and [ai-changelog](https://github.com/electrocucaracha/ai-changelog/blob/main/ci/update_versions.sh)
share useful principles:
numeric version sorting, annotated-tag dereferencing,
commit pinning, and exclusions for incompatible actions.

This CLI addresses their main portability and correctness limitations:

1. YAML-aware edits avoid the broad `grep`/`sed` substitutions
   that can lose quotes or comments and match shell examples.
2. Action subpaths are resolved against their parent `owner/repo`.
3. Failed resolutions stop updates instead of substituting an empty value.
4. Python avoids platform differences in GNU `sort -V` and `sed -i`.
5. Reusable-workflow hints are resolved per occurrence,
   so different refs are not conflated.
6. Explicit exclusions replace repository-specific hardcoded policies.

The scripts also update unrelated dependencies and tools.
Those operations are outside this application's scope.
