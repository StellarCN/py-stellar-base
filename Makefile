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
XDRGEN_COMMIT=c5f88c2ec9c39296aebf06da8756bb7f8b83b34e
XDR_COMMIT=529d5176f24c73eeccfa5eba481d4e89c19b1181


ifeq ($(shell uname), Darwin)
SED := sed -i ''
REPLACE_KEYWORD_COMMAND := find xdr -type f -exec sed -i '' 's/from;/from_;/g' {} +
REPLACE_DOCS := sed -i '' '/stellar_sdk\.xdr/,$$d' docs/en/api.rst
else
SED := sed
REPLACE_KEYWORD_COMMAND := find xdr -type f -exec sed -i 's/from;/from_;/g' {} \;
REPLACE_DOCS := sed -i '/stellar_sdk\.xdr/,$$d' docs/en/api.rst
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
	pre-commit run --all-file
.PHONY: format

replace-xdr-keywords:
	$(REPLACE_KEYWORD_COMMAND)
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
	pip install -e .
	$(REPLACE_DOCS)
	python docs/gen_xdr_api.py >> docs/en/api.rst
.PHONY: xdr-generate

xdr/%.x:
	curl -Lsf -o $@ https://raw.githubusercontent.com/stellar/stellar-xdr/$(XDR_COMMIT)/$(@F)
.PHONY: xdr

xdr-clean:
	rm xdr/*.x || true
	rm stellar_sdk/xdr/*.py || true
.PHONY: xdr-clean

xdr-update: xdr-clean xdr-generate
.PHONY: xdr-update