from bme680_sensor.abstractions import Bme680Base
from bme680_sensor.mock import Bme680Mock
from bme680_sensor.sensor import Bme680Bosh
from config import Configurator


class Bme680SensorFactory:
    """
    Factory class for BME680 sensor.
    Returns the appropriate sensor for the targe system.
    """

    @staticmethod
    def get_sensor_by_type(sensor_type: str, configurator: Configurator) -> Bme680Base:
        """
        Returns the sensor based on the given sensor type.

        Parameters
        ----------
        sensor_type : str
            The type of sensor to return.
        configurator : Configurator
            The configurator object.

        Returns
        -------
        Bme680Base
            The sensor object
        """
        if sensor_type == "Bme680Bosh":
            return Bme680Bosh(configurator)
        elif sensor_type == "Bme680Mock":
            return Bme680Mock(configurator)
        else:
            raise ValueError(f"Unknown sensor type: {sensor_type}")
