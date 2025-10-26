.. _api_symbolic_operators:

Symbolic operators
==================

CVXlab supports a variety of mathematical operators that can be used in defining 
symbolic expressions. These operators include standard arithmetic operations, 
matrix operations, and various mathematical functions.

**Standard operators** include: 

- ``==`` : Equality
- ``>=`` : Greater than or equal comparison
- ``<=`` : Less than or equal comparison
- ``+``  : Addition (works for both scalars and matrices)
- ``-``  : Subtraction (works for both scalars and matrices)
- ``*``  : Multiplication (element-wise for matrices)
- ``/``  : Division (element-wise for matrices)
- ``@``  : Matrix multiplication (for matrices)

**Other operators** are defined as functions in module ``cvxlab.support.util_operators``,
and are listed below:

- ``Minimize()`` : Create a maximization objective 
  (:func:`minimize() <cvxlab.support.util_operators.minimize>`)
- ``Maximize()`` : Create a maximization objective
  (:func:`maximize() <cvxlab.support.util_operators.maximize>`)
- ``tran()`` : Transposition of matrix or vector
  (:func:`transposition() <cvxlab.support.util_operators.transposition>`)
- ``diag()`` : Extract the diagonal of a matrix or create a diagonal matrix from 
  a vector (:func:`diagonal() <cvxlab.support.util_operators.diagonal>`)
- ``sum()`` : Sum elements of a matrix or vector along a specified axis 
  (:func:`sum() <cvxlab.support.util_operators.summation>`)
- ``mult()`` : Element-wise multiplication of two matrices or vectors
  (:func:`mult() <cvxlab.support.util_operators.multiplication>`)
- ``pow()`` : Element-wise power of matrix or scalar base by an exponent 
  (:func:`power() <cvxlab.support.util_operators.power>`)
- ``minv()`` : Calculate the inverse of matrix 
  (:func:`matrix_inverse() <cvxlab.support.util_operators.matrix_inverse>`)
- ``shift()`` : Shift values of the diagonal of an identity matrix of upwards/downwards 
  (:func:`shift() <cvxlab.support.util_operators.shift>`)
- ``annuity()`` : Calculate the annuity factor based on a set of parameters 
  (:func:`annuity() <cvxlab.support.util_operators.annuity>`)
- ``weib()`` : Generate a Weibull probability density function based on a set of parameters
  (:func:`weibull_distribution() <cvxlab.support.util_operators.weibull_distribution>`)


.. _adding_user_defined_operators:

Adding user-defined operators
-----------------------------

CVXlab allows new **user-defined** operators to be defined and used in model expressions.
This is particularly useful when the model requires specific mathematical functions
not available in CVXPY or when existing functions need to be adapted to the model's
specific needs. As example, it may be complex to define *probability density functions* 
of exogenous variables, or to implement *piece-wise linear functions with specific 
breakpoints*, based on simple mathematical expressions. 

In such cases, a new operator can be defined and then used in problem expressions 
as any other operator listed above. Definition of new operators should be performed
by defininig a new regular function in ``cvxlab/support/util_operators.py`` module. 
The function must be decorated with the key ``@operator('function_name')``, where 
``function_name`` is the name that will be used to call the operator in model expressions.

Before committing the new operator to the main package, it is recommended to:

- Provide comprehensive docstring accompanying the defined function.
- Include the new operator in the list of available operators in this documentation 
  page (``docs/source/apidocs/symbolic_operators.rst``).
- Add appropriate unit tests in ``tests/unit/test_util_operators.py`` to ensure the 
  operator behaves as expected.


Available operators reference
-----------------------------

.. automodule:: cvxlab.support.util_operators
  :members:
  :undoc-members: 
  :show-inheritance:
  :exclude-members: operator
