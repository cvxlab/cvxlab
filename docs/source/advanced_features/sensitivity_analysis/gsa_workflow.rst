.. _gsa_workflow:

Workflow
=========
The GSA workflow follows the standard CVXlab modeling workflow, while introducing additional settings and operations at selected steps. 
The table below summarizes how each standard workflow step is adapted when performing global sensitivity analysis.

.. list-table:: CVXlab GSA modeling workflow
   :header-rows: 1
   :widths: 32 30 38

   * - Workflow step
     - Standard workflow
     - GSA-specific extension
   * - :ref:`Conceptual model definition <conceptual-model-definition-gsa>`
     - Mathematical model conceptualization.
     - Identify uncertain exogenous parameters and model outputs of interest.
   * - :ref:`Generation of model directory <generation-of-model-directory-gsa>`
     - Generate the model directory and setup template file(s).
     - Enable GSA functionalities through ``uncertainty=True``.
   * - :ref:`Fill model setup file(s) <fill-model-setup-files-gsa>`
     - Define sets, data tables, variables, and numerical problems.
     - Flag data tables containing uncertain parameters and model outputs to be
       used in the sensitivity analysis.
   * - :ref:`Generate Model class instance <generate-model-class-instance-gsa>`
     - Generate the CVXlab Model instance.
     - Enable GSA functionalities through ``uncertainty=True``.
   * - :ref:`Fill sets data <fill-sets-data-gsa>`
     - Provide model coordinates.
     - No additional GSA-specific step.
   * - :ref:`Initialization of data structures <data-structures-init-gsa>`
     - Generate the SQLite database and exogenous input data file(s).
     - Additional uncertainty-related fields are generated for
       uncertainty-enabled data tables.
   * - :ref:`Fill exogenous model data <fill-exogenous-data-gsa>`
     - Provide exogenous model data.
     - No additional GSA-specific step; uncertainty-enabled tables are generated
       with additional uncertainty-related fields.
   * - :ref:`Uncertainty settings <uncertainty-settings>`
     - Not included in the standard workflow.
     - Configure the sampling design and the global sensitivity analysis settings.
   * - :ref:`Initialization run of numerical problem(s) <numerical-problem-init-run-gsa>`
     - Initialize and solve the numerical problem(s) through the standard
       initialization of numerical problems and model-run steps.
     - The initialization and execution steps are handled together by
       ``run_uncertainty()``. The method evaluates all sampled input
       configurations and collects the selected model outputs for subsequent GSA.

.. _conceptual-model-definition-gsa:

Conceptual model definition
---------------------------

The conceptual model definition should follow the standard procedure described in
:ref:`Conceptual model definition <conceptual-model-definition>`.

When planning a GSA, the user should identify which exogenous model
parameters are to be treated as uncertain and select the model output variables
of interest (uncertainty measures) for the sensitivity analysis.

.. _generation-of-model-directory-gsa:

Generation of model directory
-----------------------------

The model directory should be generated following the standard procedure described in
:ref:`Generation of model directory <generation-of-model-directory>`.

Adittionally, for GSA, uncertainty functionalities must be enabled when generating the model
directory by setting ``uncertainty=True``.

API: :py:func:`cvxlab.create_model_dir`

.. rubric:: Typical usage

.. code-block:: python

   cvxlab.create_model_dir(
       ...,
       uncertainty=True,
   )

This generates the model setup templates including the additional settings
required to define uncertainty-enabled data tables and model outputs of interest.

.. rubric:: Parameters description

.. list-table::
   :header-rows: 1
   :align: center

   * - Parameter
     - Description
     - Default
   * - ``uncertainty``
     - If ``True`` enables the generation of the additional model setup fields required by
       the GSA workflow. It must be set to ``True`` when preparing a model for GSA.
     - ``False``

For the description of all other parameters, refer to
:ref:`Generation of model directory <generation-of-model-directory>`.

.. _fill-model-setup-files-gsa:

Fill model setup file(s)
------------------------

The model setup files should be filled following the standard procedure described in
:ref:`Fill model setup file(s) <fill-model-setup-files>`.

The definition of model sets remains unchanged with respect to the standard CVXlab
workflow. For GSA, additional settings are instead required in the
``Data Tables and Variables`` section of the model structure.

Specifically, ``uncertainty_enabled`` is introduced at data-table level and
``uncertainty_measure`` at variable level, as shown below.

.. rubric:: Notation

Names written in ``<...>`` are placeholders to be replaced by user-defined
keys or values. Names written literally, such as ``description`` or
``split_problem``, are field keys and should be kept unchanged.

.. tabs::
  .. group-tab:: YAML

    File: ``structure_variables.yml``

    .. code-block:: yaml

        <data_table_key_1>:
            description: <str>                 # optional
            type: <str>
            coordinates: [<set_key_1>, ...]
            uncertainty_enabled: <bool>        # optional

            variables_info:
                <variable_key_1>:
                    type: <str>
                    uncertainty_measure: <bool>  # optional
                    ...

                <variable_key_2>:
                    ...

        <data_table_key_2>:
            ...


  .. group-tab:: XLSX

    File: ``model_settings.xlsx`` | tab ``structure_variables``

    .. list-table::
      :header-rows: 1
      :align: center

      * - data_table_key
        - description
        - type
        - coordinates
        - uncertainty_enabled
        - variable_key
        - uncertainty_measure
      * - <data_table_key_1>
        - <str>
        - <str>
        - <set_key_1>, ...
        - <bool>
        - <variable_key_1>
        - <bool>
      * - ...
        - ...
        - ...
        - ...
        - ...
        - ...
        - ...

.. rubric:: Fields description

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field name
     - Description

   * - ``uncertainty_enabled``
     - Optional boolean flag defined at data-table level. If ``True``, the table
       is enabled to contain uncertain parameters and the corresponding
       uncertainty-related fields are generated in the input data structure.
       Defaults to ``False``.

   * - ``uncertainty_measure``
     - Optional boolean flag defined at variable level. If ``True``, the variable
       is selected as a model output for GSA. Only scalar variables, with
       dimension ``(1, 1)``, can be selected as uncertainty measures.
       Defaults to ``False``.

For the description of all other fields, refer to
:ref:`Fill model setup file(s) <fill-model-setup-files>`.

.. _generate-model-class-instance-gsa:

Generate Model class instance
-----------------------------

The ``Model`` class instance should be generated following the standard procedure
described in :ref:`Generate Model class instance <generate-model-class-instance>`.

For GSA, uncertainty functionalities must also be enabled when creating the model
instance by setting ``uncertainty=True``.

API: :py:meth:`cvxlab.Model.__init__`

.. rubric:: Typical usage

.. code-block:: python

   model = cvxlab.Model(
       ...,
       uncertainty=True,
   )

.. rubric:: Parameters description

.. list-table::
   :header-rows: 1
   :align: center

   * - Parameter
     - Description
     - Default
   * - ``uncertainty``
     - If ``True`` enables the generation of the additional model setup fields required by
       the GSA workflow. It must be set to ``True`` when preparing a model for GSA.
     - ``False``

For the description of all other parameters, refer to
:ref:`Generate Model class instance <generate-model-class-instance>`.

.. _fill-sets-data-gsa:

Fill sets data
--------------

Sets data should be provided following the standard procedure described in
:ref:`Fill sets data <fill-sets-data>`.

No additional GSA-specific information is required at this step.

.. _data-structures-init-gsa:

Initialization of data structures
---------------------------------

The data structures should be initialized following the standard procedure described in
:ref:`Initialization of data structures <data-structures-init>`.

No additional GSA-specific action is required at this step. However, for data
tables previously marked with ``uncertainty_enabled=True``, the generated SQLite
database and exogenous input data files include additional uncertainty-related
fields used to define uncertain parameters and their bounds, as described in
:ref:`Fill exogenous model data <fill-exogenous-data-gsa>`.

API: :py:meth:`~cvxlab.Model.initialize_model_environment`

.. _fill-exogenous-data-gsa:

Fill exogenous model data
-------------------------

Exogenous model data should be provided following the standard procedure described in
:ref:`Fill exogenous model data <fill-exogenous-data>`.

For GSA, data tables previously marked with ``uncertainty_enabled=True`` include
additional fields that allow uncertainty to be defined at parameter level.
Enabling uncertainty for a data table does not imply that all parameters contained
in that table must be uncertain. Each parameter can be independently defined as
deterministic or uncertain.

.. rubric:: Reading the generated input tables

As in the standard CVXlab workflow, each row of an exogenous input data table
represents one parameter value associated with a specific combination of model
coordinates.

For uncertainty-enabled data tables, additional columns are generated to identify
which individual parameters are uncertain, define their uncertainty ranges and,
when required, assign them to uncertainty groups.

.. rubric:: Generic structure of an exogenous input data table

.. list-table::
   :header-rows: 1
   :align: center

   * - id
     - <coordinate_1>
     - ...
     - <coordinate_n>
     - values
     - is_uncertain
     - lower_bound
     - upper_bound
     - uncertainty_group_name
   * - <id>
     - <set_item>
     - ...
     - <set_item>
     - <value>
     - <bool>
     - <value>
     - <value>
     - <str>
   * - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...
     - ...

.. rubric:: Fields description

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field name
     - Description

   * - ``is_uncertain``
     - Boolean flag identifying whether the parameter represented by the row is
       treated as uncertain. If ``True``, the parameter is sampled within the
       specified uncertainty bounds. If ``False``, the parameter remains
       deterministic and the value specified in ``values`` is used.

   * - ``lower_bound``
     - Lower bound of the sampling range associated with an uncertain parameter.
       It must be specified when ``is_uncertain=True``.

   * - ``upper_bound``
     - Upper bound of the sampling range associated with an uncertain parameter.
       It must be specified when ``is_uncertain=True`` and must be greater than
       ``lower_bound``.

   * - ``uncertainty_group_name``
     - Optional name used to associate multiple uncertain parameters with the
       same uncertainty group. When grouped sampling is enabled, every uncertain
       parameter must be assigned to a group.

For the description of other coordinate fields, refer to
:ref:`Fill exogenous model data <fill-exogenous-data>`.

.. _uncertainty-settings:

Uncertainty settings
---------------------
Before running the uncertainty model evaluations, the sampling and global sensitivity analysis
configuration must be defined through ``uncertainty_settings()``. 

.. rubric:: Typical usage

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

.. rubric:: Parameters description

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

.. _numerical-problem-init-run-gsa:

Initialization and run of numerical problem(s)
-------------------------------------------------

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

.. rubric:: Typical usage

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

.. rubric:: Parameters description

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