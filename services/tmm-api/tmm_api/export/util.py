from typing import Any
from influxdb_client.client.flux_table import TableList


def influx_table_timed_values_to_dict(tables: TableList) -> dict[str, list[Any]]:
    return {
        table.records[0]["result"]: [
            {"time": record.values["_time"].isoformat(), record.values["_measurement"]: record.values["_value"]}
            for record in table.records
        ]
        for table in tables
        if len(table.records) > 0
    }


def influx_table_daily_values_to_dict(tables: TableList) -> dict[str, list[Any]]:
    return {
        table.records[0]["result"]: [
            {
                "date": record.values["_time"].strftime("%Y-%m-%d"),
                record.values["_measurement"]: record.values["_value"],
            }
            for record in table.records
        ]
        for table in tables
        if len(table.records) > 0
    }


def influx_table_values_to_dict(tables: TableList) -> dict[str, list[Any]]:
    return {
        table.records[0]["result"]: [record.values["_value"] for record in table.records]
        for table in tables
        if len(table.records) > 0
    }
