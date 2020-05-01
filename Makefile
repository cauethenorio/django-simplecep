.PHONY: lint black black-list test coverage-report test-all messages compilemessages migrations

lint: ## check style with flake8
	flake8 simplecep

black: ## reformat code with black
	black simplecep

black-lint: black lint

test: ## run tests quickly with the default Python
	cd tests && coverage run ../manage.py test

coverage-report:
	cd tests && coverage html && open ./coverage_html/index.html

test-all: ## run tests on every Python version with tox
	tox

messages: ## generate brazilian portuguese po file for translation
	cd simplecep && python ../manage.py makemessages --locale pt_BR

compilemessages: ## compile translation po file to binary mo file
	cd simplecep && python ../manage.py compilemessages

migrations: ## build simplecep migration files
	python manage.py makemigrations simplecep
