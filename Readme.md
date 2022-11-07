# Teuto Moisture Map (Python)

## Running the application in development mode

Simply run:

    docker compose up --build tmm-api

Now the TMM API is reachable at localhost:5000 and an InfluxDB is reachable at localhost:8086.

## Post data

You can post new examples via <http://localhost:5000/incomingMessages> with json body eg. `services/ttm-api/test/dragino_ttn_payload.json` and header `{ webhook-api-key: <yourApiKey> // see .dev.env file }`

E.g. from the `services/ttm-api/test` directory run:

    curl -X POST http://localhost:5000/incomingMessages -H "webhook-api-key: tmm-api-key" -H "Content-Type: application/json" -d @dragino_ttn_payload.json

## Retrieving data

Navigate to <http://localhost:5000/moistureData> to retrieve the latest moisture data, (will probably be empty).

## Insert test data

Navigate to <http://localhost:5000/insertTestData> to insert some random test for the last days

## Running the services without Docker

Run the individual services as indicated in there individual Readmes using poetry.
