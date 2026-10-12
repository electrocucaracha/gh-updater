# GitHub Actions Updater

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub Super-Linter](https://github.com/electrocucaracha/gh-updater/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

<!-- markdown-link-check-disable-next-line -->

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![visitors](https://visitor-badge.laobi.icu/badge?page_id=electrocucaracha.gh-updater)
[![Scc Code Badge](https://sloc.xyz/github/electrocucaracha/gh-updater?category=code)](https://github.com/boyter/scc/)
[![Scc COCOMO Badge](https://sloc.xyz/github/electrocucaracha/gh-updater?category=cocomo)](https://github.com/boyter/scc/)

Pin GitHub Actions to full commit SHAs,
not mutable version tags,
and keep those pins up to date without repository-specific scripts.
gh-updater finds remote action references,
updates them to the latest stable version's commit SHA,
and leaves the changes for you to review.

## Why commit SHAs instead of version tags?

A reference such as `owner/action@v1` identifies a tag,
not a fixed revision of the action.
Ordinary Git tags can be moved to another commit:
the same workflow can execute different code on its next run,
even though nothing changed in your repository.
That movement may be an intentional release update,
or malicious tampering after an upstream repository is compromised.
An exact-looking tag such as `v1.2.3` is not inherently immutable either.

GitHub's [secure use guidance](https://docs.github.com/en/actions/reference/security/secure-use#using-third-party-actions)
recommends full-length commit SHA pins to mitigate this risk
and warns that an attacker with repository access can move or delete tags.
GitHub also documents
[how action maintainers move version tags](https://docs.github.com/en/actions/how-tos/create-and-publish-actions/using-immutable-releases-and-tags-to-manage-your-actions-releases).
Tags associated with GitHub immutable releases are an exception,
but consumers cannot assume every upstream uses that protection.

gh-updater resolves the selected upstream version to its full 40-character commit SHA
and writes that SHA into the `uses` reference.
The version remains in a readable comment where YAML syntax permits;
GitHub Actions executes the pinned commit,
not the comment's tag.
Moving the tag afterward does not change the commit selected by that reference.
You can review and commit each update explicitly,
rather than accepting upstream tag changes implicitly.

**Pinning fixes the selected revision; it does not prove the code is safe.**
gh-updater resolves the tags advertised by the upstream at update time;
it does not authenticate releases or detect a tag that was already compromised.
Review the resolved commit and action source before accepting an update.
An action's runtime downloads and external dependencies also need their own controls.

## How it works

Run the CLI from your repository to update workflows,
reusable workflows,
and composite actions.
It preserves YAML formatting and comments,
and leaves local actions and Docker references unchanged.

For upstreams with stable numeric tags,
it selects the highest version and dereferences annotated tags to commits.
For upstreams without those tags,
it resolves a branch or named tag instead;
see [version resolution](docs/references/cli.md#version-resolution) for details.

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
