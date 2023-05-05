from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from tmm_api.common.influx import get_influx_client
from tmm_api.common.secrets import get_secret


measurement = "soil"
fieldname = "soil_moisture"
bucket = get_secret("TMM_BUCKET")


@dataclass
class Record:
    device: str
    altitude: float | None
    latitude: float
    longitude: float
    soil_moisture: float


@dataclass
class MapData:
    records: list[Record]
    timestamp: datetime


def export_moisture_map_data(days: int = 1) -> MapData:
    start = f"-{days}d"

    query = f"""
    from(bucket: "{bucket}")
    |> range(start: {start})
    |> filter(fn: (r) => r["_measurement"] == "{measurement}")
    |> filter(fn: (r) => r["_field"] == "{fieldname}")    
    |> filter(fn: (r) => exists r.device and exists r.latitude and exists r.longitude)
    |> aggregateWindow(every: inf , fn: mean)
    |> last()
    """
    with get_influx_client() as client:
        query_api = client.query_api()
        results = query_api.query(query=query)

        return MapData(
            records=[
                Record(
                    device=record.values["device"],
                    soil_moisture=record.values["_value"],
                    latitude=float(record.values["latitude"]),
                    longitude=float(record.values["longitude"]),
                    altitude=maybe_float(record.values.get("altitude")),
                )
                for result in results
                for record in result.records
            ],
            timestamp=datetime.now().astimezone(ZoneInfo("Europe/Berlin")),
        )


def maybe_float(x) -> float | None:
    return float(x) if x is not None else None
