import os

_query: str | None = None


def _get_query() -> str:
    global _query
    if _query is None:
        query_file = os.path.join(os.path.dirname(__file__), "sensor_report.flux")
        with open(query_file, "r") as file:
            _query = file.read()
    return _query


def query(sensor: str, bucket: str):
    p = {"_bucket": bucket, "_device": sensor}
    return _get_query(), p
