"""Module with user defined functions defined as model's constants.

This module provides various utility functions that are defined to support 
complex calculations in symbolic problems through generation of constants types,
such as generating special matrices (positive semidefinite matrices).

There are two ways to add a new user-defined constant:

1. Add a new constant directly in the current module `cvxlab.support.util_constants`:
   simply define a new function in this module, that will be embedded in the package
   as a built-in constant.

2. Users can define custom constants in their model directory by defining the related
   function in the 'user_defined_constants.py' file, and loading the module when
   generating the Model instance. This way, users can extend the package with their
   own custom constants without modifying the package code (ideal for model users).

Functions are registered as constants in Constants class, and actual constants data
are generated when generating variables (see backend.Variable.define_constant() method).
"""
import numpy as np

from typing import Iterable, Tuple
from cvxlab.log_exc import exceptions as exc

_CONSTANTS_REGISTRY = {}


def constant(name: str) -> callable:
    """Decorator to register a constant generation function.

    Args:
        name (str): The name of the constant to register.

    Returns:
        callable: The decorated function.
    """
    def decorator(func: callable) -> callable:
        _CONSTANTS_REGISTRY[name] = func
        return func
    return decorator


@constant('sum_vector')
def sum_vector(dimension: Tuple[int]) -> np.ndarray:
    """Define a vector of ones for matrix summation operations.

    Args:
        dimension (Tuple[int]): The dimension of the vector (rows, cols).

    Returns:
        np.ndarray: A vector of ones with the specified dimension.

    Raises:
        exc.SettingsError: If passed dimension is not a tuple containing integers,
            or if it does not represent a vector (i.e., at least one element 
            must be equal to 1).
    """
    if not isinstance(dimension, Tuple) or not \
            all(isinstance(i, int) for i in dimension):
        raise exc.SettingsError(
            "Constant definition | Summation vector constant accepts as argument"
            "only a tuple of integers.")

    if len(dimension) != 2 or not any(i == 1 for i in dimension):
        raise exc.SettingsError(
            "Constant definition | Summation vector can be defined as "
            "vector only (one dimension). Check variable shape.")

    return np.ones(dimension)


@constant('identity')
def identity_matrix(dimension: Tuple[int]) -> np.array:
    """Generate a (square) identity matrix of the specified dimension.

    Args:
        dimension (Tuple[int]): The dimension of the matrix row/col.

    Returns:
        np.ndarray: A square identity matrix of the specified dimension.

    Raises:
        exc.SettingsError: If passed dimension is not a tuple containing integers,
            or if it does not represent a vector (i.e., at least one element 
            must be equal to 1).
    """
    if not isinstance(dimension, Tuple) or not \
            all(isinstance(i, int) for i in dimension):
        raise exc.SettingsError(
            "Constant definition | Identity matrix constant accepts as argument"
            "only a tuple of integers.")

    if len(dimension) != 2 or not any(i == 1 for i in dimension):
        raise exc.SettingsError(
            "Constant definition | Identity matrix accetps as argument a tuple "
            "representing a vector only (one dimension). Check variable shape.")

    return np.eye(max(dimension))


@constant('set_length')
def set_length(dimension: Tuple[int]) -> np.array:
    """Define the length of a set as a constant.

    Args:
        dimension (Tuple[int]): The dimension of the vector (rows, cols).

    Returns:
        np.ndarray: A 1x1 array (scalar) containing the length of the set.

    Raises:
        exc.SettingsError: If passed dimension is not a tuple containing integers,
            or if it does not represent a vector (i.e., at least one element 
            must be equal to 1).
    """
    if not isinstance(dimension, Tuple) or not \
            all(isinstance(i, int) for i in dimension):
        raise exc.SettingsError(
            "Constant definition | Set lenght constant accepts as argument"
            "only a tuple of integers.")

    if len(dimension) != 2 or not any(i == 1 for i in dimension):
        raise exc.SettingsError(
            "Constant definition | Set lenght constant accetps as argument a tuple "
            "representing a vector only (one dimension). Check variable shape.")

    dimension_size = np.array(np.max(dimension))
    if dimension_size.ndim == 0:
        dimension_size = dimension_size.reshape(-1, 1)

    return dimension_size


def arange(dimension: Tuple[int], start_from: int, order: str = 'F') -> np.array:
    """Define a reshaped range array.

    Generate a reshaped array with values ranging from 'start_from' to 
    'start_from + total_elements'.
    Notice that this function is not directly registered as a constant, but it 
    is used to define other constants (e.g., arange_0)

    Args:
        shape_size (Iterable[int]): The shape of the output array.
        start_from (int, optional): The starting value for the range.
        order (str, optional): The order of the reshaped array. Defaults to 'F'.

    Returns:
        np.ndarray: The reshaped array with values ranging from 'start_from' 
            to 'start_from + total_elements'.

    Raises:
        exc.SettingsError: If passed dimension is not a tuple containing integers.
        ValueError: If 'start_from' is not an integer.
        ValueError: If 'order' is not a string or not in ['C', 'F'].
    """
    if not isinstance(dimension, Iterable) or \
            not all(isinstance(i, int) for i in dimension):
        raise exc.SettingsError(
            "Constant definition | Range constant accepts as argument only a "
            "tuple of integers.")

    if not isinstance(start_from, int):
        raise ValueError("'start_from' must be an integer.")

    if not isinstance(order, str):
        raise ValueError("'order' must be a string.")

    if order not in ['C', 'F']:
        raise ValueError("'order' must be either 'C' or 'F'.")

    total_elements = np.prod(dimension)
    values = np.arange(start_from, start_from+total_elements)
    reshaped_array = np.reshape(a=values, newshape=dimension, order=order)

    return reshaped_array


@constant('arange_0')
def arange_0(dimension: Tuple[int]) -> np.ndarray:
    """Define a reshaped range array starting from zero."""
    return arange(dimension=dimension, start_from=0)


@constant('arange_1')
def arange_0(dimension: Tuple[int]) -> np.ndarray:
    """Define a reshaped range array starting from zero."""
    return arange(dimension=dimension, start_from=1)


@constant('lower_triangular')
def lower_triangular_matrix(dimension: Tuple[int]) -> np.array:
    """Define a lower triangular matrix.

    Generate a square matrix with ones in the lower triangular region
    (including the diagonal) and zeros elsewhere.

    Args:
        dimension (Tuple[int]): The dimension of the matrix row/col.

    Returns:
        np.ndarray: A square matrix with ones in the lower triangular region 
            and zeros elsewhere.

    Raises:
        exc.SettingsError: If passed dimension is not a tuple containing integers,
            or if it does not represent a vector (i.e., at least one element 
            must be equal to 1).
    """
    if not isinstance(dimension, Tuple) or not \
            all(isinstance(i, int) for i in dimension):
        raise exc.SettingsError(
            "Constant definition | Lower triangular matrix accepts as argument"
            "only a tuple of integers.")

    if len(dimension) != 2 or not any(i == 1 for i in dimension):
        raise exc.SettingsError(
            "Constant definition | Lower triangular matrix accetps as argument "
            "a tuple representing a vector only (one dimension). Check variable shape.")

    size = max(dimension)
    matrix = np.tril(np.ones((size, size)))
    np.fill_diagonal(matrix, 1)

    return matrix


CONSTANTS = _CONSTANTS_REGISTRY
