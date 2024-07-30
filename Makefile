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
	rye test
	@echo "✅ Tests passed"

test-with-coverage: 
	@echo "🔨🔨🔨 Testing 🔨🔨🔨"
	@make test
	@rye run diff-cover .coverage.xml
	@echo "✅ Tests passed"

lint: ## Format code
	@echo "🔨🔨🔨 Linting 🔨🔨🔨"
	@rye run ruff format .
	@rye run ruff . --fix --unsafe-fixes
	@echo "✅ Lint"

types: ## Type-check code
	@echo "🔨🔨🔨 Type-checking 🔨🔨🔨"
	@rye run pyright .
	@echo "✅ Types"

validate_ci: ## Run all checks
	@echo "🔨🔨🔨 Running all checks 🔨🔨🔨"
	@make lint
	@make types
	## CI doesn't support local coverage report, so skipping full test
	@make test

docker_ci: ## Run all checks in docker
	@echo "🔨🔨🔨 Running all checks in docker 🔨🔨🔨"
	docker build -t lumberman_ci -f .github/Dockerfile.dev .
	docker run lumberman_ci make validate_ci

#########################
# End template makefile #
#########################