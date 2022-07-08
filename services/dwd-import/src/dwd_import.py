from typing import List
from datetime import timedelta, date

import rasterio as ri
from pyproj import Transformer

from models import Measurement
from influx import get_devices, write_moisture

# Transform from longitute/latitute coordinates do Gauss-Krueger 3 coordinates with swaped axes as used by DWD
wgs84 = "epsg:4326"
gk3 = "epsg:31467"
transformer = Transformer.from_crs(wgs84, gk3, always_xy=True)


def fetch_dataset(day: date):
    month = day.strftime("%Y%m")
    day_str = day.strftime("%Y%m%d")
    # For data origin see: https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/soil_moist/DESCRIPTION_gridsgermany_daily_soil_moist_en.pdf
    url = f"/vsitar/vsicurl/https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/soil_moist/grids_germany_daily_soil_moist_{month}.tgz/grids_germany_daily_soil_moist_{day_str}.asc"
    # See: https://gdal.org/user/virtual_file_systems.html
    return ri.open(url)


def get_moisture_single(day: str, lon: float, lat: float):
    with fetch_dataset(day) as src:
        x, y = transformer.transform([lon], [lat])
        rm, cm = src.shape
        r, c = src.index(x[0], y[0])
        rm, cm = src.shape
        assert 0 <= r <= rm and 0 <= c <= cm, f"Coordinates out of bounds! {lon, lat} -> {r,c}"
        data = src.read(1)[r, c]
        return data


def get_moisture(day: str, lons: List[float], lats: List[float]):
    with fetch_dataset(day) as src:
        x, y = transformer.transform(lons, lats)
        xy = list(map(lambda x, y: [x, y], x, y))
        data = list(map(lambda a: a[0], src.sample(xy, 1)))
        return data


if __name__ == "__main__":

    end = date.today().replace(day=1)
    start = date(2022, 6, 1)
    #start = (end - timedelta(days=60)).replace(day=1)

    use_influx = True
    if use_influx:

        devices = get_devices()
        lons = list(map(lambda d: d.lon, devices))
        lats = list(map(lambda d: d.lat, devices))

        measurements = []        
        for day_since_start in range((end-start).days):
            req_date = start + timedelta(days=day_since_start)
            moisture = get_moisture(req_date, lons, lats)
            
            print(f"Moisture on {req_date.isoformat()}: {moisture} %")

            for device, percent in zip(devices, moisture):
                measurements.append(Measurement(device, percent, req_date))

        print(f"Writing {len(measurements)} measurements to influx")
        write_moisture(measurements)
        print("Done!")

    else:
        # Bielefeld
        lon = 8.5333300
        lat = 52.0333300
        for day_since_start in range((end-start).days):
            req_date = start + timedelta(days=day_since_start)
            moisture = get_moisture_single(req_date, lon, lat)
            print(f"Moisture on {req_date.isoformat()}: {moisture} %")
