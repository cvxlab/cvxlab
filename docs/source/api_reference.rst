API reference
=============

CVXlab is designed to be intuitive enough so that it may be used without delving 
into APIs structures. Reading :ref:`User Guide <user_guide>` and example of models 
available in the :ref:`Tutorial <tutorial>` section will suffice in acquainting 
you with the package. Nonetheless, API reference are here included for those who 
are comfortable reading technical documentation. 

The classes and functions documented in this section are those imported into the 
*CVXlab* namespace. The documentation is grouped the following sections: *model*,
*constants* and *utility functions*. 
The model section documents the main package class cvxlab.Model, embedding all the
main package APIs necessary to generate, handle and solve the numerical model.
The constants section documents the cvxlab.constants module, which includes
various constants and default settings used throughout the package.
The utility functions section documents various utility functions available in the
package, including functions for initializing model directory and handling model
class instances.


.. toctree::
   :maxdepth: 1

   apidocs/model
   apidocs/utility_functions
   apidocs/constants
