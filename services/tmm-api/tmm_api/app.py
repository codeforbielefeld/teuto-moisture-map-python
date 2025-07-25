# app.py
from logging import StreamHandler, getLogger
import logging
from threading import Lock
from cachetools import TTLCache, cached
from fastapi import FastAPI, Form, Header, Query, Path, Request
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    request_validation_exception_handler as _request_validation_exception_handler,
)
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse

from tmm_api.common.auth import get_digest, is_auth
from tmm_api.export.sensor_report import ReportResolution, SensorReport, sensor_report
from tmm_api.domain.SoilMeasurement import SoilMeasurement
from tmm_api.ttn.TTNMessage import TTNMessage
from .common.influx import get_influx_client
import os

from .export.map_overview import MapData, export_moisture_map_data

from tmm_api.ttn.test_data import write_test_data


app = FastAPI(title="BodenfeuchteAPI")

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(StreamHandler())
logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")


# =====================
# Webhook web interface
# =====================


write_enabled = os.environ.get("ENABLE_WRITE")
if write_enabled == "true":

    @app.post(
        "/measurement/ttn",
        status_code=201,
        response_model=SoilMeasurement,
        responses={401: {}},
    )
    def ttn_dragino(message: TTNMessage, TMM_APIKEY: str = Header()):  # noqa: B008,N803
        logger.info(f"Device: {message.end_device_ids.device_id}, API_KEY: {TMM_APIKEY}")
        if not is_auth(message.end_device_ids.device_id, TMM_APIKEY):
            return JSONResponse(status_code=401, content={"error": "Unauthorized"})
        measurement = message.to_measurement()
        measurement.write_to_influx()
        return measurement


# ============
# Data exports
# ============


@app.get("/mapData", response_model=MapData, response_model_exclude_none=True)
@cached(cache=TTLCache(maxsize=1000, ttl=600), lock=Lock())
def map_data(days: int = 1):
    """
    This method exports the moisture data for the current day.
    """
    return export_moisture_map_data(days)


@app.get("/sensorData/{sensor}", response_model=SensorReport)
@cached(cache=TTLCache(maxsize=1000, ttl=600), lock=Lock())
def sensor_data(
    sensor,
    records: int = Query(7, gt=0, le=31),  # noqa: B008
    resolution: ReportResolution = ReportResolution.DAILY,
):
    """
    This method exports the sensor report for a given sensor.
    """
    return sensor_report(sensor, records=records, resolution=resolution)


# ==================
# Exception handlers
# ==================


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    body = exc.body
    logger.info(f"Request validation failed.\n Path: {request.url},\n Errors: {exc.errors()},\n Body: {body}")
    return await _request_validation_exception_handler(request, exc)


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
