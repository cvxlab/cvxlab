"""User-defined operators for symbolic optimization problems.

This module allows you to define custom operators that extend the built-in 
operators available in cvxlab. Custom operators are automatically registered 
when this module is imported, ready to be used as symbolic operators in defining
symbolic problems.

USAGE:
------
Simply define the custom operators as standard functions in this file. 
The operator can be used in defining symbolic problem expressions simply by
writing its name followed by parentheses containing the required arguments (defined 
as problems variables).

FUNCTION GUIDELINES:
-------------------
1. Use clear, descriptive function names
2. Include comprehensive docstrings with Args, Returns, and Raises sections
3. Accept cvxpy Parameters, Constants, or Expressions as inputs
4. Return cvxpy Parameters, Constants, or Expressions as outputs
5. Include type hints for better code clarity
6. Validate input types and values with appropriate error handling
7. Use numpy for numerical computations on parameter values

IMPORT REQUIREMENTS:
-------------------
Make sure to import necessary libraries at the top of this file (already required
by cvxlab): numpy and cvxpy are commonly used, but you can import others as needed.

For more examples, refer to:
    cvxlab/support/util_operators.py


EXAMPLE - 'power' OPERATOR:
---------------------------

def power(
        base: cp.Parameter | cp.Expression,
        exponent: cp.Parameter | cp.Expression,
) -> cp.Parameter:
    '''Calculate the element-wise power of a matrix or scalar.

    This funciton calculates the element-wise power of the base, provided an 
    exponent. Either base or exponent can be a scalar.

    Args:
        base (cp.Parameter | cp.Expression): The base for the power operation. 
            The corresponding value can be a scalar or a 1-D numpy array.
        exponent (cp.Parameter | cp.Expression): The exponent for the power 
            operation. The corresponding value can be a scalar or a 1-D numpy array.

    Returns:
        cp.Parameter: A new parameter with the same shape as the input parameters, 
            containing the result of the power operation.

    Raises:
        TypeError: If the base and exponent are not both instances of cvxpy 
            Parameter or Expression.
        ValueError: If the base and exponent do not have the same shape and 
            neither is a scalar. If the base and exponent are not numpy arrays.
            If the base and exponent include non-numeric values.
    '''
    if not isinstance(base, cp.Parameter | cp.Expression) or \
            not isinstance(exponent, cp.Parameter | cp.Expression):
        raise TypeError(
            "Arguments of power method must be cvxpy Parameter or Expression.")

    if base.shape != exponent.shape:
        if base.is_scalar() or exponent.is_scalar():
            pass
        else:
            raise ValueError(
                "Base and exponent must have the same shape. In case of "
                "different shapes, one must be a scalar. "
                f"Shapes -> base: {base.shape}, exponent: {exponent.shape}.")

    base_val: np.ndarray = base.value
    exponent_val: np.ndarray = exponent.value

    if not isinstance(base.value, np.ndarray) or \
            not isinstance(exponent.value, np.ndarray):
        raise ValueError("Base and exponent must be numpy arrays.")

    if not (
        np.issubdtype(base.value.dtype, np.number) and
        np.issubdtype(exponent.value.dtype, np.number)
    ):
        raise ValueError("Base and exponent must be numeric.")

    power = np.power(base_val, exponent_val)
    return cp.Parameter(shape=power.shape, value=power)
"""
import numpy as np
import cvxpy as cp


# Define your custom operators below
# -----------------------------------
