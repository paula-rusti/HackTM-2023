import logging

import utils
from bme680_sensor.data import Bme680Values
from config import Configurator
from pusher.abstractions import CloudPusherBase


class DebugCloudPusher(CloudPusherBase):
    """
    DebugPusher is a simple pusher that just logs the data to the console.
    """

    def __init__(self, configurator: Configurator):
        utils.guard_against_none(configurator, "configurator")
        self._logger = logging.getLogger("DebugPusher")
        self._logger.info(
            "Initializing DebugPusher, api_key: {configurator.cloud_api_key}"
        )

    def push_bme680_data(self, data: Bme680Values) -> bool:
        self._logger.info(f"Pushing data to cloud")
        self._logger.info(f"Data: {data.to_dict()}")
        return True

    def shutdown(self):
        self._logger.info("Shutting down DebugPusher")
