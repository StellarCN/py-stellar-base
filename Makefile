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
	rm -rf coverage.xml .coverage  dist  htmlcov  stellar_sdk.egg-info  tests/.mypy_cache  tests/.pytest_cache  docs/en/_build  docs/zh_CN/_build
.PHONY: clean

download-xdr:
	python .xdr/update_xdr.py
.PHONY: download-xdr

gen-xdr:
	rm -rf stellar_sdk/xdr/*
	xdrgen -o stellar_sdk/xdr -l python -n stellar .xdr/*.x
	autoflake --in-place --ignore-init-module-imports --remove-all-unused-imports stellar_sdk/xdr/*.py
	isort stellar_sdk/xdr/
	black stellar_sdk/xdr/
.PHONY: gen-xdr

format:
	autoflake --in-place --ignore-init-module-imports --remove-all-unused-imports .
	isort .
	black .
.PHONY: format