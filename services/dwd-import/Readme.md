# Teuto Moisture Map - DWD Import

## Requirements

- [poetry](https://python-poetry.org) for local development
- docker for building/running the docker image

## Doing things with poetry

Run `poetry install` to install dependencies within a virtual environment managed by poetry.

Run `poetry shell` to span a shell with the created virtual environment for following commands or prefix each by `poetry run`

Run `dwd-import` to run the main application for importing raster data.

Run `dwd-stations` to run the test application for  importing station data.

## Doing things with docker

It's easiest to use the top level docker compose setup using `docker compose up --build`.

Otherwise run `docker build -t dwd-import . && docker run -it dwd-import` to build an run the service inside docker.
