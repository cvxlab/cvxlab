"""
test_util_functions.py 

@author: Matteo V. Rocco
@institution: Politecnico di Milano

This module contains tests for the functions in the 'esm.support.util_functions' 
module.
"""


import pytest
import pandas as pd
import numpy as np

from cvxlab.support.util_constants import *


def test_tril():
    """
    Test the tril function.
    This function tests the tril function with valid and invalid input, and 
    checks if the function correctly generates a lower triangular matrix with 
    ones and handles invalid input.
    """

    # valid input
    matrix = tril((3, 1))
    expected_matrix = np.array([
        [1, 0, 0],
        [1, 1, 0],
        [1, 1, 1]
    ])
    assert np.array_equal(matrix, expected_matrix)

    # valid input
    matrix = tril((1, 1))
    expected_matrix = np.array([[1.]])
    assert np.array_equal(matrix, expected_matrix)

    # invalid input
    with pytest.raises(TypeError):
        tril('not an integer')

    with pytest.raises(TypeError):
        tril(-1)

    with pytest.raises(ValueError):
        tril((-10, 1))


def test_arange():
    """
    Test the arange function.
    This function tests the 'arange' function with valid and invalid input, 
    and checks if the function correctly generates a reshaped array and 
    handles invalid input.
    """

    # valid input
    array = arange((2, 3), 1, 'F')
    expected_array = np.array([
        [1, 3, 5],
        [2, 4, 6]
    ])
    assert np.array_equal(array, expected_array)

    # valid input
    array = arange((2, 3), 1, 'C')
    expected_array = np.array([
        [1, 2, 3],
        [4, 5, 6]
    ])
    assert np.array_equal(array, expected_array)

    # valid input
    expected_array = np.array([[1, 2, 3]])
    array1 = arange((1, 3), 1, 'C')
    assert np.array_equal(array1, expected_array)
    array2 = arange((1, 3), 1, 'F')
    assert np.array_equal(array2, expected_array)

    # invalid input
    with pytest.raises(ValueError):
        arange('not an iterable', 1, 'F')

    with pytest.raises(ValueError):
        arange((2, 3), 'not an integer', 'F')

    with pytest.raises(ValueError):
        arange((2, 3), 1, 'not C or F')
