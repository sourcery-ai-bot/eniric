"""Test of atmosphere.py functions."""

import numpy as np
import pytest

import eniric.atmosphere as atm


def test_consecutive_truths():
    """Test consecutive truths lists count of consecutive ones."""
    array1 = np.array([1, 1, 1, 0, 1, 1, 0, 0, 1, 0], dtype=bool)  # [3,2 1]
    array2 = np.array([0, 0, 1, 1, 1, 1, 1, 0, 1, 1], dtype=bool)  # [5, 2]
    array3 = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0], dtype=bool)  # [1,1,1,1,1]
    array4 = np.zeros(5, dtype=bool)  # []
    array5 = np.ones(5, dtype=bool)  # [5]

    assert np.all(atm.consecutive_truths(array1) == [3, 2, 1])
    assert np.all(atm.consecutive_truths(array2) == [5, 2])
    assert np.all(atm.consecutive_truths(array3) == [1, 1, 1, 1, 1])
    assert np.all(atm.consecutive_truths(array5) == [5])
    assert np.all(atm.consecutive_truths(array4) == [])

    # Check sum of trues equal sum of returned list
    assert np.sum(array1) == np.sum(atm.consecutive_truths(array1))

    rand_array = np.asarray(np.floor(np.random.random(50) * 2), dtype=bool)  # random values
    assert np.sum(rand_array) == np.sum(atm.consecutive_truths(rand_array))


@pytest.mark.xfail()
def test_barycenter_shift():
    """Test barycentric shift code."""
    raise False


@pytest.mark.xfail()
def test_old_barycenter_shift():
    """Test old barycentric shift code."""
    raise False


@pytest.mark.xfail()  # If missing the datafiles
def test_prepare_atmosphere():
    """Test that an atmosphere file is loaded.

    Test band is close to the band limits (accounting for the given offset. +- 100km/s).
    """
    raise False

# If I multiply the flux by the mask then the smallest flux should be 0.98
# If not then there would be an issue.
