# Teuto Moisture Map - DWD Import

## Requirements

- [poetry](https://python-poetry.org) for local development
- [nox](https://nox.thea.codes/en/stable/) for running all checks in one go
- docker for building/running the docker image

## Doing things with poetry

Run `poetry install` to install dependencies within a virtual environment managed by poetry.

Run `poetry shell` to spawn a shell with the created virtual environment for following commands or prefix each by `poetry run`

Run `pytest` to run tests.

Run `black .` to format code using black.

Run `ruff . --fix` for linting.

Run `mypy .` to run type checks.

Run `dwd-import` to run the main application for importing raster data.

Run `dwd-stations` to run the test application for  importing station data.

## Doing things with nox

Run `nox` to run pytest, black, ruff and mypy.

## Doing things with docker

It's easiest to use the top level docker compose setup using `docker compose up --build`.

Otherwise run `docker build -t dwd-import . && docker run -it dwd-import` to build an run the service inside docker.
