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
    soil_conductivity: float | None
    soil_temperature: float | None
    battery: float | None
    last_update: datetime


@dataclass
class MapData:
    records: list[Record]
    timestamp: datetime


def export_moisture_map_data(days: int = 1) -> MapData:
    start = f"-{days}d"

    query = f"""
    import "join"
    data = from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")
        |> filter(fn: (r) => exists r.device and exists r.latitude and exists r.longitude)
        |> aggregateWindow(every: inf , fn: mean)
        |> last()
        |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
        |> filter(fn: (r) => exists r.device and exists r.latitude and exists r.longitude and exists r.soil_moisture)
        |> group(columns: ["device"])

    //data |> yield (name: "data")

    times = from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")    
        |> group(columns: ["device"])
        |> last()
        |> keep(columns: ["_time", "device"])

    //times |> yield (name: "times")
    
    joined = join.inner(
        left: data,
        right: times,
        on: (l, r) => l.device == r.device,
        as: (l, r) => ({{l with last_update: r._time}}),
    )
    
    joined |> yield(name: "joined")
    """
    with get_influx_client() as client:
        query_api = client.query_api()
        results = query_api.query(query=query)

        return MapData(
            records=[
                Record(
                    device=record.values["device"],
                    soil_moisture=record.values["soil_moisture"],
                    latitude=float(record.values["latitude"]),
                    longitude=float(record.values["longitude"]),
                    altitude=maybe_float(record.values.get("altitude")),
                    soil_conductivity=record.values.get("soil_conductivity"),
                    soil_temperature=record.values.get("soil_temperature"),
                    battery=record.values.get("battery"),
                    last_update=record.values["last_update"],
                )
                for result in results
                for record in result.records
            ],
            timestamp=datetime.now().astimezone(ZoneInfo("Europe/Berlin")),
        )


def maybe_float(x) -> float | None:
    return float(x) if x is not None else None
