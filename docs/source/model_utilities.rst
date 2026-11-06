.. _utilities:

Inspecting and managing models
==============================

Use these utilities to inspect a Model instance, maintain its SQLite database,
and compare results with a reference database. For the overall sequence of
modeling activities, return to the :ref:`user_guide`.

Inspect model contents
----------------------

.. list-table:: CVXlab Model instance inspection utilities
  :header-rows: 1
  :widths: 30 68

  * - API
    - Description
  * - :py:attr:`~cvxlab.Model.sets`
    - **Property** reporting the list of model set keys.
  * - :py:attr:`~cvxlab.Model.data_tables`
    - **Property** reporting the list of model data table keys.
  * - :py:attr:`~cvxlab.Model.variables`
    - **Property** reporting the list of model variable keys.
  * - :py:attr:`~cvxlab.Model.is_problem_solved`
    - **Property** indicating the status of the numerical problem.
  * - :py:meth:`~cvxlab.Model.set`
    - **Method** allowing inspection of a specific set, including related
      coordinates and other attributes.
  * - :py:meth:`~cvxlab.Model.variable`
    - **Method** allowing inspection of a specific variable, including related
      data table, shape, filters and other attributes.


Manage the database and check results
------------------------------------------------------------

The following methods maintain model data structures and help verify results.

.. list-table:: CVXlab Model instance helper utilities
  :header-rows: 1
  :widths: 30 68

  * - API
    - Description
  * - :py:meth:`~cvxlab.Model.reinitialize_sqlite_database`
    - **Method** allowing regeneration of a blank SQLite database from the
      current model structure (sets and data tables). Useful to reset the
      database to a clean state.
  * - :py:meth:`~cvxlab.Model.check_model_results`
    - **Method** allowing comparison of the model SQLite database with a
      reference SQLite database, to verify that results are coherent with
      expected values.
  * - :py:meth:`~cvxlab.Model.update_sets_tables`
    - **Method** allowing update of sets tables in the SQLite database based on
      the current model structure and coordinates. Useful after changing set
      coordinates, for example to add aggregation categories.
