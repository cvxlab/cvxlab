.. _data-structures-init-gsa:

Initialization of data structures
==================================

The data structures should be initialized following the standard procedure described in
:ref:`Initialization of data structures <data-structures-init>`.

No additional GSA-specific action is required at this step. However, for data
tables previously marked with ``uncertainty_enabled=True``, the generated SQLite
database and exogenous input data files include additional uncertainty-related
fields used to define uncertain parameters and their bounds, as described in
:ref:`Fill exogenous model data <fill-exogenous-data-gsa>`.

API: :py:meth:`~cvxlab.Model.initialize_model_environment`