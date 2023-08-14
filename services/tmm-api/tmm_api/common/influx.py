import os
from influxdb_client import InfluxDBClient
from tmm_api.common.secrets import get_secret


def get_influx_client() -> InfluxDBClient:
    config_file = os.environ.get("INFLUX_CONFIG_FILE")
    if config_file:
        return InfluxDBClient.from_config_file(config_file)
    return InfluxDBClient(
        url=get_secret("INFLUXDB_V2_URL"),
        token=get_secret("INFLUXDB_V2_TOKEN"),
        org=get_secret("INFLUXDB_V2_ORG"),
    )
