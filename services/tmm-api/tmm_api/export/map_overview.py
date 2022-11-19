from datetime import datetime
from typing import Collection
from zoneinfo import ZoneInfo

from tmm_api.common.influx import get_influx_client
from tmm_api.common.secrets import get_secret


measurement = "moisture"
fieldname = "percent"
bucket = get_secret("TMM_BUCKET")


def export_moisture_map_data(days: int = 1) -> dict[str, list[Collection[str]] | str]:
    start = f"-{days}d"
    window = f"{days}d"

    query = f"""
    measurement = from(bucket: "{bucket}")
    |> range(start: {start})
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")
    |> filter(fn: (r) => r["_field"] == "{fieldname}")
    |> aggregateWindow(every: {window} , fn: mean)
    |> last()

    lat = from(bucket: "{bucket}")
    |> range(start: {start})
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")
    |> filter(fn: (r) => r["_field"] == "latitude")
    |> aggregateWindow(every: {window} , fn: last)
    |> last()

    long = from(bucket: "{bucket}")
    |> range(start: {start})
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")
    |> filter(fn: (r) => r["_field"] == "longitude")
    |> aggregateWindow(every: {window} , fn: last)
    |> last()

    alt = from(bucket: "{bucket}")
    |> range(start: {start})
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")
    |> filter(fn: (r) => r["_field"] == "altitude")
    |> aggregateWindow(every: {window} , fn: last)
    |> last()

    union(tables: [alt, lat, long, measurement])
    |> group(columns: ["device"], mode: "by")
    |> pivot(rowKey: ["_time"], columnKey: ["_field"],  valueColumn: "_value")
    |> group()
    """

    with get_influx_client() as client:

        query_api = client.query_api()
        results = query_api.query(query=query)

        return {
            "records": [
                {
                    key: record.values[key]
                    for key in [
                        "device",
                        "altitude",
                        "latitude",
                        "longitude",
                        fieldname,
                    ]
                }
                for result in results
                for record in result.records
                if record.values[fieldname] is not None
            ],
            "timestamp": datetime.now().astimezone(ZoneInfo("Europe/Berlin")).isoformat(),
        }
