.. _api_symbolic_operators:

Symbolic operators
==================

CVXlab supports a variety of built-in mathematical operators that can be used 
within symbolic expressions. These operators include standard arithmetic operations, 
matrix operations, and various mathematical functions, allowing users to construct
complex expressions for optimization problems. 

Symbolic operators defined as **mathematical signs** include: 

- ``==`` : Equality
- ``>=`` : Greater than or equal comparison
- ``<=`` : Less than or equal comparison
- ``+``  : Addition (works for both scalars and matrices)
- ``-``  : Subtraction (works for both scalars and matrices)
- ``*``  : Multiplication (element-wise for matrices)
- ``/``  : Division (element-wise for matrices)
- ``@``  : Matrix multiplication (for matrices)

Other **regular symbolic operators** works like functions, taking variables as 
inputs arguments and returning a cvxpy expression when symbolic expression is processed.
These operators are defined as functions in module ``cvxlab.support.util_operators``,
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


.. _adding_symbolic_operators:

Adding symbolic operators
-------------------------

CVXlab allows **new symbolic operators** to be defined and used in model expressions.
This is particularly useful when the model requires specific mathematical functions
not available in CVXPY or when existing functions need to be adapted to the model's
specific needs. As example, it may be complex to define *probability density functions* 
of exogenous variables, or to implement *piece-wise linear functions with specific 
breakpoints*, based on simple mathematical expressions. 

In such cases, a symbolic operator can be defined and then used in problem expressions 
as any other operator listed above. Definition of new operators should be performed
in two ways:

1. *Adding a new built-in symbolic operator to the CVXPY library.* 
   To do so, it is sufficient to add a new function the module `cvxlab.support.
   util_operators.py`, following instructions provided in the module. This way, 
   the new operator will be available to all users of the package. This approach 
   is recommended when the operator is generally useful and can be reused in 
   multiple models. It is recommended to properly document and test the new operator 
   before committing it to the main package (see :doc:`/contributing`).

2. *Defining a new custom symbolic operator in the model directory.*
   To accomplish this, users can define new operator/s as regular functions in 
   the :ref:`user_defined_operators.py <api_user_defined_operators>` file (template 
   can be found in ``template/user_defined_operators.py``). New operators are loaded 
   once Model instance is generated. This way, users can use their own custom 
   symbolic operators in defining problems without modifying the package code 
   (ideal for model users).


Built-in operators reference
----------------------------

.. automodule:: cvxlab.support.util_operators
  :members:
  :undoc-members: 
  :show-inheritance:
  :exclude-members: operator
