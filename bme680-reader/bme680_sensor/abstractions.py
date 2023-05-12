import abc

from bme680_sensor.data import Bme680Values


class Bme680Base(abc.ABC):
    """
    Abstract base class for BME680 sensors
    """

    @abc.abstractmethod
    def initialize(self):
        """
        Initialize the sensor
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_sensor_data(self) -> Bme680Values:
        """
        Get sensor data
        """
        raise NotImplementedError
