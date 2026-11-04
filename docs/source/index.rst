Python laboratory for algebraic modelling
=========================================

**CVXlab** is an open-source Python laboratory for building and solving algebraic
models in a reproducible workflow:

- **Define models** using symbolic expressions and *YAML* or *Excel* settings.
- **Manage data** in *SQLite*, keeping model structure separate from numerical data.
- **Solve models** through a *CVXPY*-based numerical engine.
- **Connect models** with managed data exchange in *parallel*, *sequential*,
  and *integrated* solution modes.

**Version:** |version|
**Date:** |today|

**Useful links**: `PyPI <https://pypi.org/project/cvxlab/>`_ | 
`Source code <https://github.com/cvxlab/cvxlab>`_ | 
`Issue tracker <https://github.com/cvxlab/cvxlab/issues>`_ | 
`GitHub discussions <https://github.com/cvxlab/cvxlab/discussions>`_


How it works
------------

The figure below summarizes the package workflow. The detailed step-by-step
explanation is in the :ref:`user_guide`, while runnable examples are collected
in the :ref:`resources` section.

.. image:: _static/CVXlab_nutshell_light.svg
  :alt: CVXlab modeling process in a nutshell
  :align: center
  :class: only-light

.. image:: _static/CVXlab_nutshell_dark.svg
  :alt: CVXlab modeling process in a nutshell
  :align: center
  :class: only-dark


Why CVXlab
----------

- **General-purpose model generator**. Build a wide range of convex optimization models.
- **Almost no code required**. Define model structure through *YAML* or *Excel* 
  templates instead of hand-coding every object.
- **Centralized data management**. Organize data in a *SQLite* database for 
  traceable, reusable data handling.
- **Linked-model orchestration**. Coordinate multiple optimization sub-models 
  and exchange data across independent, chained, or iterative solving workflows.
- **Powerful engine embedded**. Build convex and decomposed optimization workflows 
  on top of `CVXPY <https://www.cvxpy.org/tutorial/intro/index.html>`_.


Start here
----------

.. list-table::
  :header-rows: 1
  :widths: 24 76

  * - Section
    - What you will find
  * - :doc:`get_started`
    - :doc:`Install CVXlab <installation>`, then :doc:`build and solve your first model <quick_start>`.
  * - :doc:`user_guide`
    - The full modeling workflow, from conceptual model definition to results export.
  * - :doc:`api_reference`
    - Technical reference for ``cvxlab.Model``, utilities, operators, constants, and defaults.
  * - :doc:`resources`
    - Tutorials, models gallery, related publications and how to cite CVXlab.
  * - :doc:`project`
    - Release history and guidelines for contributing to CVXlab.


.. toctree::
  :maxdepth: 1
  :hidden:

  Get Started <get_started>
  User Guide <user_guide>
  API Reference <api_reference>
  Resources <resources>
  Project <project>


.. note::
  CVXlab is developed by `Matteo V. Rocco <https://www.energia.polimi.it/en/people/rocco-matteo-vincenzo-2/>`_,
  Associate Professor at *SESAM group*, `Department of Energy, Politecnico di Milano
  <https://www.energia.polimi.it/en/>`_. The project is released under the
  `Apache License 2.0 <http://www.apache.org/licenses/>`_. 
