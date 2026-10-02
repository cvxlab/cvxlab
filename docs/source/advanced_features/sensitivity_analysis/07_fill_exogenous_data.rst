.. _fill-exogenous-data-gsa:

Fill exogenous model data
===========================

Exogenous model data should be provided following the standard procedure described in
:ref:`Fill exogenous model data <fill-exogenous-data>`.

For GSA, data tables previously marked with ``uncertainty_enabled=True`` include
additional fields that allow uncertainty to be defined at parameter level.
Enabling uncertainty for a data table does not imply that all parameters contained
in that table must be uncertain. Each parameter can be independently defined as
deterministic or uncertain.

Reading the generated input tables
-----------------------------------

As in the standard CVXlab workflow, each row of an exogenous input data table
represents one parameter value associated with a specific combination of model
coordinates.

For uncertainty-enabled data tables, additional columns are generated to identify
which individual parameters are uncertain, define their uncertainty ranges and,
when required, assign them to uncertainty groups.

Generic structure of an exogenous input data table
---------------------------------------------------

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
