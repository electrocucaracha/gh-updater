<!-- Markdownlint-disable MD024 -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
