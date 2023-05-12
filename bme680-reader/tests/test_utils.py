import pytest
from utils import guard_against_none


def test_guard_against_none():
    with pytest.raises(ValueError):
        guard_against_none(None, "test")

    # This should not raise an exception.
    guard_against_none(object, "test")
