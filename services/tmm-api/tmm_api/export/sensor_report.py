from dataclasses import dataclass
import datetime
from enum import Enum

from tmm_api.common.influx import get_influx_client
from tmm_api.common.secrets import get_secret_or_fail
from tmm_api.export.util import influx_table_timed_values_to_dict
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
    time: datetime.datetime


@dataclass
class SensorReport:
    sensor: list[MoistureMeasurement]
    peers: list[MoistureMeasurement]


class ReportResolution(str, Enum):
    HOURLY = "1h"
    THREE_HOURLY = "3h"
    SIX_HOURLY = "6h"
    DAILY = "1d"
    WEEKLY = "1w"
    MONTHLY = "4w"
    YEARLY = "1y"


def _convert_measurements(x) -> list[MoistureMeasurement]:
    return [MoistureMeasurement(moisture=m["moisture"], time=m["time"]) for m in x] if x is not None else []


def sensor_report(
    sensor: str, past_days: int = 6, resolution: ReportResolution = ReportResolution.DAILY
) -> SensorReport:
    with get_influx_client() as client:
        q, p = query(sensor, get_bucket(), past_days, resolution.value)
        tables = client.query_api().query(query=q, params=p)
        res = influx_table_timed_values_to_dict(tables)
        return SensorReport(
            sensor=_convert_measurements(res.get("sensor")), peers=_convert_measurements(res.get("peers"))
        )
