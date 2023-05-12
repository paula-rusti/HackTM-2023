import logging

from bme680_sensor.abstractions import Bme680Base
from bme680_sensor.data import Bme680Values

try:
    import bme680
except ImportError:
    # If this import fails, we are not on a Raspberry Pi
    pass


class Bme680Bosh(Bme680Base):
    def __init__(self):
        self._sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
        self._logger = logging.getLogger("Bme680Bosh")

    def initialize(self):
        """
        Initialize the sensor
        """
        self._sensor.set_humidity_oversample(bme680.OS_2X)
        self._sensor.set_pressure_oversample(bme680.OS_4X)
        self._sensor.set_temperature_oversample(bme680.OS_8X)
        self._sensor.set_filter(bme680.FILTER_SIZE_3)
        self._sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

    def get_sensor_data(self) -> Bme680Values:
        """
        Get sensor data
        """
        data = self._sensor.get_sensor_data()
        if data:
            return Bme680Values(
                temperature=data.temperature,
                humidity=data.humidity,
                pressure=data.pressure,
                gas_resistance=data.gas_resistance,
            )
        else:
            self._logger.warning("Could not read sensor data")
