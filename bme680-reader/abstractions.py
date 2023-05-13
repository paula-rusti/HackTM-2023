import abc


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
