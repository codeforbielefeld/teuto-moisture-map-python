from datetime import date, datetime, timedelta
from xmlrpc.client import Boolean

import fire

from .dwd_raster import get_moisture, get_moisture_single, get_precipitation

from .db.influx import InfluxDB

from dwd_import.models import MoistureMeasurement


class App:
    def moisture(self, influx: Boolean = False):
        end = date.today().replace(day=1)
        start = date(2022, 6, 1)
        # start = (end - timedelta(days=60)).replace(day=1)
        if influx:
            db = InfluxDB()
            devices = db.get_devices()
            lons = [d.lon for d in devices]
            lats = [d.lat for d in devices]

            measurements = []
            for day_since_start in range((end - start).days):
                req_date = start + timedelta(days=day_since_start)
                moisture = get_moisture(req_date, lons, lats)

                print(f"Moisture on {req_date.isoformat()}: {moisture} %")

                for device, percent in zip(devices, moisture):
                    measurements.append(MoistureMeasurement(device, percent, req_date))

            print(f"Writing {len(measurements)} measurements to influx")
            db.write_moisture(measurements)
            print("Done!")

        else:
            # Bielefeld
            lon = 8.5333300
            lat = 52.0333300
            for day_since_start in range((end - start).days):
                req_date = start + timedelta(days=day_since_start)
                moisture = get_moisture_single(req_date, lon, lat)
                print(f"Moisture on {req_date.isoformat()}: {moisture} %")

    def precipitation(self, recent: Boolean = True):
        if recent:
            for i in range(24):
                hour = datetime(2022, 7, 20, i, 0, 0)
                print(
                    f"Precipitation recent {hour.strftime('%d.%m.%Y %H:%M')} : {get_precipitation(hour, [7.6282,8],[51.9616,52])}"
                )
        else:
            for i in range(24):
                hour = datetime(2021, 7, 13, i, 0, 0)
                print(
                    f"Precipitation reproc {hour.strftime('%d.%m.%Y %H:%M')} : {get_precipitation(hour, [7.6282,8],[51.9616,52], False)}"
                )


def run():
    # disable pager
    fire.core.Display = lambda lines, out: print(*lines, file=out)  # noqa: E731
    fire.Fire(App)


if __name__ == "__main__":
    run()
