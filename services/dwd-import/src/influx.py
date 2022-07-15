import os
from datetime import datetime, time
from typing import List

from influxdb_client import InfluxDBClient, Point

from models import Device, MoistureMeasurement


bucket = os.environ.get("TMM_BUCKET")


def get_influx_client():
    return InfluxDBClient.from_env_properties()


def get_devices() -> List[Device]:
    query = f"""from(bucket: "{bucket}")
    |> range(start: -7d)
    |> filter(fn: (r) => r["_measurement"] == "moisture")
    |> filter(fn: (r) => r["_field"] == "latitude" or r["_field"] == "longitude")  
    |> group(columns: ["device","_field"])
    |> last()
    |> pivot(columnKey: ["_field"], rowKey:["_start", "_stop", "_time","device"], valueColumn: "_value"  )
    |> group()
    """

    with get_influx_client() as client:
        result = client.query_api().query(query=query)

        return list(map(lambda record:
                        Device(
                            record.values['device'],
                            record.values['longitude'],
                            record.values['latitude']
                        ),
                        result[0].records))


def write_moisture(measurements: List[MoistureMeasurement]):
    points = map(lambda data:
                 Point("dwd_moisture")
                 .tag("device", data.device.device_id)
                 .field("percent", data.percent)
                 .time(datetime.combine(data.date, time())),
                 measurements)

    with get_influx_client() as client:
        with client.write_api() as write_api:
            write_api.write(bucket=bucket, record=points)
