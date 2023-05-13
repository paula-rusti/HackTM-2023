import abc
import functools
import logging
import signal
import time
import typing

import utils
from bme680_sensor.factory import Bme680SensorFactory
from config import Configurator
from pusher.abstractions import CloudPusherBase
from pusher.factory import CloudPusherFactory


class Shutdownable(abc.ABC):
    """
    Interface for shutdownable objects.
    """

    @abc.abstractmethod
    def shutdown(self):
        """
        Shuts down, something.
        """
        raise NotImplementedError()


def signal_handler(shutdownable, sig, frame):
    """
    Signal handler for shutting down the Worker.
    """
    sig_handler_logger = logging.getLogger("signal_handler")
    sig_handler_logger.info("Shutting down")
    shutdownable.shutdown()


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


def main():
    main_logger = logging.getLogger("main")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    main_logger.info("Hello world.")

    # configurator
    configurator = Configurator()

    # sensor
    bme680_sensor = Bme680SensorFactory.get_sensor_by_type(
        configurator.bme680_sensor_type
    )
    bme680_sensor.initialize()

    # pusher
    cloud_pusher = CloudPusherFactory.get_cloud_pusher_by_type(
        configurator.cloud_pusher_type, configurator
    )

    # worker
    worker = Worker([bme680_sensor], cloud_pusher, configurator)

    # handle signal, shut down worker
    worker_shutdown_wrapper = functools.partial(signal_handler, worker)
    # noinspection PyTypeChecker
    signal.signal(signal.SIGINT, worker_shutdown_wrapper)
    # noinspection PyTypeChecker
    signal.signal(signal.SIGABRT, worker_shutdown_wrapper)

    # start worker, blocks forever
    worker.start()


if __name__ == "__main__":
    main()
