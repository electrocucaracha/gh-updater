# CLI reference

```text
gh-updater [OPTIONS] [REPOSITORY]
```

| Argument                      | Default                                           | Meaning                                                                                     |
| ----------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `repository`                  | Current directory                                 | Directory to scan; it need not contain Git metadata                                         |
| `--dry-run`                   | Off                                               | Resolve and report updates without writing files                                            |
| `--exclude OWNER/REPO[/PATH]` | None                                              | Skip an upstream repository or exact action path; repeat as needed                          |
| `--log-level LEVEL`           | `WARNING`                                         | Diagnostic verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL` (case-insensitive) |
| `--workers N`                 | `min(32, CPUs + 4)`, capped at the upstream count | Number of parallel lookup workers (at least 1); also read from `GH_UPDATER_WORKERS`         |
| `-h`, `--help`                | Off                                               | Display usage and exit                                                                      |

`python -m gh_updater` accepts the same options.

## Examples

Install as an isolated tool with `pipx install /path/to/gh-updater`.
Target a repository from elsewhere,
exclude actions,
or enable diagnostic logs:

```sh
gh-updater /path/to/repository --exclude austenstone/copilot-cli
gh-updater --exclude actions/checkout --exclude owner/repo/sub-action
python -m gh_updater --dry-run
gh-updater --dry-run --log-level debug
```

## Discovery and formatting

The CLI scans `.yml` and `.yaml` files under `.github`,
plus `action.yml` and `action.yaml` files throughout the repository.
Symlinks and Git, virtualenv, tox, and Node dependency directories are skipped.

It updates job-level reusable workflows and step-level remote actions,
including subpaths such as `owner/repo/path@v1`.
Local actions, Docker references, shell examples,
and other strings containing `uses:` are left unchanged.

Edits preserve quotes, anchors, human comments, file modes,
and CRLF line endings.
Existing version comments are refreshed.
Flow-style mappings receive SHA replacements without version comments,
because inline comments would break those mappings.
Multiline `uses` scalars are rejected;
convert them to single-line values.

## Version resolution

The highest stable numeric Git tag wins,
including upgrades across major versions.
Accepted tags have an optional `v` or `V` prefix
and one or more dot-separated numeric components.
Prerelease tags are not candidates.
Annotated tags are dereferenced to commit SHAs.

For repositories without numeric tags,
the current branch or named tag is resolved.
A SHA pin needs a branch/tag hint as the first token of its inline comment,
such as `# main`.
Without a resolvable hint,
the command fails explicitly.

The Git executable must be on `PATH`.
Existing Git credentials handle private repositories;
the CLI does not read a GitHub token argument
or configure authentication.
Each repository lookup has a 60-second timeout.
After discovering how many upstream repositories are referenced,
the CLI splits them round-robin across `--workers` workers.
Each worker resolves its share sequentially in its own thread,
with one lookup per upstream repository per invocation.

## Output and exit status

Changed references are reported as:

```text
.github/workflows/ci.yml:12: owner/action@old-ref -> commit-sha # version
```

A final line reports the number of changed and scanned YAML files.
Dry-run output starts with `Would update`.
Update details and the summary go to stdout.
Progress messages go to stderr during scanning,
upstream lookups, file checks, and writes.
When stderr is a terminal,
lookup progress is drawn as one bar per worker and redrawn in place:

```text
Resolving upstreams [3/5]:
  Worker  1: [#############-------] 2/3 actions/checkout
  Worker  2: [##########----------] 1/2 actions/setup-python
```

Otherwise, such as in CI logs,
each finished lookup prints one `Resolved [n/total] owner/repo (worker N)` line.
Dry runs do not write files or show write progress.
Diagnostic logs also go to stderr and respect `--log-level`;
progress is shown independently of the log level.

```sh
python -m gh_updater --dry-run --log-level debug
```

- `0`: Successful execution,
  including a dry run with available updates.
- `1`: YAML, Git lookup, encoding, or filesystem failure.
- `2`: Invalid command-line arguments,
  including a nonexistent repository directory.

All references are resolved before writes begin.
Writes replace each file atomically,
but they are not a repository-wide transaction:
a filesystem failure can leave earlier files updated.
Flow-style mappings receive SHA replacements without version comments.
Multiline `uses` values are rejected.
