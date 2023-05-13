import datetime
import logging

import utils
from bme680_sensor.abstractions import Bme680Base
from bme680_sensor.data import Bme680Values
from config import Configurator
from pusher.abstractions import CloudPusherBase


class Bme680Mock(Bme680Base):
    """
    Mock BME680 sensor class for local testing and mock data.
    """

    def __init__(self, configurator: Configurator):
        utils.guard_against_none(configurator, "configurator")
        self._logger = logging.getLogger("MockSensor")
        self._config = configurator

    def initialize(self):
        self._logger.info("Initializing mock sensor")

    def get_sensor_data(self) -> Bme680Values:
        return Bme680Values(
            sensor_type="Bme680Mock",
            location_name=self._config.location_name,
            timestamp=int(datetime.datetime.now().timestamp() * 1000),
            temperature=20.0,
            humidity=50.0,
            pressure=1000.0,
            gas_resistance=10000.0,
        )

    def push_data_to_cloud(self, cloud_pusher: CloudPusherBase) -> bool:
        """
        Pushes data to the cloud

        Returns
        -------
        bool
            True if data was pushed successfully, False otherwise
        """
        self._logger.info("Pushing data to cloud")
        data = self.get_sensor_data()
        return cloud_pusher.push_bme680_data(data)
