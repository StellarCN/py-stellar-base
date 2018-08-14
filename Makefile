
# default target does nothing
.DEFAULT_GOAL: default
default: ;

init:
	pip install .
	pip install -e .
	pip install pytest-cov
.PHONY: init

start:
	docker run --rm -d -p "8000:8000" --name stellar zulucrypto/stellar-integration-test-network
	sleep 10
.PHONY: start

stop:
	docker stop stellar
.PHONY: stop

test:
	python -m pytest -v -rs tests --cov
.PHONY: test

testnet:
	python -m pytest -v -rs tests --testnet --cov
.PHONY: testnet

codecov:
	pip install codecov
	python -m codecov
.PHONY: codecov

wheel:
	python setup.py bdist_wheel
.PHONY: wheel

pypi:
	twine upload dist/*
.PHONY: pypi

clean:
	find . -name \*.pyc -delete
.PHONY: clean

updatexdr:
	cd stellar_base/stellarxdr && python updatexdr.py && python xdrgen.py ../xdr/
.PHONY: updatexdr