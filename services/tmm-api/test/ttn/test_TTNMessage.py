import unittest


from os.path import dirname

from tmm_api.ttn.TTNMessage import TTNMessage


class TestTTNMessageParsing(unittest.TestCase):
    def test_parse_payload(self):
        filepath = f"{dirname(__file__)}/../dragino_ttn_payload.json"

        message = TTNMessage.parse_file(filepath)
        measurement = message.to_measurement()

        self.assertEqual(measurement.battery, 3.304, "Battery value not ok")
        self.assertEqual(measurement.soil_conductivity, 57, "Conductivity value not ok")
        self.assertEqual(measurement.soil_temperature, 7.87, "Temperature value not ok")
        self.assertEqual(measurement.soil_moisture, 23.42, "Moisture value not ok")
        print(measurement)


if __name__ == "__main__":
    unittest.main()
