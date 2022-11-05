# Teuto Moisture Map - TTN Webhook

This project contains a small python app that acts as the receiving end for a webhook in TheThingsNetwork. The purpose of this app is to collect environmental data from a number of sensors and store the sensor's readings in a database.

---

**! In its current state the app is but a prototype !**

---

## Supported sensors

As of now the app has only been tested with the Dragino Moisture Sensor (<http://www.dragino.com/>). Extracting the readings from the payload might not work if a different sensor is used.

## Prerequisites

1. The sensor must be registered in TTN (<https://www.thethingsnetwork.org/>).
2. An Application must be created in TTN and the sensor needs to be assigned to it.
3. Within the Application, a webhook must be created that points to the correct hostname, port and path.
4. As of now the app only works with InfluxDB (<https://www.influxdata.com/>). You either need an InfluxDB 2.0 Cloud account or some other host running InfluxDB 2.0.
5. Put your InfluxDB 2.0 connection configuration into a file called **config.ini** (see: <https://influxdb-client.readthedocs.io/en/latest/api.html#influxdb_client.InfluxDBClient.from_config_file>)
6. Make sure the `TMM_BUCKET` and `TMM_API_KEY` environment variables are set appropriately.  

If everything has been set up correctly, you should see measurements piling into your selected InfluxDB bucket :-)

## Requirements

- [poetry](https://python-poetry.org) for local development
- docker for building/running the docker image

## Doing things with poetry

Run `poetry install` to install dependencies within a virtual environment managed by poetry.

Run `poetry shell` to span a shell with the created virtual environment for following commands or prefix each by `poetry run`

Run `pytest` to execute unit tests located in `test`

Run `flask --app ttn_hook:app --debug run` to run the application using flask for development.

Run `gunicorn --bind 0.0.0.0:5000 ttn_hook:app` to run the application using gunicorn for production.

## Doing things with docker

Run `docker build -t ttn-hook . && docker run -e TMM_BUCKET -e TMM_API_KEY  -p 5000:5000 -it ttn-hook` to build an run the service inside docker.
