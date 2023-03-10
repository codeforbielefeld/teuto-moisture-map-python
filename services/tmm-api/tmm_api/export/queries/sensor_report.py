import os
from typing import Union

_query: Union[str, None] = None


def _get_query() -> str:
    global _query
    if _query is None:
        query_file = os.path.join(os.path.dirname(__file__), "sensor_report.flux")
        with open(query_file, "r") as file:
            _query = file.read()
    return _query


def query(sensor: str, bucket: str, num: int = 7, window: str = "1d"):
    p = {"_bucket": bucket, "_device": sensor, "_records": num, "_windowSize": window}
    return _get_query(), p
