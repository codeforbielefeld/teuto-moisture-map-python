from abc import ABC, abstractmethod
from typing import List
from dwd_import.models import DWDStation, Device, MoistureMeasurement, PrecipitationAverage


class MoistureDB(ABC):
    @abstractmethod
    def write_moisture(self,measurements: List[MoistureMeasurement]):
        pass

class DeviceDB(ABC):
    @abstractmethod
    def get_devices(self)-> List[Device]: 
        pass

class StationDB(ABC):
    @abstractmethod
    def get_stations(self)-> List[DWDStation]:
        pass
    @abstractmethod
    def write_stations(self, stations: List[DWDStation]):
        pass

class PrecipitationAverageDB(ABC):
    @abstractmethod
    def write_precipitation_average(self, averages: List[PrecipitationAverage]):
        pass

    @abstractmethod
    def get_precipitation_average(self, station: DWDStation) -> List[PrecipitationAverage]:
        pass

class PrecipitationAverageDB(ABC):
    @abstractmethod
    def write_precipitation_average(self, averages: List[PrecipitationAverage]):
        pass

    @abstractmethod
    def get_precipitation_average(self, station: DWDStation) -> List[PrecipitationAverage]:
        pass