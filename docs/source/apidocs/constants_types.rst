.. _api_constants_types:

Constant data types
===================

CVXlab supports a variety of built-in constant data types (see next section). 
In defining models, it may be necessary to define other constants. This can be 
accomplished in the following two ways:

1. **Local user-defined constants**. Ideal for model users, who can define custom 
   constants in the local model directory by defining the related function in the 
   *user_defined_constants.py* module, which is automatically loaded when 
   generating a Model instance. This way, users can extend the package with 
   their own custom constants without modifying the package code (ideal for model 
   users). See :ref:`user defined constants template <api_user_defined_constants>` 
   for detailed instructions on how to define and use local user-defined constants.

2. **Adding a new built-in constant**. Adding a new constant directly in the current 
   package module ``cvxlab.support.util_constants`` requires defining a new function 
   in this module, which is embedded in the package as a built-in constant. 
   This approach is ideal **only when** a constant is expected to be widely used across 
   different models and users.


.. _built-in-constants-types-reference:

Built-in constant types reference
----------------------------------

.. automodule:: cvxlab.support.util_constants
  :members:
  :undoc-members: 
  :show-inheritance:
  :exclude-members: 
