from dataclasses import dataclass
import datetime

from tmm_api.common.influx import get_influx_client
from tmm_api.common.secrets import get_secret_or_fail
from tmm_api.export.util import influx_table_daily_values_to_dict
from .queries.sensor_report import query

_bucket: str | None = None


def get_bucket() -> str:
    global _bucket
    if _bucket is None:
        _bucket = get_secret_or_fail("TMM_BUCKET")
    return _bucket


@dataclass
class MoistureMeasurement:
    moisture: float
    date: datetime.date


@dataclass
class SensorReport:
    sensor: list[MoistureMeasurement]
    peers: list[MoistureMeasurement]


def _convert_measurements(x) -> list[MoistureMeasurement]:
    return [MoistureMeasurement(moisture=m["moisture"], date=m["date"]) for m in x] if x is not None else []


def sensor_report(sensor: str) -> SensorReport:
    with get_influx_client() as client:
        q, p = query(sensor, get_bucket())
        tables = client.query_api().query(query=q, params=p)
        res = influx_table_daily_values_to_dict(tables)
        return SensorReport(
            sensor=_convert_measurements(res.get("sensor")), peers=_convert_measurements(res.get("peers"))
        )
