# TTN Webhook

## Requirements

- [poetry](https://python-poetry.org) for local development
- docker for building/running the docker image

## Doing things with poetry

Run `poetry install` to install dependencies within a virtual environment managed by poetry.

Run `poetry shell` to span a shell with the created virtual environment for follwing commands or prefix each by `poetry run`

Run `pytest` to execut unit tests located in `test`

Run `flask --app ttn_hook:app --debug run` to run the application using flask for development.

Run `gunicorn --bind 0.0.0.0:5000 ttn_hook:app` to run the application using gunicorn for production.

## Doing things with docker

Run `docker build -t ttn-hook . && docker run -p 5000:5000 -it ttn-hook` to build an run the service inside docker.
