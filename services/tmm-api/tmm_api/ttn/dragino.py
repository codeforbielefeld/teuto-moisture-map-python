from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class TtnEndDeviceIds:
    device_id: str


@dataclass
class TtnDragionoDecodedPayload:
    Bat: str
    conduct_SOIL: str  # noqa: N815
    temp_SOIL: str  # noqa: N815
    water_SOIL: str  # noqa: N815


@dataclass
class TtnDragionoRxMetadata:
    time: datetime


@dataclass
class TtnDragionoUserLocations:
    latitude: float
    longitude: float
    altitude: Union[float, None] = None


@dataclass
class TtnDragionoLocations:
    user: TtnDragionoUserLocations


@dataclass
class TtnDragionoUplinkMessage:
    decoded_payload: TtnDragionoDecodedPayload
    rx_metadata: list[TtnDragionoRxMetadata]
    locations: TtnDragionoLocations
    received_at: datetime


@dataclass
class DraginoTtnMessage:
    end_device_ids: TtnEndDeviceIds
    uplink_message: TtnDragionoUplinkMessage
