import os
from datetime import datetime, time

from influxdb_client import InfluxDBClient, Point

from dwd_import.models import Device, MoistureMeasurement
from . import DeviceDB, MoistureDB


class InfluxDB(DeviceDB, MoistureDB):
    def __init__(self) -> None:
        super().__init__()
        self.bucket = os.environ.get("TMM_BUCKET")

    def get_influx_client(self):
        return InfluxDBClient.from_env_properties()

    def get_devices(self) -> list[Device]:
        query = f"""from(bucket: "{self.bucket}")
            |> range(start: -7d)
            |> filter(fn: (r) => r["_measurement"] == "soil")        
            |> group(columns: ["device"])
            |> last()        
            |> keep(columns: ["device", "latitude", "longitude"])
            |> group()
        """

        with self.get_influx_client() as client:
            result = client.query_api().query(query=query)

            return [
                Device(
                    record.values["device"],
                    float(record.values["longitude"]),
                    float(record.values["latitude"]),
                )
                for record in result[0].records
            ]

    def write_moisture(self, measurements: list[MoistureMeasurement]):
        points = (
            Point("dwd_moisture")
            .tag("device", data.device.device_id)
            .field("percent", data.percent)
            .time(datetime.combine(data.date, time()))
            for data in measurements
        )

        with self.get_influx_client() as client:
            with client.write_api() as write_api:
                write_api.write(bucket=self.bucket, record=points)
