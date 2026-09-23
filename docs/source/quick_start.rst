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

For each scenario :math:`s`, solve the following independent problem in vector form:

.. math::

   \begin{aligned}
   \text{maximize}\quad & c x^{\mathsf{T}} \\
   \text{subject to}\quad & e x^{\mathsf{T}} \leq E_{\text{max}}, \\
   & m x^{\mathsf{T}} \leq M_{\text{max}}, \\
   & x \geq 0.
   \end{aligned}

Here :math:`x`, :math:`c`, :math:`e`, and :math:`m` are row vectors over
products: production, unit profit, energy requirements, and material requirements,
respectively. The scalars :math:`E_{\text{max}}` and :math:`M_{\text{max}}`
are energy and material availability. Non-negativity
applies to every component of :math:`x`.

This matches the YAML formulation below: ``dim: cols`` places products along
the columns, ``@`` denotes matrix multiplication, and ``tran(x)`` denotes the
transpose. CVXlab handles the scenario index automatically, so the same symbolic
expressions apply to both scenarios.

There are two products, two resources, and two availability scenarios. The
numbers are intentionally small; the separation between data tables and
symbolic variables is representative of a larger model.

Product 1 uses less energy, while product 2 uses less material. Energy availability
changes across scenarios; material availability stays fixed. Filtered variables
``e`` and ``m`` select energy and material coefficients from the same data table.
Energy availability is ``E_max``; material availability is ``M_max``.

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
       description: resources consumed in production | dimension set
       filters:
           type: [energy, material]

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
           e:
               Resources:
                   dim: rows
                   filters: {type: energy}
               Products:
                   dim: cols
           m:
               Resources:
                   dim: rows
                   filters: {type: material}
               Products:
                   dim: cols

   energy_availability:
       description: available energy in each scenario
       type: exogenous
       coordinates: [Resources, Scenarios]
       variables_info:
           E_max:
               Resources:
                   dim: rows
                   filters: {type: energy}

   material_availability:
       description: available material shared by all scenarios
       type: exogenous
       coordinates: [Resources]
       variables_info:
           M_max:
               Resources:
                   dim: rows
                   filters: {type: material}


Data tables organize stored data; the names inside ``variables_info`` identify
symbolic variables. Here ``e`` and ``m`` select energy and material coefficients
from ``resource_requirements``. Energy availability ``E_max`` varies by scenario;
material availability ``M_max`` has no scenario dimension and is shared by all runs.

``problem.yml``

.. code-block:: yaml

   objective:
       - Maximize(c @ tran(x))

   expressions:
       - e @ tran(x) <= E_max
       - m @ tran(x) <= M_max
       - x >= 0

   description:
       - maximize total profit
       - respect energy availability in each scenario
       - respect material availability shared by all scenarios
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

The constructor generates ``quick_start/sets.xlsx``. Fill the
``*_Name`` column in each sheet with the following coordinates, one per row:

.. list-table:: Set coordinates
   :header-rows: 1
   :widths: 35 65

   * - Sheet
     - Coordinates
   * - ``_set_PRODUCTS``
     - ``product_1``, ``product_2``
   * - ``_set_RESOURCES``
     - ``resource_1``, ``resource_2``
   * - ``_set_SCENARIOS``
     - ``low``, ``high``

In ``_set_RESOURCES``, also fill the generated ``Resources_type`` column:

.. list-table:: Resource filters
   :header-rows: 1

   * - ``Resources_Name``
     - ``Resources_type``
   * - ``resource_1``
     - ``energy``
   * - ``resource_2``
     - ``material``

These labels select the rows used by ``e``, ``m``, ``E_max``, and ``M_max``. The filter labels alone
do not impose constraints: the availability limit is defined in ``problem.yml``.
Save and close the workbook before continuing.

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
   * - ``energy_availability``
     - (``resource_1``, ``low``); (``resource_1``, ``high``);
     - 2; 8;
   * - ``material_availability``
     - ``resource_2``
     - 6

``E_max`` selects only the energy rows of ``energy_availability``; ``M_max``
selects only the material row of ``material_availability``. Fill unused rows
with 0; they do not enter the constraints. Both tables are indexed by resource,
but only energy availability also has a scenario dimension.
Save and close the workbook before solving.

4. Solve and inspect the results
---------------------------------

Load the input data, generate one numerical problem per scenario, solve them,
and export the endogenous results to SQLite:

.. code-block:: python

   model.refresh_database_and_initialize_problem()
   model.run_model(solver="CLARABEL")
   model.load_results_to_database()

   for scenario_key, scenario in model.scenarios.iterrows():
       print(f"\nScenario: {scenario.iloc[0]}")
       print(model.variable(name="x", scenario_key=scenario_key).round(2))

:meth:`cvxlab.Model.variable` returns the optimal production volumes as a
DataFrame for each scenario. The results are also exported to the
``production`` table in ``quick_start/database.db``.

.. list-table:: Expected production volumes (up to solver tolerances)
   :header-rows: 1

   * - Scenario
     - ``product_1``
     - ``product_2``
   * - low
     - 2
     - 0
   * - high
     - 0.8
     - 3.6

With scarce energy, production concentrates on product 1, which earns more
profit per unit of energy. With more energy available, the optimal mix shifts
towards product 2, which uses less material. Both scenarios fully use the
available resources.

Next steps
----------

- Follow the :ref:`resource-constrained production planning problem
  <tutorial-production-planning>` tutorial for a detailed applied example.
- Read the :ref:`user_guide` to understand each stage of the modeling workflow.
- Use the :ref:`guided_interface` if you prefer to perform the same workflow
  through a menu-driven interface.
