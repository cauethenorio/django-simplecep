.PHONY: lint

lint: ## check style with flake8
	flake8 simplecep

black: ## reformat code with black
	black simplecep

black-lint: black lint

test: ## run tests quickly with the default Python
	python runtests.py

test-all: ## run tests on every Python version with tox
	tox
