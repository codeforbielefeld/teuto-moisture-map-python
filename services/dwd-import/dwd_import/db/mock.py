from ast import List
from . import DeviceDB, MoistureDB, PrecipitationAverageDB
from models import PrecipitationAverage

class MockDB(DeviceDB,PrecipitationAverageDB):
    def write_precipitation_average(self, averages: List[PrecipitationAverage]):
        for a in averages:
            print(a)