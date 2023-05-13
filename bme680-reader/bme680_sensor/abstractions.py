import abc

from bme680_sensor.data import Bme680Values
from pusher.abstractions import CloudPusherBase


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

    def push_data_to_cloud(self, cloud_pusher: CloudPusherBase) -> bool:
        """
        Pushes data to the cloud

        Returns
        -------
        bool
            True if data was pushed successfully, False otherwise
        """
        raise NotImplementedError
