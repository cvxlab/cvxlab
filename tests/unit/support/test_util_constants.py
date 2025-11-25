"""Tests for the cvxlab/support/util_functions.py module."""
import numpy as np

from cvxlab.support.util_constants import *
from cvxlab.log_exc import exceptions as exc
from tests.unit.conftest import run_test_cases


def test_sum_vector():
    """Test the sum_vector function."""
    test_cases = [
        ([3, 1], np.array([[1], [1], [1]]), None),
        ([1, 4], np.array([[1, 1, 1, 1]]), None),
        ('invalid type', None, exc.SettingsError),
        ([2, 2, 3], None, exc.SettingsError),
        ([2, 3], None, exc.SettingsError),
    ]

    run_test_cases(
        func=sum_vector,
        test_cases=test_cases,
        unpack_tuple_args=False,
    )


def test_identity_matrix():
    """Test the identity_matrix function."""
    test_cases = [
        ([1, 3], np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]), None),
        ([1, 1], np.array([[1]]), None),
        ([3, 3], None, exc.SettingsError),
        ([2, 3], None, exc.SettingsError),
        ('invalid type', None, exc.SettingsError),
        ([2, 2, 3], None, exc.SettingsError),
    ]

    run_test_cases(
        func=identity_matrix,
        test_cases=test_cases,
        unpack_tuple_args=False,
    )


def test_set_lenght():
    """Test the set_length function."""
    test_cases = [
        ([1, 1], np.array([[1]]), None),
        ([1, 4], np.array([[4]]), None),
        ([2, 3], None, exc.SettingsError),
        ([2, 2, 3], None, exc.SettingsError),
        ('invalid type', None, exc.SettingsError),
    ]

    run_test_cases(
        func=set_length,
        test_cases=test_cases,
        unpack_tuple_args=False,
    )


def test_arange():
    """Test the arange function."""
    test_cases = [
        (([2, 3], 1, 'F'), np.array([[1, 3, 5], [2, 4, 6]]), None),
        (([2, 3], 1, 'C'), np.array([[1, 2, 3], [4, 5, 6]]), None),
        (([1, 3], 1, 'C'), np.array([[1, 2, 3]]), None),
        (([1, 3], 0, 'F'), np.array([[0, 1, 2]]), None),
        (('not a tuple', 1, 'F'), None, exc.SettingsError),
        (([1, 3], 'not an int', 'F'), None, ValueError),
        (([2, 3], 'not an integer', 'F'), None, ValueError),
        (([2, 3], 1, 'not C or F'), None, ValueError),
    ]

    run_test_cases(
        func=arange,
        test_cases=test_cases,
    )


def test_lower_triangular_matrix():
    """Test the lower_triangular_matrix function."""
    test_cases = [
        ([3, 1], np.array([[1, 0, 0], [1, 1, 0], [1, 1, 1]]), None),
        ([1, 1], np.array([[1.]]), None),
        ('invalid type', None, exc.SettingsError),
        ([2, 2, 3], None, exc.SettingsError),
        ([2, 3], None, exc.SettingsError),
    ]

    run_test_cases(
        func=lower_triangular_matrix,
        test_cases=test_cases,
        unpack_tuple_args=False,
    )
