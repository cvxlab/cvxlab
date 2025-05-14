"""
util_functions.py 

@author: Matteo V. Rocco
@institution: Politecnico di Milano

This module provides various utility functions that are defined to support 
complex calculations in symbolic problems and generation of constants values,
such as generating special matrices, reshaping arrays, and calculating matrix 
inverses.
"""

from typing import Iterable, Tuple
import numpy as np
import pandas as pd


def tril(dimension: Tuple[int]) -> np.array:
    """
    Generate a square matrix with ones in the lower triangular region
    (including the diagonal) and zeros elsewhere.

    Parameters:
        dimension (Tuple[int]): The dimension of the matrix row/col.

    Returns:
        np.ndarray: A square matrix with ones in the lower triangular region 
            and zeros elsewhere.

    Raises:
        ValueError: If passed dimension is not greater than zero.
        TypeError: If passed dimension is not an iterable containing integers.
    """
    if not isinstance(dimension, Tuple) and not \
            all(isinstance(i, int) for i in dimension):
        raise TypeError(
            "Passed dimension must be a tuple containing integers.")

    if any(i < 0 for i in dimension):
        raise ValueError(
            "Passed dimension must be integers greater than zero.")

    if len(dimension) != 2 or not any(i == 1 for i in dimension):
        raise ValueError(
            "Passed dimension must have at least one element equal to 1 (it "
            "must represent a vector.")

    size = max(dimension)
    matrix = np.tril(np.ones((size, size)))
    np.fill_diagonal(matrix, 1)

    return matrix


def arange(
        shape_size: Iterable[int],
        start_from: int = 1,
        order: str = 'F',
) -> np.ndarray:
    """
    Generate a reshaped array with values ranging from 'start_from' to 
    'start_from + total_elements'.

    Parameters:
        shape_size (Iterable[int]): The shape of the output array.
        start_from (int, optional): The starting value for the range. 
            Defaults to 1.
        order (str, optional): The order of the reshaped array. 
            Defaults to 'F'.

    Returns:
        np.ndarray: The reshaped array with values ranging from 'start_from' 
            to 'start_from + total_elements'.

    Raises:
        ValueError: If 'shape_size' is not an iterable of integers, 
            'start_from' is not an integer, or 'order' is not a string.
        ValueError: If 'order' is not 'C' or 'F'.
    """
    if not isinstance(shape_size, Iterable) or \
            not all(isinstance(i, int) for i in shape_size):
        raise ValueError("'shape_size' must be an iterable of integers.")

    if not isinstance(start_from, int):
        raise ValueError("'start_from' must be an integer.")

    if not isinstance(order, str):
        raise ValueError("'order' must be a string.")

    if order not in ['C', 'F']:
        raise ValueError("'order' must be either 'C' or 'F'.")

    total_elements = np.prod(shape_size)
    values = np.arange(start_from, start_from+total_elements)
    reshaped_array = np.reshape(a=values, newshape=shape_size, order=order)

    return reshaped_array
