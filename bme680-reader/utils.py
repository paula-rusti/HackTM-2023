import typing


def guard_against_empty(_list: typing.List, list_name: str):
    """
    Guard against empty lists.
    It raises an exception if the list is empty.

    Parameters
    ----------
    _list : typing.List
        The list to check.
    list_name : str
        The name of the list to check.
    """
    if not _list:
        raise ValueError(f"{list_name} cannot be empty.")


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
