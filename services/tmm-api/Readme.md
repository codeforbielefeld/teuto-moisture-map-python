# Teuto Moisture Map - API

## Requirements

- [poetry](https://python-poetry.org) for local development
- [nox](https://nox.thea.codes/en/stable/) for running all checks in one go
- [pack](https://buildpacks.io/docs/tools/pack/) for building the production image using buildpacks
- docker

## Doing things with poetry

Run `poetry install` to install dependencies within a virtual environment managed by poetry.

Run `poetry shell` to span a shell with the created virtual environment for following commands or prefix each by `poetry run`

Run `pytest` to run tests.

Run `black .` to format code using black.

Run `ruff . --fix` for linting.

Run `mypy .` to run type checks.

Run `flask --app tmm_api:app --debug run` to run the application using flask for development.

Run `gunicorn --bind 0.0.0.0:5000 tmm_api:app` to run the application using gunicorn for production.

## Doing things with nox

Run `nox` to run pytest, black, ruff and mypy.

Run `nox -s serv` to start the development server.

## Doing things with docker

It's easiest to use the top level docker compose setup using `docker compose up --build tmm-api`.

Otherwise run `docker build -t tmm-api . && docker run <set environment> -p 5000:5000 -it tmm-api` to build an run the service inside docker.

Alternatively use buildpacks to build the docker image `pack build tmm-api --buildpack paketo-buildpacks/python`.

## Local development
Start a local influx instance using the top level docker compose setup using `docker compose up -d influx`.

Start the development server using `nox -s serv`.
