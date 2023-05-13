import abc

from bme680_sensor.data import Bme680Values


class CloudPusherBase(abc.ABC):
    @abc.abstractmethod
    def push_bme680_data(self, data: Bme680Values) -> bool:
        """
        Push BME680 data to the cloud
        """
        raise NotImplementedError()
