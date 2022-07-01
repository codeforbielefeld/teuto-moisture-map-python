from influxdb_client import InfluxDBClient


def get_influx_client() -> InfluxDBClient:
    return InfluxDBClient.from_env_properties()
