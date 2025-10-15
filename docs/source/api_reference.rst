API reference
=============

CVXlab is designed to be intuitive enough so that it may be used without delving 
into APIs structures. Reading :ref:`User Guide <user_guide>`, practicing with the 
tutorial notebook available in the :ref:`Tutorial <tutorial>` section, and  
looking at existing models in :ref:`Models gallery <models_gallery>` will suffice 
in acquainting you with the package. Nonetheless, API reference are here included 
for those who are comfortable reading technical documentation. 

The classes and functions documented in this section are those imported into the 
*CVXlab* namespace. The documentation is grouped the following sections: 
:ref:`Model <api_model>` section documents the main package class cvxlab.Model, 
embedding all the main package APIs necessary to generate, handle and solve the 
numerical model. :ref:`Utility functions <api_utility_functions>` section documents 
various utility functions available in the package, including functions for 
initializing model directory and handling model class instances. :ref:`Constants 
<api_constants>` documents the cvxlab.constants module, which includes various 
constants and default settings used throughout the package.


.. toctree::
   :maxdepth: 1

   apidocs/model
   apidocs/utility_functions
   apidocs/constants
   apidocs/user_defined_operators