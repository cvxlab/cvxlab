
.. _fill-model-setup-files-gsa:

Fill model setup file(s)
==========================

The model setup files should be filled following the standard procedure described in
:ref:`Fill model setup file(s) <fill-model-setup-files>`.

The definition of model sets remains unchanged with respect to the standard CVXlab
workflow. For GSA, additional settings are instead required in the
``Data Tables and Variables`` section of the model structure.

Specifically, ``uncertainty_enabled`` is introduced at data-table level and
``uncertainty_measure`` at variable level, as shown below.

Files description
--------------------

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
