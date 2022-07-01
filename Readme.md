# Teuto Moisture Map (Python)

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

If everything has been set up correctly, you should see measurements piling into your selected InfluxDB bucket :-)

## Running the app without Docker

TODO

## Running Tests

To run all Tests in the project which start with _test_ run:


    python -m unittest discover

## Running the application in production mode
TODO

## Running the application in development mode
Simply run:

    docker compose up

Now the TMM web server over localhost:5000 and an InfluxDB is reachable over localhost:8086.

## Post data:
You can post new examples via http://localhost:5000/incomingMessages with json body eg. `services/web/src/test/dragino_ttn_payload.json` and header `{ webhook-api-key: <yourApiKey> // see .dev.env file }`
    

E.g. from the `services/web/src/test` directory run:

    curl -X POST http://localhost:5000/incomingMessages -H "webhook-api-key: tmm-api-key" -H "Content-Type: application/json" -d @dragino_ttn_payload.json

## Receiving data
Navigate to http://localhost:5000/moistureData to recive the latest moisture data, (will probably be empty).

## Insert test data
Navigate to http://localhost:5000/insertTestData to insert some random test for the last days

## Cofiguration
Configuration is done via the .dev.env file

