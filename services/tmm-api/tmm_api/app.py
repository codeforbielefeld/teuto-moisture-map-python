# app.py
from typing import Union
from fastapi import FastAPI, Form, Header, Query, Response
from fastapi.responses import HTMLResponse
from tmm_api.export.sensor_report import ReportResolution, SensorReport, sensor_report
from .common.influx import get_influx_client
from .common.secrets import get_secret
import os

from .export.map_overview import export_moisture_map_data

from .ttn import handle_ttn_message, write_test_data


# ===========
# Config
# ===========

apikey = get_secret("TMM_API_KEY")


app = FastAPI()

# =====================
# Webhook web interface
# =====================


@app.post("/incomingMessages", status_code=201)
def incoming_messages(
    message: dict, response: Response, webhook_api_key: Union[str, None] = Header(None)  # noqa: B008
):
    """
    This method accepts JSON payloads from TTN, unmarshals the required information and persists them
    """

    if apikey is None or webhook_api_key == apikey:
        handle_ttn_message(message)
        return message
    else:
        response.status_code = 415
        return {"error": "Unauthorized"}


# ============
# Data exports
# ============


@app.get("/moistureData")
def moisture_data(days: int = 1):
    """
    This method exports the moisture data for the current day.
    """
    return export_moisture_map_data(days)


@app.get("/sensorData/{sensor}", response_model=SensorReport)
def sensor_data(
    sensor,
    records: int = Query(7, gt=0, le=31),  # noqa: B008
    resolution: ReportResolution = ReportResolution.DAILY,
):
    """
    This method exports the sensor report for a given sensor.
    """
    return sensor_report(sensor, records=records, resolution=resolution)


# =====================
# Development utilities
# =====================

development_mode = os.environ.get("DEVELOPMENT_MODE")
if development_mode == "true":
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/insertTestData")
    def post_insert_test_data(days: int = Form(), devices: int = Form(), measurements: int = Form()):  # noqa: B008
        """
        This method writes test data into the influx database for test purposes
        """
        write_test_data(devices, days, measurements)
        return "Success"

    @app.get("/insertTestData", response_class=HTMLResponse)
    def get_insert_test_data():
        """
        This method writes test data into the influx database for test purposes
        """
        return """
        <!doctype html>
        <html>
            <header><title>Insert test data</title></header>
            <body>
                <form action="" method=post enctype=multipart/form-data>
                    Days:<input name="days" value=1 />
                    Devices: <input name="devices" value=5 />
                    Measurements per day: <input name="measurements" value=24 />
                    <input type=submit value="Insert" />
                </form>
            </body>
        </html>
        """


# =============
# Status checks
# =============


@app.get("/internal/health/self")
def health():
    return "Ok"


@app.get("/internal/health/int")
def health_int():
    influx = get_influx_client()
    assert influx.ping()
    return "Ok"
