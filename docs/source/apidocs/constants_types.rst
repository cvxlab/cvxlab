.. _api_constants_types:

Constant data types
===================

CVXlab supports a variety of constants data types 



There are two ways to add a new user-defined constant:

1. Add a new constant directly in the current module `cvxlab.support.util_constants`:
   simply define a new function in this module, that will be embedded in the package
   as a built-in constant.

2. Users can define custom constants in their model directory by defining the related
   function in the 'user_defined_constants.py' file, and loading the module when
   generating the Model instance. This way, users can extend the package with their
   own custom constants without modifying the package code (ideal for model users).




Built-in constants types reference
----------------------------------

.. automodule:: cvxlab.support.util_constants
  :members:
  :undoc-members: 
  :show-inheritance:
  :exclude-members: 
