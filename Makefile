.PHONY: lint

lint: ## check style with flake8
	flake8 django_fast_cep

black: ## reformat code with black
	black django_fast_cep

black-lint: black lint

test: ## run tests quickly with the default Python
	python runtests.py

test-all: ## run tests on every Python version with tox
	tox
