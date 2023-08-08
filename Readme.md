# Teuto Moisture Map (Python)

## Running the application in development mode

Simply run:

    docker compose up --build tmm-api

Now the TMM API is reachable at localhost:5000 and an InfluxDB is reachable at localhost:8086.

## API Doc

Navigate to <http://localhost:5000/docs>.

## Post data

You can post new examples via <http://localhost:5000/measurement/ttn> with json body eg. `services/ttm-api/test/dragino_ttn_payload.json` and header `{ webhook-api-key: <yourApiKey> // see /examples/tmm_api_key file }`

E.g. from the `services/ttm-api/test` directory run:

    curl -X POST http://localhost:5000/measurement/ttn -H "webhook-api-key: tmm-api-key" -H "Content-Type: application/json" -d @dragino_ttn_payload.json

## Retrieving data

Navigate to <http://localhost:5000/mapData> to retrieve the latest moisture data, (will probably be empty).

## Insert test data

Navigate to <http://localhost:5000/insertTestData> to insert some random test for the last days

## Running the services without Docker

Run the individual services as indicated in there individual Readmes using poetry.
