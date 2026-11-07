<!-- Markdownlint-disable MD024 -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.10.0] - 2026-11-06

### Added

- Optimized repository size and project organization by ignoring the node_modules directory to prevent tracking of large dependencies and build artifacts. [177a5689](https://github.com/electrocucaracha/gh-updater/commit/177a5689cf71060bfbb3df0d14d725b2312f1ef3)

## [1.9.1] - 2026-11-06

### Changed

- Stabilized the handling of the `.textlintignore` file by ensuring it ends with a newline, thereby preventing issues with tools that expect newline-terminated files and maintaining POSIX compatibility. [d5313f30](https://github.com/electrocucaracha/gh-updater/commit/d5313f3086453d1b08a8e0c4e8a46451002c9d1c)

## [1.9.0] - 2026-11-06

### Added

- Enabled textlint to focus on project source files by excluding virtual environment and test runner artifacts from analysis. [87ce6430](https://github.com/electrocucaracha/gh-updater/commit/87ce6430c80ca2e7ea743f86b04667b82e2c7e9e)

## [1.8.2] - 2026-11-06

### Changed

- Stabilized tox commands to ensure reproducible dependency resolutions and prevent lockfile updates during lint and format targets. [7aa1adce](https://github.com/electrocucaracha/gh-updater/commit/7aa1adce6d1c70f6cfcd656c1b98b903e460c79d)

## [1.8.1] - 2026-11-06

### Changed

- Restricted the tox upper bound in the dev group to <4.62 to prevent compatibility issues with newer versions, and introduced virtualenv as an explicit dev dependency to ensure reliable environment setup and alignment with tox's requirements. [8bfd1436](https://github.com/electrocucaracha/gh-updater/commit/8bfd1436d5e364d7fe76a311a8e433848383c927)

## [1.8.0] - 2026-11-06

### Added

- Enable automatic review requests in pull requests by defining maintainers responsible for all code in the repository, with @electrocucaracha assigned as the default owner for all paths. [d09a22b6](https://github.com/electrocucaracha/gh-updater/commit/d09a22b6c0ae7df0d98d2e6b75d9c13fc7fbc722)

## [1.7.5] - 2026-11-06

### Fixed

- make now preserves trace output when debugging is enabled during version updates. [3191d7d6](https://github.com/electrocucaracha/gh-updater/commit/3191d7d6621b77a76fc51cc27b63ab54df833921)

## [1.7.4] - 2026-11-06

### Changed

- Updated CI workflows and pre-commit hook versions to leverage the latest fixes and features, bumping the reusable workflow version in GitHub Actions linter from v12.1.1 to v13.2.0 and the ai-prepare-commit-msg pre-commit hook version from v20.10.5 to v20.14.0. [4ec6b2f4](https://github.com/electrocucaracha/gh-updater/commit/4ec6b2f43f0a2a0f7e313bbba734b77aadbee42b)

## [1.7.3] - 2026-10-30

### Fixed

- Stabilized codespell runs by expanding the skip pattern to exclude uv.lock files in subdirectories, preventing false positives or unnecessary checks on dependency lockfiles across the project structure. [8ef3f927](https://github.com/electrocucaracha/gh-updater/commit/8ef3f927fdc84c38da3e07d107d98ea82adab43d)

## [1.7.2] - 2026-10-30

### Changed

- Configuration files now adhere to POSIX conventions by ending with a newline, improving compatibility with tools that expect configuration files to have a trailing newline. [44f39468](https://github.com/electrocucaracha/gh-updater/commit/44f394682b1f4cd783d42ff01f4968efa119e7ae)

## [1.7.1] - 2026-10-30

### Changed

- Simplified the project's linting process by running mypy and pylint checks in a separate job via tox and disabling them in Super-Linter, while also updating the Makefile and workflow documentation to reflect these changes. [00c81c97](https://github.com/electrocucaracha/gh-updater/commit/00c81c975f9241da2a769b80bdc74c97feefc3f6)

## [1.7.0] - 2026-10-30

### Added

- Enabled detailed changelog entries for versions 1.4.0 through 1.6.2, documenting enhancements to code quality, dependency management, linter configuration, project formatting, and pre-commit hook adjustments, thereby improving code maintainability and enforcing consistent formatting and linting. [7e694a51](https://github.com/electrocucaracha/gh-updater/commit/7e694a51637420581b9acac5e238bfaa5a2415d8)

## [1.6.2] - 2026-10-30

### Changed

- Simplified the codespell pre-commit hook to exclude the generated uv.lock file from spell checking, reducing pre-commit noise and improving workflow efficiency. [5bbb58a1](https://github.com/electrocucaracha/gh-updater/commit/5bbb58a16e240d86847e5d64d5255918e3dc20ef)

## [1.6.1] - 2026-10-30

### Changed

- Modernized configuration file indentation to use tabs consistently with the surrounding project's formatting style. [33b3523c](https://github.com/electrocucaracha/gh-updater/commit/33b3523c4d9d6462fcf07367ba7781da6ee203c2)

## [1.6.0] - 2026-10-30

### Added

- Enabled project contributors to work with consistent formatting by enforcing 2-space indents with tabs for JSON files and allowing Markdown files to inherit their indent size from editors, thereby reducing conflicts with Markdown linters and misconfigurations. [890285cf](https://github.com/electrocucaracha/gh-updater/commit/890285cf88477ba2cae2a47d13862ebd487c8cae)

## [1.5.5] - 2026-10-30

### Changed

- Improved code quality and maintainability by introducing type annotations and clear documentation to CLI and test methods, and by enforcing consistent formatting and linting with updated tools and configurations. [a60f621f](https://github.com/electrocucaracha/gh-updater/commit/a60f621f08a7c6e68173478f780ee7e629a7e35e)

## [1.5.4] - 2026-10-30

### Changed

- Unified linter management by centralizing Python tool configurations in pyproject.toml, standardizing formatting and linter rules, and simplifying management to reduce duplication. [3f489936](https://github.com/electrocucaracha/gh-updater/commit/3f489936f382d96b0564fd4d62b726a69f576e33)

## [1.5.3] - 2026-10-30

### Changed

- Simplified the pre-commit configuration by replacing the external markdownlint hook with a local node-based hook that includes biome-format for JSON files. [e15a044e](https://github.com/electrocucaracha/gh-updater/commit/e15a044e932915ee5c9122d0ef4b38c4b9578273)

## [1.5.2] - 2026-10-30

### Changed

- Optimized code quality enforcement and maintainability by migrating the GitHub Actions linter workflow to use modular jobs, a shared super-linter, and updated permissions for least privilege, while also adding license/copyright headers for clarity. [2a6d73b6](https://github.com/electrocucaracha/gh-updater/commit/2a6d73b6d89f9fa8d88fd97045b61862ffa1fc7c)

## [1.5.1] - 2026-10-30

### Changed

- Modernized dependency management by automating weekly version updates through a scheduled GitHub Actions workflow and corresponding shell script, ensuring up-to-date automation and development tools across multiple Python versions. [a4bb43ff](https://github.com/electrocucaracha/gh-updater/commit/a4bb43ff999e573a6eebf4136e0be316c6a4910d)

## [1.5.0] - 2026-10-12

### Added

- Enabled users to support ongoing development through funding links, introducing GitHub Sponsors and Buy Me a Coffee profiles for community contributions and project sustainability. [fa2cf941](https://github.com/electrocucaracha/gh-updater/commit/fa2cf941ac3c2f9c7abe12762d2a1bd6dcf3fee9)

## [1.4.0] - 2026-10-12

### Added

- Enabled a structured record of project changes through the introduction of a CHANGELOG.md file adhering to Keep a Changelog and Semantic Versioning guidelines. [151ba2ac](https://github.com/electrocucaracha/gh-updater/commit/151ba2ac8903864baf48bd6f4e9b3e489bb522bc)

## [1.3.1] - 2026-10-12

### Changed

- Standardized table formatting in Markdown documentation and Makefile tasks for improved readability and automated consistency checks. [8fc03aba](https://github.com/electrocucaracha/gh-updater/commit/8fc03abab2238e623d1b230c90127386ec9287ee)

## [1.3.0] - 2026-10-12

### Added

- Enabled the documentation site with a user-friendly configuration, including a customizable project title and theme selection, and improved code sharing capabilities through the copy code button. [af03800a](https://github.com/electrocucaracha/gh-updater/commit/af03800ab101f24aef17323159c6329423abaf95)

## [1.2.1] - 2026-10-12

### Changed

- Clarified and expanded the project's readme documentation to provide a more comprehensive guide for users, including improved security considerations and version resolution behavior. [aa9b4cbe](https://github.com/electrocucaracha/gh-updater/commit/aa9b4cbe333a55f0b89e75aa5c4fa6fdb8f257bc)

## [1.2.0] - 2026-10-12

### Added

- Enabled flexible authoring in Markdown files by disabling linting checks for H1 headers and line length, allowing for self-contained documents and longer lines without false positives. [ebe4b0ba](https://github.com/electrocucaracha/gh-updater/commit/ebe4b0baf0dabbf95cae5409a02d4ee55eed1b5a)

## [1.1.1] - 2026-10-12

### Changed

- The pre-commit hooks configuration has been modernized to enable automatic installation and clarify licensing, eliminating the need for custom Ruff and yamllint entries. [f6a429b5](https://github.com/electrocucaracha/gh-updater/commit/f6a429b5e8db67ec0be6b973409996113c83273b)

## [1.1.0] - 2026-10-12

### Added

- Enabled users to control parallel lookup workers with a new --workers option, defaulting to min(32, CPUs + 4) and capped at the number of upstream repositories, resulting in improved resource usage and reduced latency on large invocations. [088d62fb](https://github.com/electrocucaracha/gh-updater/commit/088d62fb0f1b33218b2385e92bf7031eacda6bc1)

## [1.0.0] - 2026-10-11

### Added

- Enabled the gh-updater tool to update GitHub Actions references to the latest stable commit, including project configuration and setup scripts, with no breaking changes or migration requirements. [f449200e](https://github.com/electrocucaracha/gh-updater/commit/f449200ec6b799bde69bfebe5d784185ae17467b)
