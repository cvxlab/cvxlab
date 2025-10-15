.. _user_defined_operators:

User-defined operators
======================

CVXlab allows new **user-defined operators** to be defined and used in model expressions.

This is particularly useful when the model requires specific mathematical functions
not available in CVXPY or when existing functions need to be adapted to the model's
specific needs. As example, it may be complex to define *probability density functions* 
of exogenous variables, or to implement *piece-wise linear functions with specific 
breakpoints*, based on simple mathematical expressions. 

In such cases, a new **user-defined operator** can be defined and then used in problem
expressions as any other built-in operator. Definition of new user-defined operator
is performed based on the following simple steps:

- First, the operator must be defined as a regular function in ``cvxlab/support/
  util_operators.py`` module. 
- Secondly the user-defined operator (i.e. the function name) must be added to 
  the list of allowed operators in the ``cvxlab/constants.py`` module. 
- Finally, the new operator can be used in model expressions, as any other built-in 
  operator.

Notably, some user-defined operators are already implemented in CVXlab, described
below.


Module reference
----------------

.. automodule:: cvxlab.support.util_operators
  :members:
  :undoc-members:
  :show-inheritance:
