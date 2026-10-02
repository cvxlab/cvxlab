.. _numerical-problem-init-run-gsa:

Initialization and run of numerical problem(s)
==================================================

The loading of exogenous data, initialization
of the numerical problem, sampling, and repeated model evaluations are handled
together through ``run_uncertainty()``.

The method loads and validates the exogenous input data, generates or retrieves the
uncertainty samples according to the previously defined
:ref:`Uncertainty settings <uncertainty-settings>`, initializes the numerical
problem, solves the model for each sampled input configuration, and computes the
corresponding global sensitivity indices associated with the selected GSA method.

For each successful model evaluation, the variables previously marked with
``uncertainty_measure=True`` are collected. Model runs that do not reach an
optimal solution are retained in the uncertainty results with their solver status.

API: :py:meth:`cvxlab.Model.run_uncertainty`

Typical usage
---------------

.. code-block:: python

   model.run_uncertainty(
       verbose=False,
       solver="GUROBI",
       solver_settings={
           "DualReductions": 0,
           "reoptimize": True,
       },
       n_parallel=4,
       convergence_monitoring=False,
   )

Parameters description
-------------------------

``run_uncertainty()`` supports the standard model-run parameters described in
:ref:`Run numerical problem(s) <numerical-problem-run>`, along with additional
options specific to uncertainty model evaluations, described below:

.. list-table::
   :header-rows: 1
   :align: center
   :widths: 26 56 18

   * - Parameter
     - Description
     - Default
   * - ``resume``
     - If ``True``, resumes a previously interrupted uncertainty campaign using
       the existing uncertainty samples and temporarily saved model outputs.
     - ``False``
   * - ``n_parallel``
     - Number of uncertainty model evaluations to execute concurrently.
     - ``None``

For the remaining model-solution parameters, refer to
:ref:`Run numerical problem(s) <numerical-problem-run>`.