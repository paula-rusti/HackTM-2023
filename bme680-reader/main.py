import functools
import logging
import signal

from bme680_sensor.factory import Bme680SensorFactory
from config import Configurator
from pusher.factory import CloudPusherFactory
from worker import Worker


def signal_handler(shutdownable, sig, frame):
    """
    Signal handler for shutting down the Worker.
    """
    sig_handler_logger = logging.getLogger("signal_handler")
    sig_handler_logger.info("Shutting down")
    shutdownable.shutdown()


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
