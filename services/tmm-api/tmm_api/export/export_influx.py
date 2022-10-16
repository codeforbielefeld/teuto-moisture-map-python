from datetime import datetime
import json

from tmm_api.common.influx import get_influx_client
from tmm_api.common.secrets import get_secret

query_type = "map"
range = "-1d"
measurement = "moisture"
fieldname = "percent"
bucket = get_secret("TMM_BUCKET")


def export_moisture_map_data():

    value_query = (
        'from(bucket: "'
        + bucket
        + '") \
    |> range(start: '
        + range
        + ') \
    |> filter(fn: (r) => \
        r._measurement == "'
        + measurement
        + '" and \
        r._field == "'
        + fieldname
        + '")'
    )

    map_query = (
        'lat = from(bucket: "'
        + bucket
        + '") \
    |> range(start: '
        + range
        + ') \
    |> filter(fn: (r) => r["_measurement"] == "'
        + measurement
        + '") \
    |> filter(fn: (r) => r["_field"] == "latitude") \
    |> aggregateWindow(every: 1d , fn: last) \
    |> last() \
    \
    long = from(bucket: "'
        + bucket
        + '") \
    |> range(start: '
        + range
        + ') \
    |> filter(fn: (r) => r["_measurement"] == "'
        + measurement
        + '") \
    |> filter(fn: (r) => r["_field"] == "longitude") \
    |> aggregateWindow(every: 1d , fn: last) \
    |> last() \
    \
    measurement = from(bucket: "'
        + bucket
        + '") \
    |> range(start: '
        + range
        + ') \
    |> filter(fn: (r) => r["_measurement"] == "'
        + measurement
        + '") \
    |> filter(fn: (r) => r["_field"] == "'
        + fieldname
        + '") \
    |> aggregateWindow(every: 1d , fn: last) \
    |> last() \
    \
    alt = from(bucket: "'
        + bucket
        + '") \
    |> range(start: '
        + range
        + ') \
    |> filter(fn: (r) => r["_measurement"] == "'
        + measurement
        + '") \
    |> filter(fn: (r) => r["_field"] == "altitude") \
    |> aggregateWindow(every: 1d , fn: last) \
    |> last() \
    \
    union(tables: [alt, lat, long, measurement]) \
    |> group(columns: ["device"], mode: "by") \
    |> pivot(rowKey: ["_time"], columnKey: ["_field"],  valueColumn: "_value") \
    |> group()'
    )

    # TODO: Implement processing of value query
    query = map_query

    if query_type == "value":
        query = value_query

    with get_influx_client() as client:

        query_api = client.query_api()
        result = query_api.query(query=query)

        jsonObj = {}

        if query_type == "map":
            mapdataArray = []
            for record in result[0].records:
                jsonRecord = {}
                jsonRecord["device"] = record.values["device"]
                jsonRecord["altitude"] = record.values["altitude"]
                jsonRecord[fieldname] = record.values[fieldname]
                jsonRecord["latitude"] = record.values["latitude"]
                jsonRecord["longitude"] = record.values["longitude"]
                if record.values[fieldname] is not None:
                    mapdataArray.append(jsonRecord)

            jsonObj["records"] = mapdataArray

        elif query_type == "value":
            valuesArray = []
            for sensor in result:
                for record in sensor.records:
                    jsonRecord = {}
                    jsonRecord["measurement"] = str(record.get_measurement())
                    jsonRecord[record.get_field()] = str(record.get_value())
                    jsonRecord["timestamp"] = str(record.get_time())
                    jsonRecord["deviceId"] = str(record.values["device"])
                    valuesArray.append(jsonRecord)
            jsonObj["values"] = valuesArray

        else:
            print("unknown query type: " + str(query_type))

        jsonObj["timestamp"] = str(datetime.now())

        return json.dumps(jsonObj)
