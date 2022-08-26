from typing import List
from dwd_import.db import DeviceDB
from dwd_import.models import Device
from pymongo import MongoClient
from pymongo.collection import Collection
import os


class MongoDB(DeviceDB):
    def __init__(self) -> None:
        super().__init__()

        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = os.environ["MONGO_CONNECTION_STRING"]
        self._client: MongoClient = MongoClient(CONNECTION_STRING)

        DATABASE_NAME = os.environ["MONGO_DATABASE_NAME"]
        self._database = self._client[DATABASE_NAME]
        self._devices: Collection = self._database["devices"]

    def get_devices(self) -> List[Device]:
        return [
            Device(**{k: v for (k, v) in d.items() if k in Device._fields})
            for d in self._devices.find()
        ]


def test():
    d = MongoDB()
    print("Devices:", d.get_devices())
