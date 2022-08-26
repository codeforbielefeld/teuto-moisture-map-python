from typing import List
from . import DeviceDB, PrecipitationAverageDB
from dwd_import.models import PrecipitationAverage


class MockDB(DeviceDB, PrecipitationAverageDB):
    def write_precipitation_average(self, averages: List[PrecipitationAverage]):
        for a in averages:
            print(a)
