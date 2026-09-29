from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from zoneinfo import ZoneInfo

from tmm_api.common.influx import get_influx_client
from tmm_api.common.secrets import get_secret
from tmm_api.common.sensor_metadata import get_sensors_metadata
import typing

measurement = "soil"
fieldname = "soil_moisture"
bucket = get_secret("TMM_BUCKET")

logger = getLogger(__name__)


@dataclass
class Record:
    device: str
    altitude: float | None
    latitude: float
    longitude: float
    soil_moisture: float
    soil_conductivity: float | None
    soil_temperature: float | None
    avg_soil_moisture: float
    avg_soil_conductivity: float | None
    avg_soil_temperature: float | None
    battery: float | None
    avg_battery: float | None
    last_update: datetime
    shaded: bool | None
    depth_cm: float | None
    sealed_ground: bool | None
    note: str | None
    soil_note: str | None


@dataclass
class MapData:
    records: list[Record]
    timestamp: datetime


def export_moisture_map_data(days: int = 1) -> MapData:
    start = f"-{days}d"

    # Optional fields (e.g. soil_conductivity) may be missing entirely in the
    # queried range. Flux joins fail on missing columns, so we run two simple
    # queries and merge them by device in Python instead.
    average_query = f"""
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")
        |> aggregateWindow(every: inf, fn: mean)
        |> last()
        |> pivot(rowKey: ["device"], columnKey: ["_field"], valueColumn: "_value")
        |> drop(columns: ["_measurement", "_time", "device_brand", "device_model"])
        |> group(columns: ["device"])
    """

    latest_query = f"""
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")
        |> last()
        |> pivot(rowKey: ["device", "_time"], columnKey: ["_field"], valueColumn: "_value")
        |> drop(columns: ["_measurement", "device_brand", "device_model"])
        |> group(columns: ["device"])
    """

    with get_influx_client() as client:
        logger.debug("Executing queries to export map data")
        query_api = client.query_api()
        average_results = query_api.query(query=average_query)
        latest_results = query_api.query(query=latest_query)
        logger.debug("Retrieved results from InfluxDB")
        metadata = get_sensors_metadata()
        logger.debug(f"Retrieved metadata for {len(metadata)} sensors")

        def get_field(sensor_id, field) -> typing.Any:
            sensor = metadata.get(sensor_id)
            return sensor.get(field) if sensor else None

        averages: dict[str, dict[str, typing.Any]] = {
            record.values["device"]: record.values
            for table in average_results
            for record in table.records
            if record.values.get("device") is not None and record.values.get("soil_moisture") is not None
        }

        records: list[Record] = []
        for table in latest_results:
            for record in table.records:
                values = record.values
                device = values.get("device")
                if (
                    device is None
                    or device not in averages
                    or values.get("latitude") is None
                    or values.get("longitude") is None
                    or values.get("soil_moisture") is None
                ):
                    continue
                avg = averages[device]
                records.append(
                    Record(
                        device=device,
                        latitude=float(values["latitude"]),
                        longitude=float(values["longitude"]),
                        altitude=maybe_float(values.get("altitude")),
                        soil_moisture=values["soil_moisture"],
                        soil_conductivity=values.get("soil_conductivity"),
                        soil_temperature=values.get("soil_temperature"),
                        battery=values.get("battery"),
                        avg_battery=avg.get("battery"),
                        avg_soil_moisture=avg["soil_moisture"],
                        avg_soil_conductivity=avg.get("soil_conductivity"),
                        avg_soil_temperature=avg.get("soil_temperature"),
                        last_update=values["_time"],
                        shaded=get_field(device, "shaded"),
                        depth_cm=get_field(device, "depth_cm"),
                        sealed_ground=get_field(device, "sealed_ground"),
                        note=get_field(device, "note"),
                        soil_note=get_field(device, "soil_note"),
                    )
                )

        return MapData(
            records=records,
            timestamp=datetime.now().astimezone(ZoneInfo("Europe/Berlin")),
        )


def maybe_float(x) -> float | None:
    return float(x) if x not in (None, "") else None
