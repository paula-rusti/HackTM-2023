import logging

import requests

import utils
from bme680_sensor.data import Bme680Values
from config import Configurator
from pusher.abstractions import CloudPusherBase


class HttpCloudPusher(CloudPusherBase):
    """
    Push data to the cloud via HTTP
    """

    def __init__(self, configurator: Configurator):
        utils.guard_against_none(configurator, "configurator")

        self._logger = logging.getLogger("CloudHttpPusher")
        self._config = configurator

        self._api_key = self._config.cloud_api_key
        self._bme_680_endpoint = self._config.cloud_data_endpoint_bme680

    def push_bme680_data(self, data: Bme680Values) -> bool:
        """
        Push BME680 data to the cloud
        """
        self._logger.debug(f"Pushing data to {self._bme_680_endpoint}")
        self._logger.debug(f"Data: {data}")

        try:
            requests.post(
                self._bme_680_endpoint,
                json=data.to_dict(),
                headers={"X-API-KEY": self._api_key},
            )
            return True
        except requests.exceptions.RequestException as e:
            self._logger.error(f"Error pushing data: {e}")
            return False

    def shutdown(self):
        self._logger.info("Shutting down HttpCloudPusher")
