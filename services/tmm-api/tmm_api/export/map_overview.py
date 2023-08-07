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
    avg_soil_moisture: float
    avg_soil_conductivity: float | None
    avg_soil_temperature: float | None
    battery: float | None
    avg_battery: float | None
    last_update: datetime


@dataclass
class MapData:
    records: list[Record]
    timestamp: datetime


def export_moisture_map_data(days: int = 1) -> MapData:
    start = f"-{days}d"

    query = f"""
    import "join"
    average = from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")
        |> aggregateWindow(every: inf , fn: mean)
        |> last()
        |> pivot(rowKey: ["device"], columnKey: ["_field"], valueColumn: "_value")
        |> filter(fn: (r) => exists r.device and exists r.latitude and exists r.longitude and exists r.soil_moisture)
        |> drop(columns: ["_measurement","_time", "device_brand", "device_model"])
        |> group(columns: ["device"])

        //average |> yield (name: "average")

        latest = from(bucket: "tmm-bucket")
        |> range(start: {start})
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")
        |> last()
        |> pivot(rowKey: ["device","_time"], columnKey: ["_field"], valueColumn: "_value")
        |> filter(fn: (r) => exists r.device and exists r.latitude and exists r.longitude and exists r.soil_moisture)
        |> drop(columns: ["_measurement", "device_brand", "device_model"])
        |> group(columns: ["device"])

        //latest |> yield(name: "latest")
        
        joined = join.inner(
            left: average,
            right: latest,
            on: (l, r) => l.device == r.device,
            as: (l, r) => ({{r with last_update: r._time, avg_soil_moisture: l.soil_moisture, avg_soil_temperature: l.soil_temperature, avg_soil_conductivity: l.soil_conductivity, avg_battery: l.battery}}),
        ) |> drop(columns: ["_time"])
                
        joined |> yield(name: "joined")
    """
    with get_influx_client() as client:
        query_api = client.query_api()
        results = query_api.query(query=query)

        return MapData(
            records=[
                Record(
                    device=record.values["device"],
                    latitude=float(record.values["latitude"]),
                    longitude=float(record.values["longitude"]),
                    altitude=maybe_float(record.values.get("altitude")),
                    soil_moisture=record.values["soil_moisture"],
                    soil_conductivity=record.values.get("soil_conductivity"),
                    soil_temperature=record.values.get("soil_temperature"),
                    battery=record.values.get("battery"),
                    avg_battery=record.values.get("avg_battery"),
                    avg_soil_moisture=record.values["avg_soil_moisture"],
                    avg_soil_conductivity=record.values.get("avg_soil_conductivity"),
                    avg_soil_temperature=record.values.get("avg_soil_temperature"),
                    last_update=record.values["last_update"],
                )
                for result in results
                for record in result.records
            ],
            timestamp=datetime.now().astimezone(ZoneInfo("Europe/Berlin")),
        )


def maybe_float(x) -> float | None:
    return float(x) if x is not None else None
