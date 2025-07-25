from datetime import datetime, timedelta
from random import random
from collections.abc import Generator

from tmm_api.domain.SoilMeasurement import SoilMeasurement


def construct_data(device_id, lon, lat, received_at, moisture, temperature, conductivity) -> SoilMeasurement:
    return SoilMeasurement(
        soil_moisture=moisture,
        soil_conductivity=conductivity,
        soil_temperature=temperature,
        battery=0.8,
        latitude=lat,
        longitude=lon,
        altitude=17.42,
        device=str(device_id),
        device_brand="test_brand",
        device_model="test_model",
        time=received_at,
    )


def generate_test_data(num_devices: int, days: int, num_measurements: int = 24) -> Generator[SoilMeasurement]:
    last = datetime.now()
    for device in range(num_devices):
        lat = 52.01 + (random() - 0.5) / 2
        lon = 8.542732 + (random() - 0.5)
        for day in range(days):
            for measurement in range(num_measurements):
                received_at = last - timedelta(days=day + measurement / num_measurements)
                yield construct_data(
                    device,
                    lon,
                    lat,
                    received_at,
                    random() * 10 + random() * random() * 90,
                    random() * 30,
                    random(),
                )


def write_test_data(num_devices: int, days: int, num_measurements: int = 24):
    for data in generate_test_data(num_devices, days, num_measurements):
        data.write_to_influx()
