# ==============================================================================
# Makefile for Project Automation
#
# This Makefile automates tasks such as testing, code quality checks,
# and packaging.
# ==============================================================================

# ==============================================================================
# Phony Targets Declaration
# Declare all targets that do not represent actual files to ensure they
# are always executed and to improve 'make' performance.
# ==============================================================================
.PHONY: default unit-test integration-test package clean \
        pre-commit type-check

# ==============================================================================
# Configuration Variables
# Define key project-specific variables for easier management.
# ==============================================================================

# Command prefix for running Python tools with uv
UV_RUN_CMD = uv run --frozen --all-extras

# ==============================================================================
# Default Target
# No action by default, encourages explicit target execution.
# ==============================================================================
default: ;

# ==============================================================================
# Test Automation
# Targets for running various levels of tests with coverage.
# ==============================================================================
unit-test:
	$(UV_RUN_CMD) pytest -v -rs tests --cov --cov-report=html

integration-test:
	$(UV_RUN_CMD) pytest -v -rs tests --integration --cov=./ --cov-report=xml

# ==============================================================================
# Build & Clean Targets
# Manage project packaging and cleanup of build artifacts.
# ==============================================================================
package:
	uv build

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	rm -rf coverage.xml .coverage dist htmlcov stellar_sdk.egg-info .mypy_cache .pytest_cache docs/en/_build

# ==============================================================================
# Code Quality Checks
# Targets for running pre-commit hooks and type checkers.
# ==============================================================================
pre-commit:
	$(UV_RUN_CMD) pre-commit run --all-files

type-check:
	$(UV_RUN_CMD) pyright
	$(UV_RUN_CMD) mypy -p stellar_sdk -p tests -p examples
