-include .env
export

# Run pep8 code style validations
#
#   make build/code-style
#
build/code-style:
	$(PYTHON_BIN)/pycodestyle --statistics --ignore=E501,E402 --count app/ test/

# Install dependent libraries
#
#   make build/dependencies/install
#
build/dependencies/install:
	$(PYTHON_BIN)/pip3 install -r ./config/requirements.txt
	$(PYTHON_BIN)/pip3 install -r ./config/build_requirements.txt

# Run safety check on lib dependencies
#
#   make build/dependencies/lib/safety-check
#
build/dependencies/lib/safety-check:
	$(PYTHON_BIN)/safety check -r ./config/requirements.txt
	$(PYTHON_BIN)/safety check -r ./config/build_requirements.txt

# Build project
#
#   make build
#
build: build/dependencies/install build/dependencies/lib/safety-check build/code-style

db/migration:
	python manage.py db migrate -m ${name}

db/migrate:
	python manage.py db upgrade

db/initialize:
	python manage.py init_db

local/clean:
	docker-compose stop && docker-compose rm -vf

local/up: local/clean
	docker-compose up -d
	sleep 15

# Upload coverage report
#
#   make test/coverage/upload current_branch==master
#
test/coverage/upload:
ifeq ($(stage),prod)
	$(PYTHON_BIN)/codecov -t $(CODECOV_TOKEN) -b $(CURRENT_BRANCH)
else
	@echo $(CURRENT_BRANCH)
endif



# Run project tests
#
#   make test
#
test: build local/up db/migrate test/run
	make local/clean

# Run tests with its coverage report
#
#   make test/run
#
test/run:
	$(PYTHON_BIN)/py.test test -v -x --cov-fail-under=80


run: build local/up db/migrate db/initialize
	python manage.py runserver




PYTHON_BIN ?= .venv/bin