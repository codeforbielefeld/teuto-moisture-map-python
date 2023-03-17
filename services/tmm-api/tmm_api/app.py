# app.py
from fastapi import FastAPI, Form, Header, Query, Response, Path
from fastapi.responses import HTMLResponse, PlainTextResponse
from tmm_api.common.auth import get_digest, is_auth
from tmm_api.export.sensor_report import ReportResolution, SensorReport, sensor_report
from tmm_api.ttn.dragino import DraginoTtnMessage
from tmm_api.ttn.payload import parse_payload
from .common.influx import get_influx_client
from .common.secrets import get_secret
import os

from .export.map_overview import export_moisture_map_data

from tmm_api import ttn


# ===========
# Config
# ===========

apikey = get_secret("TMM_API_KEY")


app = FastAPI()

# =====================
# Webhook web interface
# =====================
write_enabled = os.environ.get("ENABLE_WRITE")
if write_enabled == "true":

    @app.post("/incomingMessages", status_code=201)
    def incoming_messages(message: dict, response: Response, webhook_api_key: str = Header()):  # noqa: B008
        """
        This method accepts JSON payloads from TTN, unmarshals the required information and persists them
        """
        data = parse_payload(message)
        user = data["device_id"]

        if is_auth(user, webhook_api_key):
            ttn.write_data(data)
            return message
        else:
            response.status_code = 415
            return {"error": "Unauthorized"}

    @app.post("/ttn/dragino", status_code=201)
    def ttn_dragino(
        message: DraginoTtnMessage, response: Response, X_Downlink_Apikey: str = Header()  # noqa: B008,N803
    ):
        if not is_auth(message.end_device_ids.device_id, X_Downlink_Apikey):
            response.status_code = 415
            return {"error": "Unauthorized"}
        return message


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
        ttn.write_test_data(devices, days, measurements)
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

    @app.get("/genKey/{user}", response_class=PlainTextResponse)
    def gen_key(user: str = Path()):  # noqa: B008
        return get_digest(user)


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
