# default target does nothing
.DEFAULT_GOAL: default
default: ;

install:
	pip install .
.PHONY: install

install-dev:
	pipenv install --dev
.PHONY: install-dev

test:
	pytest -v -s -rs tests --cov --cov-report=html
.PHONY: test

full-test:
	pytest -v -s -rs tests --runslow --cov --cov-report=html
.PHONY: full-test

codecov:
	codecov
.PHONY: codecov

package:
	python setup.py sdist bdist_wheel
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

lock:
	pipenv lock --requirements > requirements.txt
	pipenv lock --requirements --dev > requirements-dev.txt
.PHONY: lock
