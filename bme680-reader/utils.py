import typing


def guard_against_none(_object: typing.Any, object_name: str):
    """
    Guard against None values.
    It raises an exception if the object is None.

    Parameters
    ----------
    _object : typing.Any
        The object to check.
    object_name : str
        The name of the object to check.
    """
    if _object is None:
        raise ValueError(f"{object_name} cannot be None.")
