.. _fill-model-setup-files:

Fill model setup file(s)
========================

This page guides you through the structure and meaning of the CVXlab model
settings.


Introduction
------------

The model setup files contain the essential settings required to translate the
conceptual model (see :ref:`conceptual-model-definition`) from a mathematical
formulation into an instance of the *CVXlab Model* class.

The setup files define the structure of the fundamental CVXlab objects,
including *sets*, *data tables (with related variables)*, and *mathematical
problems (with related expressions)*. These structures are defined in the
:py:attr:`default module <cvxlab.defaults.Defaults.DefaultStructures>` and
automatically reflected in the generated template settings files.

Once the model directory has been generated
(see :ref:`generation-of-model-directory`), the setup information is provided
in *YAML* format (as three separate files) or *Excel* format (as one workbook
with three tabs). The setup files are:

- **Structure of sets**: defined in ``structure_sets.yml`` or the
  ``structure_sets`` Excel tab.
- **Structure of data tables and variables**: defined in
  ``structure_variables.yml`` or the ``structure_variables`` Excel tab.
- **Mathematical problem**: defined in ``problem.yml`` or the ``problem`` Excel tab.

Optionally, template files for user-defined symbolic operators and constants can
be included in the model directory if requested during the directory generation
step:

- :ref:`user_defined_operators.py <api_user_defined_operators>`: template for
  custom symbolic operators.
- :ref:`user_defined_constants.py <api_user_defined_constants>`: template for
  custom constant types.


.. _sets_definition:

Sets
----

*Sets* define the dimensions of the model according to the following structure
(shown here in YAML format; the same logic applies to the Excel file):


.. rubric:: Notation

Names written in ``<...>`` are placeholders to be replaced by user-defined
keys or values. Names written literally, such as ``description`` or
``split_problem``, are field keys and should be kept unchanged.


.. tabs::

  .. group-tab:: YAML

    File: ``structure_sets.yml``

    .. code-block:: yaml

        <set_key_1>:                        # user-defined set key
            description: <str>              # optional
            split_problem: <bool>           # optional
            copy_from: <str>                # optional
            filters: <dict>                 # optional
                <filter_key_1>: [<str>, <str>, ...]
                <filter_key_2>: [<str>, <str>, ...]
                ...
            aggregations: [<int | str>, ...] # optional

        <set_key_2>:
            ...
        ...

  .. group-tab:: XLSX

    File: ``model_settings.xlsx`` | tab ``structure_sets``
    
    .. list-table::
      :header-rows: 1
      :align: center

      * - set_key
        - description
        - split_problem
        - copy_from
        - filters
        - aggregations
      * - <set_key_1>
        - <str>
        - <bool>
        - <str>
        - <filter_key_1>: [<str>, <str>, ...], <filter_key_2>: [<str>, <str>, ...], ...
        - <int | str>, ...
      * - ...
        - ...
        - ...
        - ...
        - ...
        - ...


.. rubric:: Fields description

``<set_key_#>``: (required) user-defined key of the set. This placeholder must
be replaced with the actual set key used in the SQLite data table. Set keys
are case-insensitive. This is the only required field.

- ``description``: (optional) metadata provided by the modeler.
- ``split_problem``: (optional) if *true*, set items define independent numerical
  sub-problems. Such a set is classified as an inter-problem set.
- ``copy_from``: (optional) key of another set to copy data from. If defined,
  the set data need not be provided again in the sets workbook generated in a
  following step.
- ``filters``: (optional) dictionary used to identify subsets of data tables for
  generating variables. Each key is a filter key, and the corresponding value is
  a list of values defining the filter categories. For example, the *technology
  type* filter can be used to identify the following subsets of technologies:
  *[renewable, non-renewable]*.
- ``aggregations``: (optional) list of aggregation keys used for reporting and
  visualization. These are not used in numerical problem operations, but are
  useful for identifying how to aggregate results for reporting and visualization.

At this stage, the modeler only defines the structure of the sets, while the
actual set items (that is, the *coordinates*) are defined later in the sets
Excel file generated after an instance of the Model class is created
(see :ref:`fill-sets-data`).


.. _data_tables_variables_definition:

Data Tables and Variables
-------------------------

*Data Tables* represent collections of data that share the same structure, that
is, the same coordinates and variable types. Each data table corresponds to a
table in the SQLite database. One or more *Variables* can be defined from each
data table. These variables represent symbolic objects arranged in different
shapes for use in mathematical expressions.

*Data Tables* and *Variables* are defined according to the structure below
(shown here in YAML format; the same logic applies to the Excel file).


.. rubric:: Notation

Names written in ``<...>`` are placeholders to be replaced by user-defined
keys or values. Names written literally, such as ``description``, ``type``,
``coordinates`` or ``variables_info``, are field keys and should be kept
unchanged.


.. tabs::

  .. group-tab:: YAML

    File: ``structure_variables.yml``

    .. code-block:: yaml

        <table_key_#>:                         # user-defined table key
            description: <str>                 # optional
            type: <str | dict[str, str]>
                <problem_key_#>: <str>, ...    # optional, for hybrid Data Tables only

            domain: <str>             # optional
            coordinates: <str | list[str]>
            variables_info:

                <variable_key_#>:              # user-defined variable key
                    value: <str>               # optional
                    blank_fill: <int|float>    # optional
                    nonneg: <bool>             # optional
                    <set_key_#>:               # optional, user-defined set key
                        dim: <str>
                        filters:
                            <filter_key_#>: [<str>, <str>, ...]
                            ...
                    ...
                ...
        ...

  .. group-tab:: XLSX

    File: ``model_settings.xlsx`` | tab ``structure_variables``

    .. list-table::
        :header-rows: 1
        :align: center

        * - table_key
          - description
          - type
          - domain
          - coordinates
          - variables_info
          - value
          - blank_fill
          - nonneg
          - <set_key_#>
          - ...
        * - <table_key_#>
          - <str>
          - <str> | <problem_key_#>: <str>, ...
          - <str>  # ``integer`` | ``boolean``
          - <str>, <str>, ...
          - <str>
          - <str>
          - <int | float>
          - <bool>
          - dim: <str>, filters: {<filter_key_#>: [<str>, <str>, ...], ...}
          - ...
        * - ...
          - ...
          - ...
          - ...
          - ...
          - ...
          - ...
          - ...
          - ...
          - ...
          - ...


.. rubric:: Field descriptions

``<table_key_#>``: (required) user-defined key of the Data Table. This
placeholder must be replaced with the actual table key used in the SQLite
database. Since SQLite data tables are case-insensitive, table keys are also
case-insensitive.

- ``description``: (optional) information about the data table.
- ``type``: (required) type of the data table. It can be *endogenous*, *exogenous*,
  *constant*, or a dictionary mapping problem keys to types for integrated
  problems (in this case, variables are defined as *hybrid* type).
- ``domain``: (optional) domain of the endogenous variables. Accepted values:
  ``integer`` (integer-valued variables, :math:`\mathbb{Z}`) or ``boolean``
  (binary variables, :math:`\{0,1\}`). If omitted, variables are continuous.
- ``coordinates``: (required) list of Set keys defining the dimensions of the 
  Data Table.
- ``variables_info``: dictionary defining variable keys and their properties.
  Each key is a user-defined variable key, and its value is a dictionary
  containing the following properties:

  - ``<variable_key_#>``: (required) user-defined variable key. This is the only
    required field for each variable, and it is used as the variable key in
    mathematical expressions.
    
    - ``value``: (optional) for *constant*-type variables only, identifies the
      constant value assigned to the variable. A full list of built-in constants
      and instructions for defining custom constants are documented in
      :ref:`api_constants_types`.
    - ``blank_fill``: (optional) for *exogenous* variables only, the value used
      to fill blank cells in SQLite Data Tables when values are missing.
    - ``nonneg``: (optional) for *endogenous* variables only, indicates whether
      the variable is constrained to be non-negative.
    - ``<set_key_#>``: (optional) key of a Set included in the Data Table
      coordinates. The following information is provided for each set to define
      how it shapes the variable and whether and how it is filtered.
      Any set in the Data Table coordinates that is not explicitly included in
      the variable definition is assigned as an intra-problem dimension by
      default, unless it is an inter-problem set.
      
      - ``dim``: (required) dimension assigned to the set. It can be *row* for
        rows, *col* for columns, or *intra* for intra-problem indexing (meaning
        that the variable will be defined once for each combination of items
        from the intra-problem sets). Each set can be assigned to only one
        dimension.
      - ``filters``: (optional) dictionary used to filter Data Tables when
        generating variables. Each key is a filter key (defined in the
        ``filters`` fields of the :ref:`sets_definition` section), and the
        corresponding value is a list of values defining the filter categories
        to include.


.. admonition:: About the ``nonneg`` field

  The ``nonneg`` field indicates whether an endogenous variable is expected to
  be non-negative. If so, the model includes an implicit non-negativity
  constraint. In the case of a *single numerical problem*, setting
  ``nonneg=True`` adds an implicit non-negativity expression to the problem.
  For *integrated numerical problems*:

  - For *hybrid variables*, non-negativity constraints are added to the problem
    in which the variable is defined as endogenous. This also helps ensure that
    the variable is used with the correct sign in that problem, avoiding
    numerical inconsistencies during model solving.
  - For *pure endogenous variables*, non-negativity constraints are added only
    if the variable is used in another problem expression. If it is not used in
    any expression, an error is raised; constraints must be defined explicitly
    in the symbolic problem.


.. admonition:: Using the same set for rows and columns

  A variable may need to be represented as a square table indexed by the same
  set on both dimensions. For example, an economic model may use a
  country-by-country table to record trade connections. A set cannot be
  assigned to more than one dimension, so define two sets with the same
  elements (for example, ``country_from`` and ``country_to``) and assign one
  to the rows and the other to the columns.

  To avoid entering the same set data twice, define ``copy_from`` for one of
  the sets, referring to the other set. The data then need to be provided only
  once in the sets workbook generated in the following step.


Problem and Expressions
-----------------------

Problems are defined in ``problem.yml`` or in the ``problem`` tab of
``model_settings.xlsx``. Each problem key can include an objective and a list of
symbolic expressions, thereby defining either a system of equations or a system
of inequalities, with or without an objective function.


.. rubric:: Notation

Names written in ``<...>`` are placeholders to be replaced by user-defined
keys or values. Names written literally, such as ``objective``, are field keys 
and should be kept unchanged.


.. tabs::

  .. group-tab:: YAML

    File: ``problem.yml``

    .. code-block:: yaml

        <problem_key_#>:              # optional, user-defined problem key
            objective: <str>          # optional
            expressions: [<str>, <str>, ...]
        
        ...

  .. group-tab:: XLSX

    File: ``model_settings.xlsx`` | tab ``problem``

    .. list-table::
        :header-rows: 1
        :align: center

        * - problem_key
          - objective
          - expressions
        * - <problem_key_#>
          - <str>
          - <str>
        * - ...
          - ...
          - ...


.. rubric:: Field descriptions

``<problem_key_#>``: (optional) user-defined problem key. This can be omitted
if there is only one problem.

- ``objective``: (optional) symbolic expression defining the problem objective.
  If omitted, the problem is treated as a system of equations or inequalities
  without an objective function. Each problem can have at most one objective.
- ``expressions``: (required) list of symbolic expressions defining the problem
  constraints.
    
Objectives and expressions are literal strings that refer to variables by their
*variable keys* and can include built-in or user-defined operators (see
:ref:`api_symbolic_operators`).

If the objective includes variables defined over *multiple intra-problem sets*,
it is automatically aggregated over those dimensions. For example, if variable
*cost* is defined over an intra-problem set *t* representing time, CVXlab
automatically sums the objective over the time steps, producing a scalar
CVXPY expression.


Final notes
-----------

- Unused fields in the setup files can be left blank or omitted.
  For example, for *inter-problem sets*, only two fields are needed:
  ``<set_name>_Name``, ``<set_name>_split_problem``.
  
