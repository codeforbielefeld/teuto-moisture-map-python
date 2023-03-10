from datetime import datetime
import json
from tmm_api.common.influx import get_influx_client
from tmm_api.common.secrets import get_secret

query_type = "map"
range = "-1d"
measurement = "moisture"
fieldname = "percent"
bucket = get_secret("TMM_BUCKET")


def export_moisture_map_data_legacy():
    value_query = f"""
    from(bucket: "{bucket}")
    |> range(start: {range})
    |> filter(fn: (r) =>
        r._measurement == "{measurement}" and
        r._field == "{fieldname}")"""

    map_query = f"""
    lat = from(bucket: "{bucket}")
    |> range(start: {range})
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")
    |> filter(fn: (r) => r["_field"] == "latitude")
    |> aggregateWindow(every: 1d , fn: last)
    |> last()

    long = from(bucket: "{bucket}")
    |> range(start: {range})
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")
    |> filter(fn: (r) => r["_field"] == "longitude")
    |> aggregateWindow(every: 1d , fn: last)
    |> last()

    measurement = from(bucket: "{bucket}")
    |> range(start: {range})
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")
    |> filter(fn: (r) => r["_field"] == "{fieldname}")
    |> aggregateWindow(every: 1d , fn: last)
    |> last()

    alt = from(bucket: "{bucket}")
    |> range(start: {range})
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")
    |> filter(fn: (r) => r["_field"] == "altitude")
    |> aggregateWindow(every: 1d , fn: last)
    |> last()

    union(tables: [alt, lat, long, measurement])
    |> group(columns: ["device"], mode: "by")
    |> pivot(rowKey: ["_time"], columnKey: ["_field"],  valueColumn: "_value")
    |> group()
    """

    # TODO: Implement processing of value query
    query = map_query

    if query_type == "value":
        query = value_query

    with get_influx_client() as client:
        query_api = client.query_api()
        result = query_api.query(query=query)

        json_obj = {}

        if query_type == "map":
            mapdata_array = []
            for record in result[0].records:
                json_record = {}
                json_record["device"] = record.values["device"]
                json_record["altitude"] = record.values["altitude"]
                json_record[fieldname] = record.values[fieldname]
                json_record["latitude"] = record.values["latitude"]
                json_record["longitude"] = record.values["longitude"]
                if record.values[fieldname] is not None:
                    mapdata_array.append(json_record)

            json_obj["records"] = mapdata_array

        elif query_type == "value":
            values_array = []
            for sensor in result:
                for record in sensor.records:
                    json_record = {}
                    json_record["measurement"] = str(record.get_measurement())
                    json_record[record.get_field()] = str(record.get_value())
                    json_record["timestamp"] = str(record.get_time())
                    json_record["deviceId"] = str(record.values["device"])
                    values_array.append(json_record)
            json_obj["values"] = values_array

        else:
            print("unknown query type: " + str(query_type))

        json_obj["timestamp"] = str(datetime.now())

        return json.dumps(json_obj)
