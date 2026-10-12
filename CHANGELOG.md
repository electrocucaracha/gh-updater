<!-- Markdownlint-disable MD024 -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
