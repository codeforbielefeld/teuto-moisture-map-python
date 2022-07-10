from typing import List
from datetime import datetime, timedelta, date

import rasterio as ri
from pyproj import Transformer, CRS

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



def get_moisture_single(day: date, lon: float, lat: float):
    with fetch_dataset(day) as src:
        x, y = transformer.transform([lon], [lat])
        rm, cm = src.shape
        r, c = src.index(x[0], y[0])
        rm, cm = src.shape
        assert 0 <= r <= rm and 0 <= c <= cm, f"Coordinates out of bounds! {lon, lat} -> {r,c}"
        data = src.read(1)[r, c]
        return data


def get_moisture(day: date, lons: List[float], lats: List[float]):
    with fetch_dataset(day) as src:
        x, y = transformer.transform(lons, lats)
        xy = list(map(lambda x, y: [x, y], x, y))
        data = list(map(lambda a: a[0], src.sample(xy, 1)))
        return data

def fetch_rain(hour: datetime):    
    day_str = hour.strftime("%Y%m%d")
    hour_str = hour.strftime("%Y%m%d-%H")    
    url = f"/vsitar/vsicurl/https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/radolan/recent/asc/RW-{day_str}.tar.gz/RW_{hour_str}50.asc"
    # See: https://gdal.org/user/virtual_file_systems.html
    return ri.open(url)

radolan_prj = 'PROJCS["Stereographic_North_Pole",GEOGCS["GCS_unnamed ellipse",DATUM["D_unknown",SPHEROID["Unknown",6370040,0]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Stereographic_North_Pole"],PARAMETER["standard_parallel_1",60],PARAMETER["central_meridian",10],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["Meter",1]]'
radolan_transformer = Transformer.from_crs(wgs84, CRS(radolan_prj), always_xy=True)
def get_rain(hour: datetime, lons: List[float], lats: List[float]):
    with fetch_rain(hour) as src:
        xs, ys = radolan_transformer.transform(lons, lats)
        xy = list(map(lambda x, y: [x, y], xs, ys))
        data = list(map(lambda a: a[0]*0.1, src.sample(xy, 1)))
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

        for i in range(24):
            hour = datetime(2022,6,30,i,0,0)
            print(f"Niederschlag {hour.strftime('%d.%m.%Y %H:%M')} : {get_rain(hour, [7.6282,8],[51.9616,52])}")
