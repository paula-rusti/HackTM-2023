import json

import pika
from pika.exceptions import NackError, UnroutableError

import utils
from bme680_sensor.data import Bme680Values
from config import Configurator
from pusher.abstractions import CloudPusherBase


class RabbitMqPusher(CloudPusherBase):
    def __init__(self, configurator: Configurator):
        utils.guard_against_none(configurator, "configurator")
        self._config = configurator

        self._api_key = self._config.cloud_api_key
        self._bme_680_endpoint = self._config.cloud_data_endpoint_bme680

        rabbit_mq_connection_string = (
            f"amqp://{self._api_key}:{self._api_key}@{self._bme_680_endpoint}/"
        )

        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbit_mq_connection_string)
        )
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange="sensor-data", exchange_type="fanout")

    def push_bme680_data(self, data: Bme680Values) -> bool:
        body = json.dumps(data.to_dict()).encode("utf-8")
        try:
            self._channel.basic_publish(
                exchange="sensor-data", routing_key=data.sensor_type, body=body
            )
            return True
        except NackError | UnroutableError as e:
            print(f"Error pushing data: {e}")
            return False
