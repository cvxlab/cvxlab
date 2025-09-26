CVXlab documentation
====================

**CVXlab - Open-source Python laboratory for convex algebraic modeling**

**Version:** |version|
**Date:** |today|

**Useful Links:**
- `PyPI Page <https://>`_
- `Source GitHub Repository <https://github.com/cvxlab/cvxlab>`_
- `Issue Tracker <https://github.com/cvxlab/cvxlab/issues>`_



Package features
----------------

CVXlab provides an efficient pipeline and a set of tools for defining, managing
and solving numerical optimization problems. Its main features are summarized below:

- **General-purpose model generator**: CVXlab enables to define a wide range of convex 
  optimization problems, as well as nonlinear problems handled as sequence of convex 
  problems (i.e. decomposed into coupled convex subproblems), solving them iteratively 
  using a block Gauss-Seidel (alternating optimization) scheme. Numerical problems
  parametric analysis is also supported and made easy.

- **User experience**: mathematical problems settings based on Excel or yaml files, 
  data collection based on Excel spreadsheets, and problem expressions defined 
  literally as they are written on paper. Users can focus on the modeling of the 
  problem rather than on programming issues. Very low coding skills are required.

- **Centralized data management based on SQLite databases**: model data are arranged 
  in a SQLite database (`SQLite documentation <https://sqlite.org/index.html>`_), 
  which allows to easily store, retrieve, and manage datasets for optimization 
  problems. Database structure enables to easily visualize and analyze results 
  through Business Intelligence tools (PowerBI, ...).

- **Powerful engine embedded**: numerical problems generated and solved based on 
  CVXPY, a convex optimization modeling library for Python (see `CVXPY documentation 
  <https://www.cvxpy.org/tutorial/intro/index.html>`_ for a comprehensive description
  of the package capabilities).


CVXlab in a nutshell
--------------------

text


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation
   user_guide
   tutorial
   resources
   api_reference


.. note::
   - CVXlab has conceived and developed by *Matteo V. Rocco*, Associate Professor 
     at *SESAM group*, `Department of Energy, Politecnico di Milano 
     <https://www.energia.polimi.it/en/>`_, Italy.
   - CVXlab is an open-source project based on the `Apache License Version 2.0, 
     (January 2004) <http://www.apache.org/licenses/>`_. Contributions and feedback 
     are welcome!

