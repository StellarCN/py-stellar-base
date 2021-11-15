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
.PHONY: clean

update-xdr:
	python .xdr/update_xdr.py
.PHONY: update-xdr

format:
	isort .
	black --required-version 21.7b0 .
.PHONY: format