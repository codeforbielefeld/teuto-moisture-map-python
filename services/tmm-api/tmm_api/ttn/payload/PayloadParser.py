from abc import ABC, abstractmethod
import re


class PayloadParser(ABC):
    @staticmethod
    def extract_numbers_from_string(string: str) -> list:
        """
        Extracts numerical values from strings
        """
        return re.findall(r"^\d+[.]*\d*", string)

    @staticmethod
    def extract_units_from_string(string: str) -> list:
        """
        Extracts the unit of measurements from strings
        """
        return re.findall(r"[\w]*[°/%]*\w*$", string)

    @abstractmethod
    def parse_payload(self, payload: dict) -> dict:
        pass
