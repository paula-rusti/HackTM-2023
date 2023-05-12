import pytest
from utils import guard_against_none, guard_against_empty


def test_guard_against_none():
    with pytest.raises(ValueError):
        guard_against_none(None, "test")

    # This should not raise an exception.
    guard_against_none(object, "test")


def test_guard_against_empty():
    with pytest.raises(ValueError):
        guard_against_empty([], "test")

    # This should not raise an exception.
    guard_against_empty([1], "test")
