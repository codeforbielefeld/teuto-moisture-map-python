from typing import List
from datetime import datetime, date

import rasterio as ri
from pyproj import Transformer, CRS

# Transform from longitute/latitute coordinates do Gauss-Krueger 3 coordinates with swaped axes as used by DWD
wgs84 = "epsg:4326"
gk3 = "epsg:31467"
transformer = Transformer.from_crs(wgs84, gk3, always_xy=True)


def fetch_moisture(day: date):
    month = day.strftime("%Y%m")
    day_str = day.strftime("%Y%m%d")
    # For data origin see: https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/soil_moist/DESCRIPTION_gridsgermany_daily_soil_moist_en.pdf
    url = f"/vsitar/vsicurl/https://opendata.dwd.de/climate_environment/CDC/grids_germany/daily/soil_moist/grids_germany_daily_soil_moist_{month}.tgz/grids_germany_daily_soil_moist_{day_str}.asc"
    # See: https://gdal.org/user/virtual_file_systems.html
    return ri.open(url)


def get_moisture_single(day: date, lon: float, lat: float):
    with fetch_moisture(day) as src:
        x, y = transformer.transform([lon], [lat])
        rm, cm = src.shape
        r, c = src.index(x[0], y[0])
        rm, cm = src.shape
        assert 0 <= r <= rm and 0 <= c <= cm, f"Coordinates out of bounds! {lon, lat} -> {r,c}"
        data = src.read(1)[r, c]
        return data


def get_moisture(day: date, lons: List[float], lats: List[float]):
    with fetch_moisture(day) as src:
        x, y = transformer.transform(lons, lats)
        xy = [[x, y] for x, y in zip(x, y)]
        data = [a[0] for a in src.sample(xy, 1)]
        return data


def fetch_precipitation(hour: datetime, recent: bool = True):
    day_str = hour.strftime("%Y%m%d")
    hour_str = hour.strftime("%Y%m%d-%H")

    reproc_year_str = hour.strftime("%Y")
    reproc_month_str = hour.strftime("%Y%m")
    reproc_hour_str = hour.strftime("%Y%m%d_%H")

    # See: https://gdal.org/user/virtual_file_systems.html
    url = f"/vsitar/vsicurl/https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/radolan/recent/asc/RW-{day_str}.tar.gz/RW_{hour_str}50.asc" if recent else \
        f"/vsitar/vsicurl/https://opendata.dwd.de/climate_environment/CDC/grids_germany/hourly/radolan/reproc/2017_002/asc/{reproc_year_str}/RW2017.002_{reproc_month_str}_asc.tar.gz/RW_2017.002_{reproc_hour_str}50.asc"
    return ri.open(url)


radolan_prj = 'PROJCS["Stereographic_North_Pole",GEOGCS["GCS_unnamed ellipse",DATUM["D_unknown",SPHEROID["Unknown",6370040,0]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Stereographic_North_Pole"],PARAMETER["standard_parallel_1",60],PARAMETER["central_meridian",10],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["Meter",1]]'
radolan_transformer = Transformer.from_crs(wgs84, CRS(radolan_prj), always_xy=True)


def get_precipitation(hour: datetime, lons: List[float], lats: List[float], recent: bool = True):
    with fetch_precipitation(hour, recent) as src:
        xs, ys = radolan_transformer.transform(lons, lats)
        xy = xy = [[x, y] for x, y in zip(xs, ys)]
        data = [a[0]*0.1 for a in src.sample(xy, 1)]
        return data
