Global Sensitivity Analysis
====================================


CVXlab provides functionalities to perform *Global Sensitivity Analysis (GSA)*, 
extending the standard modeling workflow described in
the :ref:`user_guide`.

The GSA workflow combines uncertainty sampling, repeated model evaluations,
and sensitivity analysis to quantify how variations in uncertain model inputs
influence selected model outputs.

CVXLab relies on  `SALib <https://salib.readthedocs.io/>`_ for sampling and
sensitivity-analysis methods, while managing their integration with the  model. 
The GSA workflow follows the standard CVXlab modeling workflow while introducing
additional settings and operations at selected steps. The table below summarizes
the GSA-specific extensions required throughout the workflow.

.. list-table:: CVXlab GSA modeling workflow
   :header-rows: 1
   :widths: 38 62

   * - Workflow step
     - GSA-specific extension

   * - :ref:`Conceptual model definition <conceptual-model-definition-gsa>`
     - Identify the exogenous model parameters to be treated as uncertain and
       the model outputs of interest for the sensitivity analysis.

   * - :ref:`Generation of model directory <generation-of-model-directory-gsa>`
     - Enable uncertainty functionalities through ``uncertainty=True``.

   * - :ref:`Fill model setup file(s) <fill-model-setup-files-gsa>`
     - Enable uncertainty for the relevant data tables through
       ``uncertainty_enabled=True`` and identify the model outputs of interest for
       sensitivity analysis through ``uncertainty_measure=True``.

   * - :ref:`Generate Model class instance <generate-model-class-instance-gsa>`
     - Enable uncertainty functionalities through ``uncertainty=True``.

   * - :ref:`Fill sets data <fill-sets-data-gsa>`
     - No additional GSA-specific task required.

   * - :ref:`Initialization of data structures <data-structures-init-gsa>`
     - Additional uncertainty-related fields are generated for
       uncertainty-enabled data tables.

   * - :ref:`Fill exogenous model data <fill-exogenous-data-gsa>`
     - Define which parameters are uncertain, specify their sampling bounds and,
       optionally, assign them to uncertainty groups.

   * - :ref:`Uncertainty settings <uncertainty-settings>`
     - Configure the sampling design, optional uncertainty grouping, GSA method,
       analysis targets, and result-export settings.

   * - :ref:`Initialization and run of numerical problem(s) <numerical-problem-init-run-gsa>`
     - Execute the uncertainty workflow through ``run_uncertainty()``, including
       sampling, model evaluations, collection of uncertainty measures,
       and computation of sensitivity indices when a GSA method is configured.

.. toctree::
   :maxdepth: 1
   :caption: Modeling workflow steps


   01_conceptual_model_definition
   02_generation_model_directory
   03_fill_model_setup_files
   04_generate_model_instance
   05_fill_sets_data
   06_initialize_data_structures
   07_fill_exogenous_data
   08_uncertainty_settings
   09_run_uncertainty