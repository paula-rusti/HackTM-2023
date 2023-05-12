import logging

from bme680_sensor.abstractions import Bme680Base
from bme680_sensor.data import Bme680Values


class Bme680Mock(Bme680Base):
    """
    Mock BME680 sensor class for local testing and mock data.
    """

    def __init__(self):
        self._logger = logging.getLogger("MockSensor")

    def initialize(self):
        self._logger.info("Initializing mock sensor")

    def get_sensor_data(self) -> Bme680Values:
        return Bme680Values(
            temperature=20.0,
            humidity=50.0,
            pressure=1000.0,
            gas_resistance=10000.0,
        )
