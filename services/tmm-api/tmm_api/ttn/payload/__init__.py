from .PayloadParser import PayloadParser
from .DraginoLSE01 import DraginoLSE01

"""
This module produces PayloadParser instances, depending on the brand and model
of a sensor.

It keeps a local cache of instantiated parsers and returns the same instance,
once it has been created.
"""


def parse_payload(payload: dict) -> dict:
    common_attributes = _parse_common_attributes(payload)
    specific_attributes = _get_parser_for_model(
        common_attributes["device_brand"], common_attributes["device_model"]
    ).parse_payload(payload)
    return dict(**common_attributes, **specific_attributes)


__parsers: dict[str, PayloadParser] = {}


def _get_instance(brand: str, model: str) -> PayloadParser:
    return __parsers[brand + "_" + model]


def _set_instance(brand: str, model: str, instance: PayloadParser):
    __parsers[brand + "_" + model] = instance


def _get_parser_for_model(brand: str, model: str) -> PayloadParser:
    if brand == "dragino":
        if model == "lse01":
            try:
                return _get_instance(brand=brand, model=model)
            except Exception:
                dragino = DraginoLSE01()
                _set_instance(brand=brand, model=model, instance=dragino)

    return _get_instance(brand=brand, model=model)


def _parse_common_attributes(json: dict) -> dict:
    device_id = json["end_device_ids"]["device_id"]
    device_brand = json["uplink_message"]["version_ids"]["brand_id"]
    device_model = json["uplink_message"]["version_ids"]["model_id"]

    received_at = json["received_at"]

    try:
        latitude = float(json["uplink_message"]["locations"]["user"]["latitude"])
    except Exception:
        latitude = None

    try:
        longitude = float(json["uplink_message"]["locations"]["user"]["longitude"])
    except Exception:
        longitude = None

    try:
        altitude = float(json["uplink_message"]["locations"]["user"]["altitude"])
    except Exception:
        altitude = 0.0

    return {
        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude,
        "device_id": device_id,
        "device_brand": device_brand,
        "device_model": device_model,
        "received_at": received_at,
    }
