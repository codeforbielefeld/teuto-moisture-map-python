# app.py
from .common.influx import get_influx_client
from .common.secrets import get_secret
from flask import Flask, request
import os

from .export.map_overview import export_moisture_map_data

from .ttn import handle_ttn_message, write_test_data


# ===========
# Config
# ===========

apikey = get_secret("TMM_API_KEY")


app = Flask(__name__)

# =====================
# Webhook web interface
# =====================


@app.post("/incomingMessages")
def incomingMessages():
    """
    This method accepts JSON payloads from TTN, unmarshals the required information and persists them
    """
    request_apikey = request.headers.get(key="webhook-api-key", default=None)

    if apikey is None or request_apikey == apikey:

        if request.is_json:
            message = request.get_json()
            handle_ttn_message(message, app.logger)
            return message, 201
        return {"error": "Request must be JSON"}, 415

    else:
        return {"error": "Unauthorized"}, 401


@app.get("/moistureData")
def moistureData():
    """
    This method exports the moisture data for the current day.
    """
    days = request.args.get("days", 1, type=int)
    return export_moisture_map_data(days), 200


development_mode = os.environ.get("DEVELOPMENT_MODE")
if development_mode == "true":

    @app.route("/insertTestData", methods=["GET", "POST"])
    def insertTestData():
        """
        This method writes test data into the influx database for test purposes
        """
        if request.method == "POST":
            days = int(request.form["days"])
            devices = int(request.form["devices"])
            measurements = int(request.form["measurements"])
            write_test_data(devices, days, measurements)
            return "Success", 200
        return (
            """
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
        """,
            200,
        )


@app.get("/internal/health/self")
def health():
    return "", 200


@app.get("/internal/health/int")
def health_int():
    influx = get_influx_client()
    assert influx.ping()
    return "", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
