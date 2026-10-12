UV ?= uv

.PHONY: test coverage lint fmt

test:
	$(UV) run --frozen tox -e test

coverage:
	$(UV) run --frozen tox -e coverage

lint:
	$(UV) run --frozen tox -e lint

fmt:
	$(UV) run --frozen tox -e fmt

