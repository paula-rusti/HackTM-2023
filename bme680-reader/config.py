import os

import yaml
from pydantic import BaseSettings


def yaml_config_settings_source():
    config_file_location = os.getenv("CONFIG_FILE_PATH", "config.yaml")
    # open yaml file and return contents
    with open(config_file_location) as file:
        return yaml.safe_load(file)


class Configurator(BaseSettings):
    """Application configuration."""

    cloud_api_key: str
    cloud_data_endpoint_bme680: str

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
