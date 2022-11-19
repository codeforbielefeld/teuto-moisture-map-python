from typing import Any

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


def sensor_report(sensor: str) -> dict[str, list[Any]]:
    with get_influx_client() as client:
        q, p = query(sensor, get_bucket())
        tables = client.query_api().query(query=q, params=p)
        return influx_table_daily_values_to_dict(tables)
