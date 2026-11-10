.. _resources:

Resources
=========

This section collects tutorials and example models for learning and applying
**CVXlab**. Core tutorials introduce the modeling workflow described in the
:ref:`User Guide <user_guide>`, while applied tutorials explore domain-specific
workflows with supporting tools and data.

Tutorial directories (with supplementary modeling materials such as Jupyter
Notebooks, Excel concept files, input-data files and SQLite databases) can be
downloaded where linked in the tables below, so that you can run them locally
on your machine.


.. _tutorials:

Core tutorials
--------------

Learn CVXlab's modeling workflow and capabilities through a series of
production-planning examples.

.. list-table::
    :header-rows: 1
    :widths: 30 60 10

    * - Tutorial
      - Description
      - Material
    * - :doc:`Production planning <tutorials/production_planning/production_planning>`
      - Complete workflow for defining and solving a simple production planning 
        under resource constraints. Step by step guide aligned with :ref:`User 
        Guide <model_generation_from_scratch>`. **[Ideal for newbies]**.
      - :download:`link <tutorials/production_planning/production_planning.zip>`
    * - :doc:`Handling non-linearities <tutorials/production_planning_nonlinear/production_planning_nonlinear>`
      - Non-linear production planning under resource constraints. Similar to the 
        previous production planning tutorial, but handling non-linearities explicitly. 
      - :download:`link <tutorials/production_planning_nonlinear/production_planning_nonlinear.zip>`
    * - :doc:`Problem decomposition <tutorials/production_planning_decomposition/production_planning_decomposition>`
      - Reformulating and decomposing the previous non-linear production planning 
        problem into coupled convex sub-problems solved iteratively (block Gauss–Seidel).
      - :download:`link <tutorials/production_planning_decomposition/production_planning_decomposition.zip>`
    * - :doc:`Sequential problems solution <tutorials/production_planning_sequential/production_planning_sequential>`
      - Sequential solution of the original production planning problem, by first 
        calibrating the model and deriving parameters, then solving the production 
        planning problem with calibrated parameters.
      - :download:`link <tutorials/production_planning_sequential/production_planning_sequential.zip>`


Applied tutorials
-----------------

Apply CVXlab to domain-specific problems using external data and supporting tools.

.. list-table::
    :header-rows: 1
    :widths: 30 60 10

    * - Tutorial
      - Description
      - Material
    * - :doc:`Input-output impact assessment <tutorials/input_output_analysis_mario/input_output_analysis_mario>`
      - Download and pre-process input-output data with MARIO, then build and
        solve an algebraic model in CVXlab to perform nation-wide impact assessments.
      - :download:`link <tutorials/input_output_analysis_mario/ioa_mario.zip>`


.. _models_gallery:

Models gallery
--------------

A collection of published models built with CVXlab, including links to data
repositories where models and input data can be found.

.. list-table::
    :header-rows: 1
    :widths: 40 45 15

    * - Model
      - Description
      - Repository
    * - **Parametric LCA model of floating offshore wind farm**
        *(Ghezzi D, Rocco MV | 2025)*
      - Parametric life-cycle assessment of electricity generation from
        semi-submersible floating offshore wind farms. Covers 192 configurations
        defined by turbine capacity, platform and mooring material, end-of-life
        treatment, capacity factor, cable type, and steel origin.
      - `Dataset <https://doi.org/10.5281/zenodo.17161021>`__
        `Related article <https://www.scopus.com/pages/publications/105039704468?origin=resultslist>`__


.. _publications:

Publications
------------

A collection of published articles that use CVXlab for modeling and solving
optimization problems.

- **Parametric life cycle assessment of carbon footprint of electricity generation from floating offshore wind farms**
  *(Ghezzi D, Rocco MV | Sustainable Energy Technology and Assessments | 2025)* |
  `Article link <https://www.scopus.com/pages/publications/105039704468?origin=resultslist>`__



.. toctree::
  :maxdepth: 1
  :hidden:
  :caption: Core tutorials

  tutorials/production_planning/production_planning
  tutorials/production_planning_nonlinear/production_planning_nonlinear
  tutorials/production_planning_decomposition/production_planning_decomposition
  tutorials/production_planning_sequential/production_planning_sequential

.. toctree::
  :maxdepth: 1
  :hidden:
  :caption: Applied tutorials

  tutorials/input_output_analysis_mario/input_output_analysis_mario