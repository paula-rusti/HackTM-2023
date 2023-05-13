import logging
import time
import typing

import utils
from abstractions import Shutdownable
from config import Configurator
from pusher.abstractions import CloudPusherBase


class Worker(Shutdownable):
    """
    Worker class for the application.
    It reads data from sensors and pushes them to the cloud.
    """

    def __init__(
        self,
        sensors: typing.List,
        cloud_pusher: CloudPusherBase,
        configurator: Configurator,
    ):
        self._logger = logging.getLogger("Worker")
        utils.guard_against_none(sensors, "sensors")

        self._sensors = sensors
        self._cloud_pusher = cloud_pusher
        self._worker_polling_interval = configurator.worker_polling_interval

        self._logger.info("Starting worker")
        self._is_running = False

    def start(self):
        self._is_running = True
        while self._is_running:
            for sensor in self._sensors:
                retry = 0
                while retry < 3:
                    ok = sensor.push_data_to_cloud(self._cloud_pusher)
                    if ok:
                        break
                    retry += 1
                    time.sleep(1)
                if retry >= 3:
                    self._logger.error("Error reading data from sensor")
            time.sleep(self._worker_polling_interval)

    def shutdown(self):
        self._is_running = False
