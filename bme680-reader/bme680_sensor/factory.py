from bme680_sensor.abstractions import Bme680Base
from bme680_sensor.mock import Bme680Mock
from bme680_sensor.sensor import Bme680Bosh


class Bme680SensorFactory:
    """
    Factory class for BME680 sensor.
    Returns the appropriate sensor for the targe system.
    """

    @staticmethod
    def get_sensor_by_type(sensor_type: str) -> Bme680Base:
        """
        Returns the sensor based on the given sensor type.

        Parameters
        ----------
        sensor_type : str
            The type of sensor to return.

        Returns
        -------
        Bme680Base
            The sensor object
        """
        if sensor_type == "Bme680Bosh":
            return Bme680Bosh()
        elif sensor_type == "Bme680Mock":
            return Bme680Mock()
