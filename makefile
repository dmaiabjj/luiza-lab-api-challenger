-include .env
export


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

db/initialize:
	python manage.py init_db

local/clean:
	docker-compose stop && docker-compose rm -vf

local/up: local/clean
	docker-compose up -d

run:
	python manage.py runserver

PYTHON_BIN ?= .venv/bin