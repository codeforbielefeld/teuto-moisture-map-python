import os
from datetime import datetime, time
from typing import List

from influxdb_client import InfluxDBClient, Point

from dwd_import.models import Device, MoistureMeasurement
from . import DeviceDB, MoistureDB


class InfluxDB(DeviceDB, MoistureDB):
    def __init__(self) -> None:
        super().__init__()
        self.bucket = os.environ.get("TMM_BUCKET")

    def get_influx_client(self):
        return InfluxDBClient.from_env_properties()

    def get_devices(self) -> List[Device]:
        query = f"""from(bucket: "{self.bucket}")
        |> range(start: -7d)
        |> filter(fn: (r) => r["_measurement"] == "moisture")
        |> filter(fn: (r) => r["_field"] == "latitude" or r["_field"] == "longitude")  
        |> group(columns: ["device","_field"])
        |> last()
        |> pivot(columnKey: ["_field"], rowKey:["_start", "_stop", "_time","device"], valueColumn: "_value"  )
        |> group()
        """

        with self.get_influx_client() as client:
            result = client.query_api().query(query=query)

            return [
                Device(
                    record.values['device'],
                    record.values['longitude'],
                    record.values['latitude']
                ) for record in result[0].records
            ]

    def write_moisture(self, measurements: List[MoistureMeasurement]):
        points = (Point("dwd_moisture")
                  .tag("device", data.device.device_id)
                  .field("percent", data.percent)
                  .time(datetime.combine(data.date, time()))
                  for data in measurements)

        with self.get_influx_client() as client:
            with client.write_api() as write_api:
                write_api.write(bucket=self.bucket, record=points)
