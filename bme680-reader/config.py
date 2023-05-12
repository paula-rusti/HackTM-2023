import os

import yaml
from pydantic import BaseSettings


def yaml_config_settings_source(settings):
    config_file_location = os.getenv("CONFIG_FILE_PATH", "config.yaml")
    # open yaml file and return contents
    with open(config_file_location) as file:
        return yaml.safe_load(file)


class Configurator(BaseSettings):
    """
    Application configuration.

    Attributes:
    ----------
    cloud_api_key: str
        API key for the cloud service
    cloud_data_endpoint_bme680: str
        Endpoint for pushing BME680 data to the cloud
    cloud_pusher_type: str
        Type of cloud pusher to use
    bme680_sensor_type: str
        Type of BME680 sensor to use
    bme680_sensor_i2c_address: int
        I2C address of the BME680 sensor
    """

    cloud_api_key: str
    cloud_data_endpoint_bme680: str
    cloud_pusher_type: str

    worker_polling_interval: int

    bme680_sensor_type: str = "Bme680Bosh"
    bme680_sensor_i2c_address: int = 118

    class Config:
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                yaml_config_settings_source,
                env_settings,
                file_secret_settings,
            )
