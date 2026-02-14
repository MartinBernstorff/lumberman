###########################
# Start template makefile #
###########################

SRC_PATH = lumberman
MAKEFLAGS = --no-print-directory

# Dependency management
install:
	rye sync

quicksync:
	rye sync --no-lock

test:
	uv run pytest

test-with-coverage: 
	@echo "––– Testing –––"
	@make test
	@uv run diff-cover .coverage.xml
	@echo "✅✅✅ Tests passed ✅✅✅"

lint: ## Format code
	@echo "––– Linting –––"
	@uv run ruff format .
	@uv run ruff . --fix --unsafe-fixes
	@echo "✅✅✅ Lint ✅✅✅"

types: ## Type-check code
	@echo "––– Type-checking –––"
	@uv run pyright .
	@echo "✅✅✅ Types ✅✅✅"

validate_ci: ## Run all checks
	@echo "––– Running all checks –––"
	@make lint
	@make types
	## CI doesn't support local coverage report, so skipping full test
	@make test

docker_ci: ## Run all checks in docker
	@echo "––– Running all checks in docker –––"
	docker build -t lumberman_ci -f .github/Dockerfile.dev .
	docker run lumberman_ci make validate_ci

#########################
# End template makefile #
#########################