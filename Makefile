APP_NAME="app"
IMAGE_NAME="image"
VERSION="latest"
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    DOCKER_USER=$(shell id -u $(USER)):$(shell id -g $(USER))
endif
ifeq ($(UNAME_S),Darwin)
    DOCKER_USER=
endif

local/install:
	pipenv install --dev --skip-lock

local/lint:
	black --check app/
	flake8 app/

local/lint/fix:
	black app/

local/check-packages:
	pipenv check --system -e PIPENV_PYUP_API_KEY=""

local/bandit:
	bandit -r . app *.py

local/shell:
	pipenv shell

local/test:
	ENV_FOR_DYNACONF=test python -m pytest -s -c tests/pytest.ini \
	--pyargs ./tests -v --junitxml=results.xml \
	--cov-fail-under 50 --cov-report xml \
	--cov-report term \
	--cov-report html --cov ./app

local/run:
	python run.py


docker/build:
	docker-compose build ${APP_NAME}

docker/up:
	docker-compose up -d

docker/postgres/up:
	docker-compose up -d postgres-db

docker/down:
	docker-compose down --remove-orphans

docker/lint:
	docker-compose run ${APP_NAME} black --check app/
	docker-compose run ${APP_NAME} flake8 app/

docker/lint/fix:
	docker-compose run ${APP_NAME} run black app/

docker/check-packages:
	docker-compose run -e PIPENV_PYUP_API_KEY="" ${APP_NAME} pipenv check --system

docker/bandit:
	docker-compose run ${APP_NAME} bandit -r . app *.py

docker/verify:
	make docker/lint
	make docker/bandit

docker/test:
	docker-compose run -e ENV_FOR_DYNACONF=test ${APP_NAME} \
	python -m pytest -s -c tests/pytest.ini \
	--pyargs ./tests -v  \
	--cov-fail-under 50 --cov-report xml \
	--cov-report term \
	--cov-report html --cov ./app

docker/run:
	docker-compose run --service-port ${APP_NAME} python run.py

docker/migrations/generate:
	docker-compose run ${APP_NAME} alembic revision --autogenerate

docker/migrations/upgrade:
	docker-compose run ${APP_NAME} alembic upgrade head

image/build:
	docker build . --target production -t ${IMAGE_NAME}:${VERSION}

image/push:
	docker push ${IMAGE_NAME}:${VERSION}

generate-default-env-file:
	@if [ ! -f .env ]; then cp env.template .env; fi;
