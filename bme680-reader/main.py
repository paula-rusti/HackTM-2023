import logging

from bme680_sensor.factory import Bme680SensorFactory
from cloud_pusher.factory import CloudPusherFactory
from config import Configurator


class Worker:
    """
    Worker class for the application.
    It reads data from sensors and pushes them to the cloud.
    """

    pass


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
    sensor = Bme680SensorFactory.get_sensor_by_type(configurator.bme680_sensor_type)
    sensor.initialize()

    # pusher
    cloud_pusher = CloudPusherFactory.get_cloud_pusher_by_type(
        configurator.cloud_pusher_type, configurator
    )


if __name__ == "__main__":
    main()
