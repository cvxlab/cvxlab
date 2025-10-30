.. _api_constant_data_types:

Constant data types
===================

CVXlab supports a variety of constants data types 


that can be used in defining 
symbolic expressions. These operators include standard arithmetic operations, 
matrix operations, and various mathematical functions.

**Standard operators** include: 

- ``/``  : Division (element-wise for matrices)
- ``@``  : Matrix multiplication (for matrices)

**Other operators** are defined as functions in module ``cvxlab.support.util_operators``,
and are listed below:

- ``weib()`` : Generate a Weibull probability density function based on a set of parameters
  (:func:`weibull_distribution() <cvxlab.support.util_operators.weibull_distribution>`)


.. _adding_user_defined_constants:

Adding user-defined constant data types
---------------------------------------

symbolic operators are defined as functions, so arguments are defined in the symbolic problem directly.
for such reason, once the user defined function is defined, there is no need to manually
register it anywhere else in the package.

define the new constant as a function in ``cvxlab/support/util_constants.py`` module. 
the function must be decorated with the key ``@constant('constant_name')``, where 
``constant_name`` is the name that will be used to call the constant in model settings.

these functions are called in the Variable class, in the method 
``define_constant()``, which is responsible for generating constant data based on
the variable shape and constant type. in case a new constant requires additional
arguments, the method can be adapted accordingly.

in case adding a user-defined constant type is particularly complex, consider 
avoiding this process by simply defining the variable as exogenous, and then manually
defining the constant data as input for the model (simpler, but may be less elegant and
prone to errors).




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

.. automodule:: cvxlab.support.util_constants
  :members:
  :undoc-members: 
  :show-inheritance:
  :exclude-members: 
