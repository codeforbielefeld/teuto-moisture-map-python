from logging import Logger
import os
from influxdb_client import InfluxDBClient


def get_influx_client() -> InfluxDBClient:
    config_file = os.environ.get("INFLUX_CONFIG_FILE")
    if config_file:
        return InfluxDBClient.from_config_file(config_file)
    return InfluxDBClient.from_env_properties()
