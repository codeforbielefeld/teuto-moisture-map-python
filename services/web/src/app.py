# app.py
from cgitb import reset
from flask import Flask, request
import os

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


from os.path import dirname, abspath

from dotenv import load_dotenv
from tmm.export_influx import export_moisture_map_data

from ttn import handle_ttn_message, write_test_data
from ttn.examples import generate_test_data

load_dotenv()

# ===========
# Config
# ===========

apikey = os.environ.get("TMM_API_KEY")

# =====================
# Webhook web interface
# =====================

# Json WS endpoint accepting messages from TTN
app = Flask(__name__)

"""
This method accepts JSON payloads from TTN, unmarshals the required information and persists them 
"""


@app.post("/incomingMessages")
def incomingMessages():
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
    return export_moisture_map_data(), 200

@app.route("/insertTestData", methods=["GET", "POST"])
def insertTestData():
    if request.method == "POST":
        days = int(request.form["days"])
        devices = int(request.form["devices"])
        measurements = int(request.form["measurements"])
        write_test_data(devices, days, measurements)
        return "Success", 200
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
    """, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")