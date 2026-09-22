.. _quick_start:

Quick Start
===========

This page builds and solves a small model in a few minutes. The example is
deliberately compact, but it uses the same CVXlab workflow that supports larger
models: the model structure is separate from numerical data, one problem is
generated for each scenario, and results are stored in SQLite.

It introduces the workflow, not every modeling concept. For a detailed,
applied walkthrough, continue with the :ref:`resource-constrained production
planning problem <tutorial-production-planning>` tutorial. The :ref:`user_guide`
provides the complete reference for creating your own models.

The model
---------

For each scenario :math:`s`, choose non-negative quantities :math:`x_i` that
maximize their total value while respecting two resource limits:

.. math::

   \begin{aligned}
   \operatorname{maximize}\quad & \sum_i c_i x_{i,s} \\
   \text{subject to}\quad & \sum_i A_{r,i}x_{i,s} \leq b_{r,s}
   && \forall r, s, \\
   & x_{i,s} \geq 0 && \forall i, s.
   \end{aligned}

There are two products, two resources, and two availability scenarios. The
numbers are intentionally small; the separation between data tables and
symbolic variables is representative of a larger model.

1. Create the model directory
-------------------------------

Create an empty model directory with YAML setup files:

.. code-block:: python

   import cvxlab

   cvxlab.create_model_dir(
       model_dir_name="quick_start",
       main_dir_path=".",
       settings_file_type="yml",
   )

This creates ``quick_start/`` with ``structure_sets.yml``,
``structure_variables.yml``, and ``problem.yml``. Replace their template
content with the following definitions.

``structure_sets.yml``

.. code-block:: yaml

   Products:
       description: products whose optimal production volumes are to be determined | dimension set

   Resources:
       description: resources that constrain production | dimension set

   Scenarios:
       description: alternative resource-availability conditions | inter-problem set
       split_problem: True

``structure_variables.yml``

.. code-block:: yaml

   production:
       description: production volumes to be determined
       type: endogenous
       coordinates: [Products, Scenarios]
       variables_info:
           x:
               Products:
                   dim: cols

   unit_profit:
       description: profit earned per unit of each product
       type: exogenous
       coordinates: [Products]
       variables_info:
           c:
               Products:
                   dim: cols

   resource_requirements:
       description: resource consumption required to produce one unit of each product
       type: exogenous
       coordinates: [Resources, Products]
       variables_info:
           A:
               Resources:
                   dim: rows
               Products:
                   dim: cols

   resource_availability:
       description: available amount of each resource in each scenario
       type: exogenous
       coordinates: [Resources, Scenarios]
       variables_info:
           b:
               Resources:
                   dim: rows

The names on the left (for example ``unit_profit``) identify *data tables*.
The shorter names inside ``variables_info`` (``x``, ``c``, ``A``, and ``b``)
identify the symbolic variables used in the mathematical problem.

``problem.yml``

.. code-block:: yaml

   objective:
       - Maximize(c @ tran(x))

   expressions:
       - A @ tran(x) - b <= 0
       - x >= 0

   description:
       - maximize total profit
       - respect the available amount of every resource
       - define non-negative production volumes

2. Create the model and fill its sets
--------------------------------------

Create the :class:`cvxlab.Model` instance:

.. code-block:: python

   model = cvxlab.Model(
       model_dir_name="quick_start",
       main_dir_path=".",
       model_settings_from="yml",
   )

The constructor generates ``quick_start/sets.xlsx``. Fill the sole
``*_Name`` column in each sheet with the following coordinates:

.. list-table:: Set coordinates
   :header-rows: 1
   :widths: 35 65

   * - Sheet
     - Coordinates
   * - ``_set_Products``
     - ``product_1``, ``product_2``
   * - ``_set_Resources``
     - ``resource_1``, ``resource_2``
   * - ``_set_Scenarios``
     - ``low``, ``high``

3. Generate and fill the numerical input data
----------------------------------------------

Generate the SQLite database and an Excel workbook containing the exogenous
data tables:

.. code-block:: python

   model.initialize_model_environment()

This creates ``quick_start/input_data/input_data.xlsx``. Leave the coordinate
and ``id`` columns unchanged; fill only the ``values`` column. Match values to
the generated rows using their coordinate columns:

.. list-table:: Input values
   :header-rows: 1
   :widths: 25 60 15

   * - Sheet
     - Coordinates
     - ``values``
   * - ``unit_profit``
     - ``product_1``; ``product_2``
     - 3; 5
   * - ``resource_requirements``
     - (``resource_1``, ``product_1``); (``resource_1``, ``product_2``);
       (``resource_2``, ``product_1``); (``resource_2``, ``product_2``)
     - 1; 2; 3; 1
   * - ``resource_availability``
     - (``resource_1``, ``low``); (``resource_1``, ``high``);
       (``resource_2``, ``low``); (``resource_2``, ``high``)
     - 4; 8; 3; 6

4. Solve and inspect the results
---------------------------------

Load the input data, generate one numerical problem per scenario, solve them,
and export the endogenous results to SQLite:

.. code-block:: python

   model.refresh_database_and_initialize_problem()
   model.run_model(solver="CLARABEL")
   model.load_results_to_database()

   for scenario_key, scenario in model.scenarios.iterrows():
       print(f"\nScenario {scenario_key}:")
       print(scenario)
       print(model.variable(name="x", scenario_key=scenario_key))

The ``production`` table in ``quick_start/database.db`` now contains the
optimal production volumes for both scenarios. The corresponding objective
values are 10.2 for ``low`` and 20.4 for ``high``. The loop uses
:meth:`cvxlab.Model.variable` to print the endogenous variable ``x`` for each
scenario.

Next steps
----------

- Follow the :ref:`resource-constrained production planning problem
  <tutorial-production-planning>` tutorial for a detailed applied example.
- Read the :ref:`user_guide` to understand each stage of the modeling workflow.
- Use the :ref:`guided_interface` if you prefer to perform the same workflow
  through a menu-driven interface.
