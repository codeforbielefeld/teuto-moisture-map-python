from dataclasses import dataclass
from datetime import datetime
from typing import Union

from influxdb_client import Point
from tmm_api.common.influx import get_influx_client
from tmm_api.common.secrets import get_secret
from influxdb_client.client.write_api import SYNCHRONOUS


@dataclass
class SoilMeasurement:
    soil_moisture: float
    soil_conductivity: Union[float, None]
    soil_temperature: Union[float, None]
    battery: Union[float, None]
    latitude: float
    longitude: float
    altitude: Union[float, None]
    device: str
    device_brand: str
    device_model: str
    time: datetime

    def to_data_point(self) -> Point:
        point = (
            Point("soil")
            .tag("device", self.device)
            .tag("device_brand", self.device_brand)
            .tag("device_model", self.device_model)
            .tag("latitude", self.latitude)
            .tag("longitude", self.longitude)
            .field("soil_moisture", self.soil_moisture)
            .time(self.time)
        )
        if self.altitude:
            point = point.tag("altitude", self.altitude)
        if self.soil_conductivity:
            point = point.field("soil_conductivity", self.soil_conductivity)
        if self.soil_temperature:
            point = point.field("soil_temperature", self.soil_temperature)
        if self.battery:
            point = point.field("battery", self.battery)
        return point

    def write_to_influx(self):
        bucket = get_secret("TMM_BUCKET")
        with get_influx_client() as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=bucket, record=self.to_data_point())
