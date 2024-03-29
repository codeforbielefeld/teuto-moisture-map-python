from typing import Any
from influxdb_client.client.flux_table import TableList


def influx_table_windowed_values_to_dict(tables: TableList) -> dict[str, list[Any]]:
    return {
        table.records[0]["result"]: [
            {
                "start": record.values["_start"],
                "stop": record.values["_stop"],
                record.values["_measurement"]: record.values["_value"],
            }
            for record in table.records
        ]
        for table in tables
        if len(table.records) > 0
    }


def influx_table_timed_values_to_dict(tables: TableList) -> dict[str, list[Any]]:
    return {
        table.records[0]["result"]: [
            {"time": record.values["_time"], record.values["_measurement"]: record.values["_value"]}
            for record in table.records
        ]
        for table in tables
        if len(table.records) > 0
    }


def influx_table_daily_values_to_dict(tables: TableList) -> dict[str, list[Any]]:
    return {
        table.records[0]["result"]: [
            {
                "date": record.values["_time"].date(),
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
