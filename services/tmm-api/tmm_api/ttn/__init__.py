from logging import Logger
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from ..common.influx import get_influx_client
from ..common.secrets import get_secret
from .examples import generate_test_data
from .payload import parse_payload


# ===========
# Persistence
# ===========

bucket = get_secret("TMM_BUCKET")


def create_point_with_common_attributes(name, data):
    """
    Sets common attributes from a sensor to a newly created Point
    """
    return (
        Point(name)
        .tag("device", data["device_id"])
        .tag("device_brand", data["device_brand"])
        .tag("device_model", data["device_model"])
        .field("latitude", data["latitude"])
        .field("longitude", data["longitude"])
        .field("altitude", data["altitude"])
        .time(data["received_at"])
    )


def write_data(data: dict):
    """
    Writes a parsed payload to the database
    """
    with get_influx_client() as client:

        write_api = client.write_api(write_options=SYNCHRONOUS)

        bat_point = (
            create_point_with_common_attributes("battery", data)
            .field("voltage", data["battery"])
            .field("unit", data["battery_unit"])
        )
        conductivity_point = (
            create_point_with_common_attributes("conductivity", data)
            .field("uS/cm", data["conductivity"])
            .field("unit", data["conductivity_unit"])
        )
        temp_point = (
            create_point_with_common_attributes("temperature", data)
            .field("celsius", data["temperature"])
            .field("unit", data["temperature_unit"])
        )
        moisture_point = (
            create_point_with_common_attributes("moisture", data)
            .field("percent", data["moisture"])
            .field("unit", data["moisture_unit"])
        )

        write_api.write(bucket=bucket, record=bat_point)
        write_api.write(bucket=bucket, record=conductivity_point)
        write_api.write(bucket=bucket, record=temp_point)
        write_api.write(bucket=bucket, record=moisture_point)


def handle_ttn_message(json: dict, logger: Logger):
    """
    Handle an incomming TTN message
    """
    logger.info("Received message: %s", str(json))

    data = parse_payload(json)
    logger.info("Parsed payload: %s", str(data))

    logger.info("Writing to bucket: %s", bucket)
    write_data(data)


def write_test_data(num_devices: int, days: int, num_measurments: int = 24):
    for data in generate_test_data(num_devices, days, num_measurments):
        write_data(data)
