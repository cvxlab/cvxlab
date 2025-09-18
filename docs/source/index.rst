CVXlab documentation
====================

**Version:** 1.0.0
**Date:** Sep 2025

**Useful Links:**
- `PyPI Page < ... >`_
- `Source GitHub Repository <https://github.com/cvxlab/cvxlab>`_
- `Issue Tracker <https://github.com/cvxlab/cvxlab/issues>`_

**CVXlab - Open-source Python laboratory for convex algebraic modeling**

CVXlab provides an efficient pipeline and a set of tools for defining, managing
and solving numerical optimization problems. Its main features are summarized below:

- **Very low coding skills requested**: mathematical problems settings based on 
  Excel/yaml, and problem expressions are defined literally as they are written 
  on paper.

- **Centralized data management based on SQLite databases**: this allows to easily 
  store, retrieve, and manage large datasets for optimization problems, and enables 
  to easily visualize and analyze results based on Business Intelligence tools 
  (PowerBI, ...).

- **Powerful engine embedded**: numerical problems generated and solved based on 
  CVXPY, a convex optimization modeling library for Python 
  (see `CVXPY documentation <https://www.cvxpy.org/tutorial/intro/index.html>`_).

- **Flexibility**: CVXlab enables users to define and solve parametric problems 
  easily, and to handle nonlinear problems as sequence of convex problems (i.e. 
  decomposed into coupled convex subproblems), solving them iteratively using a 
  block Gauss-Seidel (alternating optimization) scheme. 


.. toctree::
   :maxdepth: 1
   :caption: Contents:
   
   installation
   user_guide
   api_reference
   examples


.. note::
   - CVXlab has conceived and developed by *Matteo V. Rocco*, Associate Professor 
     at *SESAM group*, *Department of Energy*, *Politecnico di Milano*, Italy 
     (`<https://www.energia.polimi.it/en/>`_).
   - CVXlab is an open-source project based on the Apache License Version 2.0, 
     January 2004 (http://www.apache.org/licenses/). Contributions and feedback 
     are welcome!

