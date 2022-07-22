from datetime import date
from typing import NamedTuple


class Device(NamedTuple):
    device_id: str
    lon: float
    lat: float


class MoistureMeasurement(NamedTuple):
    device: Device
    percent: int
    date: date

class DWDStation(NamedTuple):
    station_id: str
    data_since: date
    data_until: date
    height: int
    lon: float
    lat: float
    name: str
    state: str
    historic_precipitation_dataset_url: str

class PrecipitationMeasurment(NamedTuple):
    station: DWDStation
    date: date
    preciptation: float # DWD field: RS
    form: int # DWD field: RSF
    quality: int # DWD field: QN_6

class PrecipitationAverage(NamedTuple):
    station: DWDStation
    day_in_month: int
    month_in_year: int
    preciptation: float
    since: date
    unitl: date