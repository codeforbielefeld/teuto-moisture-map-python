from abc import ABC, abstractmethod
import re


class PayloadParser(ABC):

    @staticmethod
    def extract_numbers_from_string(string: str) -> float:
        """ 
        Extracts numerical values from strings
        """
        return re.findall("^\d+[.]*\d*", string)

    @staticmethod
    def extract_units_from_string(string: str) -> str:
        """
        Extracts the unit of measurements from strings 
        """
        return re.findall("[\w]*[°/%]*\w*$", string)

    @abstractmethod
    def parse_payload(self, payload: str) -> dict:
        pass
