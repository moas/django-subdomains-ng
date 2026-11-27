install:
	python -m pip install .

test:
	python -m django test subdomains.tests --settings=subdomains.tests.settings

test-matrix:
	python -m tox

.PHONY: install test test-matrix
