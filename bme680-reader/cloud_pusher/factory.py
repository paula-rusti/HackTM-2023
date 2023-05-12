from config import Configurator
from cloud_pusher.http_pusher import CloudHttpPusher


class CloudPusherFactory:
    """
    Factory class for creating cloud pusher objects.
    """

    @staticmethod
    def get_cloud_pusher_by_type(cloud_pusher_type: str, configurator: Configurator):
        if cloud_pusher_type == "CloudHttpPusher":
            return CloudHttpPusher(configurator)
        else:
            raise ValueError(f"Unknown cloud pusher type: {cloud_pusher_type}")
