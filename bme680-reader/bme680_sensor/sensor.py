import datetime
import logging

import utils
from bme680_sensor.abstractions import Bme680Base
from bme680_sensor.data import Bme680Values
from config import Configurator
from pusher.abstractions import CloudPusherBase

try:
    import bme680
except ImportError:
    # If this import fails, we are not on a Raspberry Pi
    pass


class Bme680Bosh(Bme680Base):
    def __init__(self, configurator: Configurator):
        utils.guard_against_none(configurator, "configurator")
        self._sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        self._logger = logging.getLogger("Bme680Bosh")
        self._config = configurator

    def initialize(self):
        """
        Initialize the sensor
        """
        self._sensor.set_humidity_oversample(bme680.OS_2X)
        self._sensor.set_pressure_oversample(bme680.OS_4X)
        self._sensor.set_temperature_oversample(bme680.OS_8X)
        self._sensor.set_filter(bme680.FILTER_SIZE_3)
        self._sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        self._sensor.set_gas_heater_temperature(320)
        self._sensor.set_gas_heater_duration(150)
        self._sensor.select_gas_heater_profile(0)

    def get_sensor_data(self) -> Bme680Values:
        """
        Get sensor data
        """
        ok = self._sensor.get_sensor_data()
        if ok:
            return Bme680Values(
                sensor_type="Bme680Bosh",
                location_name=self._config.location_name,
                timestamp=int(datetime.datetime.now().timestamp() * 1000),
                temperature=self._sensor.data.temperature,
                humidity=self._sensor.data.humidity,
                pressure=self._sensor.data.pressure,
                gas_resistance=self._sensor.data.gas_resistance,
            )
        else:
            self._logger.warning("Could not read sensor data")
            return Bme680Values(
                sensor_type="Bme680Bosh",
                location_name=self._config.location_name,
                timestamp=int(datetime.datetime.now().timestamp() * 1000),
                temperature=-1,
                humidity=-1,
                pressure=-1,
                gas_resistance=-1,
            )

    def push_data_to_cloud(self, cloud_pusher: CloudPusherBase) -> bool:
        """
        Pushes data to the cloud

        Returns
        -------
        bool
            True if data was pushed successfully, False otherwise
        """
        data = self.get_sensor_data()
        return cloud_pusher.push_bme680_data(data)
