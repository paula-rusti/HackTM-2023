import dataclasses


@dataclasses.dataclass
class Bme680Values:
    """
    Dataclass for BME680 sensor values

    Arguments
    ----------
    sensor_type: str
        Sensor type
    timestamp: int
        Timestamp in milliseconds
    temperature: float
        Temperature in degrees Celsius
    humidity: float
        Humidity in % relative humidity
    pressure: float
        Pressure in hPa
    gas_resistance: float
        Gas resistance in Ohms
    """

    sensor_type: str
    timestamp: int
    temperature: float
    humidity: float
    pressure: float
    gas_resistance: float

    def to_dict(self) -> dict:
        """
        Convert the dataclass to a dictionary
        """
        return dataclasses.asdict(self)
