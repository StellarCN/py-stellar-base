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
xdr/Stellar-contract-config-setting.x

XDRGEN_REPO=overcat/xdrgen
XDRGEN_COMMIT=3a25689ac881fd9370b45ac2e98908cea86ddaf3
XDRNEXT_COMMIT=e372df9f677961aac04c5a4cc80a3667f310b29f

UNAME := $(shell uname)
SED := sed
ifeq ($(UNAME), Darwin)
	SED := sed -i ''
endif

# default target does nothing
.DEFAULT_GOAL: default
default: ;

install:
	pip install .
.PHONY: install

install-dev:
	poetry install
.PHONY: install-dev

test:
	poetry run pytest -v -s -rs tests --cov --cov-report=html
.PHONY: test

full-test:
	poetry run pytest -v -s -rs tests --runslow --cov --cov-report=html
.PHONY: full-test

codecov:
	codecov
.PHONY: codecov

package:
	poetry build
.PHONY: package

pypi:
	twine upload dist/*
.PHONY: pypi

clean:
	find . -name \*.pyc -delete
	rm -rf coverage.xml .coverage dist htmlcov stellar_sdk.egg-info tests/.mypy_cache tests/.pytest_cache docs/en/_build docs/zh_CN/_build
.PHONY: clean

format:
	autoflake --in-place --ignore-init-module-imports --remove-all-unused-imports --recursive .
	isort .
.PHONY: format

replace-xdr-keywords:
	find xdr -type f -exec $(SED) 's/from;/from_;/g' {} +
.PHONY: replace-xdr-keywords

xdr-generate: $(XDRS)
	make replace-xdr-keywords
	docker run -it --rm -v $$PWD:/wd -w /wd ruby /bin/bash -c '\
		gem install specific_install -v 0.3.8 && \
		gem specific_install https://github.com/$(XDRGEN_REPO).git -b $(XDRGEN_COMMIT) && \
		xdrgen \
			--language python \
			--namespace stellar \
			--output stellar_sdk/xdr \
			$(XDRS)'
.PHONY: xdr-generate

xdr/%.x:
	curl -Lsf -o $@ https://raw.githubusercontent.com/stellar/stellar-xdr/$(XDRNEXT_COMMIT)/$(@F)
.PHONY: xdr

xdr-clean:
	rm .xdr/*.x || true
	rm stellar_sdk/xdr/*.py || true
.PHONY: xdr-clean

xdr-update: xdr-clean xdr-generate format
.PHONY: xdr-update