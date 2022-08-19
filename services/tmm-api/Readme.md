# Teuto Moisture Map - API

## Requirements

- [poetry](https://python-poetry.org) for local development
- docker for building/running the docker image

## Doing things with poetry

Run `poetry install` to install dependencies within a virtual environment managed by poetry.

Run `poetry shell` to span a shell with the created virtual environment for following commands or prefix each by `poetry run`

Run `pytest` to run tests.

Run `flask --app tmm_api:app --debug run` to run the application using flask for development.

Run `gunicorn --bind 0.0.0.0:5000 tmm_api:app` to run the application using gunicorn for production.

## Doing things with docker

It's easiest to use the top level docker compose setup using `docker compose up --build`.

Otherwise run `docker build -t tmm-api . && docker run <set environment> -p 5000:5000 -it tmm-api` to build an run the service inside docker.
