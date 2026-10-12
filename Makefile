# SPDX-license-identifier: Apache-2.0
##############################################################################
# Copyright (c) 2026
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

DOCKER_CMD ?= $(shell which docker 2> /dev/null || which podman 2> /dev/null || echo docker)

UV ?= uv

.PHONY: test coverage clean lint fmt

test:
	$(UV) run --frozen tox -e test

coverage:
	$(UV) run --frozen tox -e coverage

clean:
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.tox' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name 'htmlcov' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name 'build' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name 'dist' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.ruff_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name 'node_modules' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '.coverage' -exec rm -f {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -exec rm -f {} + 2>/dev/null || true
	find . -type f -name '*.pyo' -exec rm -f {} + 2>/dev/null || true
	find . -type f -name '*.pyd' -exec rm -f {} + 2>/dev/null || true
	@echo "Clean complete!"

lint: clean
	sudo -E $(DOCKER_CMD) run --rm -v $$(pwd):/tmp/lint \
	-e RUN_LOCAL=true \
	-e LINTER_RULES_PATH=/ \
	-e DEFAULT_BRANCH=main \
	ghcr.io/super-linter/super-linter
	command -v uvx > /dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
	uvx tox -e lint-check
	@echo "Lint complete!"

fmt: clean
	command -v shfmt > /dev/null || curl -s "https://i.jpillora.com/mvdan/sh!!?as=shfmt" | bash
	shfmt -l -w -s -i 4 .
	command -v yamlfmt > /dev/null || curl -s "https://i.jpillora.com/google/yamlfmt!!" | bash
	yamlfmt -dstar **/*.{yaml,yml}
	command -v textlint > /dev/null && npm list --global --depth=0 textlint-rule-terminology > /dev/null 2>&1 || sudo npm install --global textlint textlint-rule-terminology
	textlint . --fix
	command -v prettier > /dev/null || npm install prettier
	npx prettier . --write
	command -v uvx > /dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
	uvx tox -e lint
	@echo "Format complete!"
