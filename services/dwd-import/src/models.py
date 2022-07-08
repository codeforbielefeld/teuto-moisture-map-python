from datetime import date
from typing import NamedTuple


class Device(NamedTuple):
    device_id: str
    lon: float
    lat: float


class Measurement(NamedTuple):
    device: Device
    percent: int
    date: date
