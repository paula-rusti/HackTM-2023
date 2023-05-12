import dataclasses


@dataclasses.dataclass
class Bme680Values:
    """
    Dataclass for BME680 sensor values

    Arguments
    ----------
    temperature: float
        Temperature in degrees Celsius
    humidity: float
        Humidity in % relative humidity
    pressure: float
        Pressure in hPa
    gas_resistance: float
        Gas resistance in Ohms
    """

    temperature: float
    humidity: float
    pressure: float
    gas_resistance: float
