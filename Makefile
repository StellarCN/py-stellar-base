
# default target does nothing
.DEFAULT_GOAL: default
default: ;

install:
	pip install .
.PHONY: install

install-test:
	pip install -r requirements-test.txt
.PHONY: install-test

test:
	pytest -v -s -rs tests --cov --cov-report=html
.PHONY: test

fulltest:
	pytest -v -s -rs tests --runslow --cov --cov-report=html
.PHONY: fulltest

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

updatexdr:
	python .xdr/update_xdr.py
.PHONY: updatexdr