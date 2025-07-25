# Teuto Moisture Map - API

## Tools

- [uv](https://docs.astral.sh/uv/) for local development
- docker for testing
- terraform to manage the infrastructure

## Doing things with uv

Run `uv sync` to install dependencies within a virtual environment managed by uv.

Run `uv shell` to spawn a shell with the created virtual environment for following commands or prefix each by `uv run`

Run `uv run pytest` to run tests.

Run `uv run black .` to format code using black.

Run `uv run ruff . --fix` for linting.

Run `uv run mypy .` to run type checks.

Run `uv run flask --app tmm_api:app --debug run` to run the application using flask for development.

Run `uv run gunicorn --bind 0.0.0.0:5000 tmm_api:app` to run the application using gunicorn for production.

## Doing things with nox

Run `uv run nox` to run pytest, black, ruff and mypy.

Run `uv run nox -s serv` to start the development server.

## Doing things with docker

It's easiest to use the top level docker compose setup using `docker compose up --build tmm-api`.

Otherwise run `docker build -t tmm-api . && docker run <set environment> -p 5000:5000 -it tmm-api` to build an run the service inside docker.

## Local development

Create a `influx_config.ini` containing the configuration for the influx database you wish to use.  

You may use the provided `influx_config.ini.template` file which works with the top level docker compose config.
In that case start the local influx instance from the root directory using `docker compose up -d influx`.

Afterwards start the development server using `uv run nox -s serv`.

## Helper Scripts

### Generate API Keys

Use `uv run scripts/keygen.py <device-id>` to generate api keys.
