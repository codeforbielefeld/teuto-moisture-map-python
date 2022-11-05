from abc import ABC, abstractmethod
from dwd_import.models import (
    DWDStation,
    Device,
    MoistureMeasurement,
    PrecipitationAverage,
)


class MoistureDB(ABC):
    @abstractmethod
    def write_moisture(self, measurements: list[MoistureMeasurement]):
        pass


class DeviceDB(ABC):
    @abstractmethod
    def get_devices(self) -> list[Device]:
        pass


class StationDB(ABC):
    @abstractmethod
    def get_stations(self) -> list[DWDStation]:
        pass

    @abstractmethod
    def write_stations(self, stations: list[DWDStation]):
        pass


class PrecipitationAverageDB(ABC):
    @abstractmethod
    def write_precipitation_average(self, averages: list[PrecipitationAverage]):
        pass

    @abstractmethod
    def get_precipitation_average(self, station: DWDStation) -> list[PrecipitationAverage]:
        pass
