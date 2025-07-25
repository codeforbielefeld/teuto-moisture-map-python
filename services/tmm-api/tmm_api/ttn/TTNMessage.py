from dataclasses import dataclass
from datetime import datetime, UTC
import re
from typing import Annotated, Union
from pydantic import BaseModel, ConfigDict, StringConstraints
from tmm_api.domain.SoilMeasurement import SoilMeasurement

FLOAT_REGEX = re.compile(r"^-?\d+[.]*\d*")
FloatStringWithUnit = Annotated[str, StringConstraints(pattern=FLOAT_REGEX)]


FloatValue = Union[FloatStringWithUnit, float]  # noqa: U007
MaybeFloatValue = Union[FloatValue, None]  # noqa: U007


@dataclass
class EndDeviceIds:
    device_id: str


class VersionIds(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"brand_id": "dragino", "model_id": "lse01"},
        }
    )

    brand_id: str
    model_id: str


class DecodedPayload(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"Bat": "3.304 V", "conduct_SOIL": "57 uS/cm", "temp_SOIL": "7.87 °C", "water_SOIL": "23.42 %"}
        }
    )

    Bat: MaybeFloatValue
    conduct_SOIL: MaybeFloatValue  # noqa: N815
    temp_SOIL: MaybeFloatValue  # noqa: N815
    water_SOIL: FloatValue  # noqa: N815


@dataclass
class RxMetadata:
    time: datetime | None = None


class UserLocations(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"latitude": 52.014, "longitude": 8.526, "altitude": 62.1}})

    latitude: float
    longitude: float
    altitude: float | None = None


@dataclass
class Locations:
    user: UserLocations


@dataclass
class UplinkMessage:
    decoded_payload: DecodedPayload
    rx_metadata: list[RxMetadata | None]
    locations: Locations
    received_at: datetime
    version_ids: VersionIds


class TTNMessage(BaseModel):
    received_at: datetime
    end_device_ids: EndDeviceIds
    uplink_message: UplinkMessage

    def to_measurement(self) -> SoilMeasurement:
        return SoilMeasurement(
            soil_moisture=parse_float_value(self.uplink_message.decoded_payload.water_SOIL),
            soil_conductivity=parse_maybe_float_value(self.uplink_message.decoded_payload.conduct_SOIL),
            soil_temperature=parse_maybe_float_value(self.uplink_message.decoded_payload.temp_SOIL),
            battery=parse_maybe_float_value(self.uplink_message.decoded_payload.Bat),
            latitude=self.uplink_message.locations.user.latitude,
            longitude=self.uplink_message.locations.user.longitude,
            altitude=self.uplink_message.locations.user.altitude or 0.0,
            device=self.end_device_ids.device_id,
            device_brand=self.uplink_message.version_ids.brand_id,
            device_model=self.uplink_message.version_ids.model_id,
            time=min(
                datetime.now(UTC),
                self.received_at,
                self.uplink_message.received_at,
                *[x.time for x in self.uplink_message.rx_metadata if x is not None and x.time is not None],
            ),
        )


def parse_float_value(x: FloatValue) -> float:
    if isinstance(x, float):
        return x
    match = FLOAT_REGEX.search(x)
    assert match
    return float(match.group())


def parse_maybe_float_value(x: MaybeFloatValue) -> float | None:
    return parse_float_value(x) if x is not None else None
