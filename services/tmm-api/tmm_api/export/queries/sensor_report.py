import os

query_file = os.path.join(os.path.dirname(__file__), "sensor_report.flux")
with open(query_file, "r") as file:
    global _query
    _query = file.read()


def query(sensor: str, bucket: str):
    p = {"_bucket": bucket, "_device": sensor}
    return _query, p
