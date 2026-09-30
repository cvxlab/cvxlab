Overview
========

CVXlab provides functionalities to perform *Global Sensitivity Analysis (GSA)*, 
extending the standard modeling workflow described in
the :ref:`user_guide`.

The GSA workflow combines uncertainty sampling, repeated model evaluations,
and sensitivity analysis to quantify how variations in uncertain model inputs
influence selected model outputs.

CVXLab relies on  `SALib <https://salib.readthedocs.io/>`_ for sampling and
sensitivity-analysis methods, while managing their integration with the  model. 

CVXlab allows users to:

- flag data tables that contain uncertain parameters;
- specify lower and upper bounds for the uncertain parameters within those tables;
- construct the corresponding sampling problem;
- generate input samples using the selected sampling method;
- evaluate the numerical model for each sampled configuration;
- collect selected model outputs;
- compute global sensitivity indices from the resulting model responses.

The standard CVXlab modeling workflow is preserved when performing GSA.
However, selected workflow steps require additional settings. The following
section describes the :ref:`Global Sensitivity Analysis workflow <gsa_workflow>`,
following the same sequence of steps adopted in the standard CVXlab workflow
and highlighting the additional operations required for GSA.