from config import Configurator
from pusher.debug_pusher import DebugCloudPusher
from pusher.http_pusher import HttpCloudPusher


class CloudPusherFactory:
    """
    Factory class for creating cloud pusher objects.
    """

    @staticmethod
    def get_cloud_pusher_by_type(cloud_pusher_type: str, configurator: Configurator):
        if cloud_pusher_type == "CloudHttpPusher":
            return HttpCloudPusher(configurator)
        elif cloud_pusher_type == "DebugCloudPusher":
            return DebugCloudPusher(configurator)
        else:
            raise ValueError(f"Unknown cloud pusher type: {cloud_pusher_type}")
