# ==============================================================================
# Makefile for Project Automation
#
# This Makefile automates tasks such as XDR generation, testing,
# code quality checks, and packaging.
# ==============================================================================

# ==============================================================================
# Phony Targets Declaration
# Declare all targets that do not represent actual files to ensure they
# are always executed and to improve 'make' performance.
# ==============================================================================
.PHONY: default unit-test full-unit-test integration-test package clean \
        pre-commit type-check replace-xdr-keywords xdr-generate xdr \
        xdr-clean xdr-update xdr-generator-test xdr-generator-update-snapshots

# ==============================================================================
# Configuration Variables
# Define key project-specific variables for easier management.
# ==============================================================================

# XDR (External Data Representation) files list
XDRS = xdr/Stellar-SCP.x \
       xdr/Stellar-ledger-entries.x \
       xdr/Stellar-ledger.x \
       xdr/Stellar-overlay.x \
       xdr/Stellar-transaction.x \
       xdr/Stellar-types.x \
       xdr/Stellar-contract-env-meta.x \
       xdr/Stellar-contract-meta.x \
       xdr/Stellar-contract-spec.x \
       xdr/Stellar-contract.x \
       xdr/Stellar-internal.x \
       xdr/Stellar-contract-config-setting.x \
       xdr/Stellar-exporter.x

# Stellar XDR definitions repository commit hash
XDR_COMMIT = 4b7a2ef7931ab2ca2499be68d849f38190b443ca

# Command prefix for running Python tools with uv
UV_RUN_CMD = uv run --frozen --all-extras

# ==============================================================================
# Platform-Specific Commands
# Adjust commands based on the operating system (e.g., 'sed' differences).
# ==============================================================================
ifeq ($(shell uname), Darwin)
    SED_INPLACE := sed -i ''
    # Use find -exec with \; for macOS sed due to argument parsing differences
    REPLACE_KEYWORD_COMMAND := find xdr -type f -exec $(SED_INPLACE) 's/from;/from_;/g' {} +
    REPLACE_DOCS := $(SED_INPLACE) '/stellar_sdk\.xdr/,$$d' docs/en/api.rst
else
    SED_INPLACE := sed -i
    # Use find -exec with {} \; for Linux/GNU sed
    REPLACE_KEYWORD_COMMAND := find xdr -type f -exec $(SED_INPLACE) 's/from;/from_;/g' {} \;
    REPLACE_DOCS := $(SED_INPLACE) '/stellar_sdk\.xdr/,$$d' docs/en/api.rst
endif

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
	$(UV_RUN_CMD) pytest -v -s -rs tests --cov --cov-report=html

full-unit-test:
	$(UV_RUN_CMD) pytest -v -s -rs tests --runslow --cov --cov-report=html

integration-test:
	$(UV_RUN_CMD) pytest -v -s -rs tests --runslow --integration --cov=./ --cov-report=xml

# ==============================================================================
# Build & Clean Targets
# Manage project packaging and cleanup of build artifacts.
# ==============================================================================
package:
	uv build

clean:
	find . -name \*.pyc -delete
	rm -rf coverage.xml .coverage dist htmlcov stellar_sdk.egg-info tests/.mypy_cache tests/.pytest_cache docs/en/_build

# ==============================================================================
# Code Quality Checks
# Targets for running pre-commit hooks and type checkers.
# ==============================================================================
pre-commit:
	$(UV_RUN_CMD) pre-commit run --all-file

type-check:
	$(UV_RUN_CMD) pyright
	$(UV_RUN_CMD) mypy -p stellar_sdk -p tests -p examples

# ==============================================================================
# XDR Generation & Management
# Targets for fetching, generating, and cleaning XDR-related files.
# ==============================================================================

replace-xdr-keywords:
	$(REPLACE_KEYWORD_COMMAND)

xdr-generate: $(XDRS) replace-xdr-keywords
	@echo "--- Generating XDR Python files ---"
	$(REPLACE_KEYWORD_COMMAND)
	docker run -it --rm -v $(PWD):/wd -w /wd ruby:3.4 /bin/bash -c '\
		cd xdr-generator && \
		bundle install --quiet && \
		bundle exec ruby generate.rb'
	@echo "--- Updating XDR API documentation ---"
	$(REPLACE_DOCS)
	$(UV_RUN_CMD) python docs/gen_xdr_api.py >> docs/en/api.rst
	@echo "--- Running pre-commit hooks ---"
	$(MAKE) pre-commit

xdr/%.x:
	@echo "--- Fetching $@ ---"
	curl -Lsf -o $@ https://raw.githubusercontent.com/stellar/stellar-xdr/$(XDR_COMMIT)/$(@F)

xdr-generator-test:
	@echo "--- Running xdr-generator snapshot tests ---"
	docker run --rm -v $(PWD):/wd -w /wd ruby:3.4 /bin/bash -c '\
		cd xdr-generator && \
		bundle install --quiet && \
		bundle exec ruby test/generator_snapshot_test.rb'

xdr-generator-update-snapshots:
	@echo "--- Updating xdr-generator snapshots ---"
	docker run --rm -v $(PWD):/wd -w /wd ruby:3.4 /bin/bash -c '\
		cd xdr-generator && \
		bundle install --quiet && \
		UPDATE_SNAPSHOTS=1 bundle exec ruby test/generator_snapshot_test.rb'

xdr-clean:
	@echo "--- Cleaning XDR files ---"
	rm -f xdr/*.x stellar_sdk/xdr/*.py || true

xdr-update: xdr-clean xdr-generate
	@echo "--- XDR update complete ---"
