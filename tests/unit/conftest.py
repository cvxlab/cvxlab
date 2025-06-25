import cvxpy
import pytest
import pandas as pd
import numpy as np

from typing import Callable, Sequence, Any, Optional, Dict, Union


def assert_equality(
        result: Any,
        expected: Any,
        msg: str,
        tolerance: Optional[float] = None
) -> None:
    """
    Helper to assert equality for various types, with optional absolute tolerance.
    """

    if isinstance(result, cvxpy.Expression):
        result = result.value

    if isinstance(result, pd.DataFrame) and isinstance(expected, pd.DataFrame):
        if tolerance:
            assert result.shape == expected.shape and \
                (result.columns == expected.columns).all() and \
                (result.index == expected.index).all(), msg
            assert np.allclose(
                result.values, expected.values, atol=tolerance), msg
        else:
            assert result.equals(expected), msg

    elif isinstance(result, pd.Series) and isinstance(expected, pd.Series):
        if tolerance:
            assert result.shape == expected.shape and \
                (result.index == expected.index).all(), msg
            assert np.allclose(
                result.values, expected.values, atol=tolerance), msg
        else:
            assert result.equals(expected), msg

    elif isinstance(result, np.ndarray) and isinstance(expected, np.ndarray):
        if tolerance:
            assert np.allclose(result, expected, atol=tolerance), msg
        else:
            assert np.array_equal(result, expected), msg

    else:
        assert result == expected, msg


def run_test_cases(
    func: Callable,
    test_cases: Sequence[
        Union[
            # (args, expected, exception)
            tuple[Sequence[Any], Any, Optional[type]],
            # (args, expected, exception, kwargs)
            tuple[Sequence[Any], Any, Optional[type], Dict[str, Any]],
        ]
    ],
    tolerance: Optional[float] = None,
    **common_kwargs,
) -> None:
    """
    General-purpose test runner for any function signature.

    Parameters
    ----------
    func : Callable
        The function to test.
    test_cases : Sequence[tuple]
        List of test cases in one of the following forms:
            ((args...), expected_output, expected_exception)
            ((args...), expected_output, expected_exception, {kwarg: val, ...})
    tolerance : Optional[float]
         If a float is passed, use tolerant equality based on the passed 
            tolerancefor numpy arrays, Series, and DataFrames. (default is None).
    **common_kwargs
        Common keyword arguments passed to all test cases (overridden by 
            test-specific kwargs).
    """
    if not test_cases:
        raise ValueError("No test cases provided")

    if not callable(func):
        raise ValueError("func must be callable")

    for case in test_cases:
        if len(case) == 3:
            input_val, expected_output, expected_exception = case
            kwargs = common_kwargs
        elif len(case) == 4:
            input_val, expected_output, expected_exception, specific_kwargs = case
            kwargs = {**common_kwargs, **specific_kwargs}
        else:
            raise ValueError("Each test case must have 3 or 4 elements")

        # if input_val is a tuple, treat as positional args
        if isinstance(input_val, tuple):
            call_args = input_val
            def call_func(): return func(*call_args, **kwargs)
        else:
            def call_func(): return func(input_val, **kwargs)

        if expected_exception:
            with pytest.raises(expected_exception):
                call_func()
        else:
            result = call_func()
            msg = \
                f"""
                Failed for input={input_val}, kwargs={kwargs}. 
                Expected {expected_output}, got {result}
                """
            assert_equality(result, expected_output, msg, tolerance=tolerance)
