# Scribe Project Makefile
# Provides convenient commands for development, testing, and building

.PHONY: help install test clean build lint format type-check pre-commit dev-setup docs docs-clean docs-serve docs-watch

# Default target
help: ## Show this help message
	@echo "Scribe Development Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Create virtual environment and install dependencies
	@echo "Setting up Scribe development environment..."
	poetry install
	@echo "✓ Virtual environment created and dependencies installed"

setup: install ## Alias for install command
	@echo "✓ Development environment setup complete"

test: clean-test ## Run tests with coverage
	@echo "Running tests..."
	poetry run pytest tests/ -v --cov=scribe --cov-report=html --cov-report=term-missing
	@echo "✓ Tests completed. Coverage report available in htmlcov/"

test-fast: ## Run tests without coverage (faster)
	@echo "Running tests (fast mode)..."
	poetry run pytest tests/ -v
	@echo "✓ Tests completed"

clean: clean-test clean-build clean-cache ## Clean all generated files and caches
	@echo "✓ All generated files cleaned"

clean-test: ## Clean test artifacts
	@echo "Cleaning test artifacts..."
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf test_project/
	@echo "✓ Test artifacts cleaned"

clean-build: ## Clean build artifacts
	@echo "Cleaning build artifacts..."
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	@echo "✓ Build artifacts cleaned"

clean-cache: ## Clean Python cache files
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@echo "✓ Cache files cleaned"

build: clean-build ## Build distribution packages (wheel and source)
	@echo "Building distribution packages..."
	poetry build
	@echo "✓ Distribution packages built in dist/"

build-wheel: clean-build ## Build only wheel package
	@echo "Building wheel package..."
	poetry build --format wheel
	@echo "✓ Wheel package built in dist/"

build-sdist: clean-build ## Build only source distribution
	@echo "Building source distribution..."
	poetry build --format sdist
	@echo "✓ Source distribution built in dist/"

lint: ## Run linting checks
	@echo "Running linting checks..."
	poetry run flake8 scribe/ tests/
	@echo "✓ Linting completed"

format: ## Format code with black
	@echo "Formatting code..."
	poetry run black scribe/ tests/
	@echo "✓ Code formatted"

format-check: ## Check if code is properly formatted
	@echo "Checking code formatting..."
	poetry run black --check scribe/ tests/
	@echo "✓ Code formatting check completed"

type-check: ## Run type checking with mypy
	@echo "Running type checks..."
	poetry run mypy scribe/
	@echo "✓ Type checking completed"

pre-commit: ## Run pre-commit hooks
	@echo "Running pre-commit hooks..."
	poetry run pre-commit run --all-files
	@echo "✓ Pre-commit hooks completed"

dev-setup: install ## Complete development setup with pre-commit hooks
	@echo "Setting up development environment..."
	poetry run pre-commit install
	@echo "✓ Development environment setup complete with pre-commit hooks"

check: lint format-check type-check test ## Run all quality checks
	@echo "✓ All quality checks passed"

ci: clean check build ## Run CI pipeline (clean, check, build)
	@echo "✓ CI pipeline completed successfully"

demo: ## Run a quick demo of scribe init
	@echo "Running scribe demo..."
	@mkdir -p demo_project
	cd demo_project && poetry run scribe init
	@echo "✓ Demo completed. Check demo_project/ directory"

demo-clean: ## Clean demo project
	@echo "Cleaning demo project..."
	rm -rf demo_project/
	@echo "✓ Demo project cleaned"

install-local: build ## Install scribe locally for testing
	@echo "Installing scribe locally..."
	pip install dist/*.whl
	@echo "✓ Scribe installed locally"

uninstall-local: ## Uninstall local scribe installation
	@echo "Uninstalling scribe..."
	pip uninstall scribe -y
	@echo "✓ Scribe uninstalled"

publish-test: build ## Publish to test PyPI (requires credentials)
	@echo "Publishing to test PyPI..."
	poetry publish --repository testpypi
	@echo "✓ Published to test PyPI"

publish: build ## Publish to PyPI (requires credentials)
	@echo "Publishing to PyPI..."
	poetry publish
	@echo "✓ Published to PyPI"

deps-update: ## Update dependencies
	@echo "Updating dependencies..."
	poetry update
	@echo "✓ Dependencies updated"

deps-outdated: ## Check for outdated dependencies
	@echo "Checking for outdated dependencies..."
	poetry show --outdated
	@echo "✓ Dependency check completed"

shell: ## Open poetry shell
	@echo "Opening poetry shell..."
	poetry shell

version: ## Show current version
	@poetry version

version-patch: ## Bump patch version
	@poetry version patch

version-minor: ## Bump minor version
	@poetry version minor

version-major: ## Bump major version
	@poetry version major

# Documentation targets
docs: ## Build documentation
	@echo "📚 Building documentation..."
	cd docs && poetry run sphinx-build -b html source _build/html
	@echo "✅ Documentation built in docs/_build/html/"

docs-clean: ## Clean documentation
	@echo "🧹 Cleaning documentation..."
	rm -rf docs/_build/
	@echo "✅ Documentation cleaned"

docs-serve: docs ## Serve documentation locally
	@echo "🌐 Serving documentation..."
	cd docs/_build/html && python -m http.server 8000

docs-watch: ## Watch documentation for changes
	@echo "👀 Watching documentation for changes..."
	cd docs && poetry run sphinx-autobuild source _build/html --host 0.0.0.0 --port 8000
