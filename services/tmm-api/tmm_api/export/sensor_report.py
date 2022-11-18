import json

from tmm_api.common.influx import get_influx_client
from tmm_api.common.secrets import get_secret_or_fail
from tmm_api.export.util import influx_table_daily_values_to_dict
from .queries.sensor_report import query

bucket = get_secret_or_fail("TMM_BUCKET")


def sensor_report(sensor: str) -> str:
    with get_influx_client() as client:
        q, p = query(sensor, bucket)
        tables = client.query_api().query(query=q, params=p)
        return json.dumps(influx_table_daily_values_to_dict(tables))
