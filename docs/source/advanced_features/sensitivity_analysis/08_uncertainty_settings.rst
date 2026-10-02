.. _uncertainty-settings:

Uncertainty settings
========================

Before running the uncertainty model evaluations, the sampling and global sensitivity analysis
configuration must be defined through ``uncertainty_settings()``. 

Typical usage
-----------------
.. code-block:: python

   model.uncertainty_settings(
       sampling_method="morris",
       gsa_method="morris",
       sampling_kwargs={
           "N": 100,
           "num_levels": 4,
           "optimal_trajectories": 10,
           "seed": 123,
       },
       gsa_kwargs={
           "print_to_console": True,
       },
   )

API: :py:meth:`cvxlab.Model.uncertainty_settings`

Parameters description
------------------------

.. list-table::
   :header-rows: 1
   :align: center
   :widths: 24 58 18

   * - Parameter
     - Description
     - Default
   * - ``sampling_method``
     - SALib sampling method used to generate the uncertain input
       configurations. Supported methods are ``"morris"``, ``"sobol"``
       and ``"latin"``.
     - Required
   * - ``gsa_method``
     - SALib method used to compute global sensitivity indices.
       Supported methods are ``"morris"``, ``"sobol"``, ``"delta"``
       and ``"rbd_fast"``. If ``None``, model evaluations are performed
       without subsequent GSA.
     - ``None``
   * - ``sampling_kwargs``
     - Dictionary of method-specific arguments passed to the selected SALib
       sampling method.
     - ``None``
   * - ``gsa_kwargs``
     - Dictionary of method-specific arguments passed to the selected SALib
       analysis method.
     - ``None``
   * - ``groups``
     - If ``True``, uncertain parameters are analyzed according to the
       groups defined through ``uncertainty_group_name``. Grouped sampling
       is supported for Morris and Sobol sampling.
     - ``False``
   * - ``measures``
     - List of uncertainty measures to include in the GSA. If ``None``,
       all model outputs previously marked with
       ``uncertainty_measure=True`` are considered.
     - ``None``
   * - ``scenarios``
     - List of model scenarios to include in the GSA. If ``None``, all
       available scenarios are considered.
     - ``None``
   * - ``save_samples``
     - If ``True``, the generated uncertainty samples are exported.
     - ``True``
   * - ``save_measures``
     - If ``True``, the model outputs collected across the uncertainty
       evaluations are exported.
     - ``True``
   * - ``save_gsa``
     - If ``True``, the computed GSA results are exported. This setting
       is ignored when no ``gsa_method`` is specified.
     - ``True``
   * - ``temp_save``
     - If ``True``, collected uncertainty measures are progressively saved
       during model evaluation. Requires ``save_measures=True``.
     - ``True``
   * - ``file_format``
     - File format used to export uncertainty samples, measures and GSA
       results.
     - ``"xlsx"``

``sampling_kwargs`` and ``gsa_kwargs`` depend on the selected SALib methods.
For the complete list of method-specific arguments, refer to the corresponding
SALib sampling and analysis documentation on `SALib <https://salib.readthedocs.io/>`_.
