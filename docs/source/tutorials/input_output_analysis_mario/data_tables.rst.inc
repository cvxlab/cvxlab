.. list-table:: Data Tables of the tutorial model
  :header-rows: 1
  :widths: 23 20 23 34

  * - Name
    - Type
    - Domain [row count]
    - Description
  * - make_0
    - Exogenous
    - | :math:`p \times a`
      | :math:`[189 \times 172]`
    - Reference supply flows.
  * - use_0
    - Exogenous
    - | :math:`p \times a`
      | :math:`[189 \times 172]`
    - Reference domestic intermediate use and final demand.
  * - imports_0
    - Exogenous
    - | :math:`p \times a`
      | :math:`[189 \times 172]`
    - Reference intermediate and final imports.
  * - extensions_0
    - Exogenous
    - | :math:`e \times a`
      | :math:`[13 \times 172]`
    - Reference value added and environmental flows for intermediate and final accounts.
  * - total_demand_0
    - Exogenous
    - | :math:`p`
      | :math:`[189]`
    - Reference domestic product output.
  * - total_activity_0
    - Exogenous
    - | :math:`a`
      | :math:`[172]`
    - Reference technology activity.
  * - delta_make
    - Exogenous
    - | :math:`p \times a \times s`
      | :math:`[189 \times 172 \times 3]`
    - Scenario changes to technology market shares.
  * - delta_use
    - Exogenous
    - | :math:`p \times a \times s`
      | :math:`[189 \times 172 \times 3]`
    - Scenario changes to domestic use coefficients and final demand.
  * - delta_imports
    - Exogenous
    - | :math:`p \times a \times s`
      | :math:`[189 \times 172 \times 3]`
    - Scenario changes to import coefficients and final imports.
  * - sum_vector_y
    - Constant
    - | :math:`a`
      | :math:`[172]`
    - Column vector of ones for final-demand aggregation.
  * - market_shares
    - Endogenous (DP); exogenous (IA)
    - | :math:`p \times a \times s`
      | :math:`[189 \times 172 \times 3]`
    - Scenario technology market shares.
  * - use_coefficients
    - Endogenous (DP); exogenous (IA)
    - | :math:`p \times a \times s`
      | :math:`[189 \times 172 \times 3]`
    - Scenario domestic use coefficients.
  * - imports_coefficients
    - Endogenous (DP); exogenous (IA)
    - | :math:`p \times a \times s`
      | :math:`[189 \times 172 \times 3]`
    - Scenario intermediate import coefficients.
  * - extensions_coefficients
    - Endogenous (DP); exogenous (IA)
    - | :math:`e \times a \times s`
      | :math:`[13 \times 172 \times 3]`
    - Scenario value added and environmental flow coefficients.
  * - total_demand
    - Endogenous
    - | :math:`p \times s`
      | :math:`[189 \times 3]`
    - Scenario domestic product output.
  * - total_activity
    - Endogenous
    - | :math:`a \times s`
      | :math:`[172 \times 3]`
    - Scenario technology activity.
  * - make
    - Endogenous
    - | :math:`p \times a \times s`
      | :math:`[189 \times 172 \times 3]`
    - Scenario supply flows.
  * - use
    - Endogenous
    - | :math:`p \times a \times s`
      | :math:`[189 \times 172 \times 3]`
    - Scenario domestic intermediate use and final demand.
  * - imports
    - Endogenous
    - | :math:`p \times a \times s`
      | :math:`[189 \times 172 \times 3]`
    - Scenario intermediate and final imports.
  * - extensions
    - Endogenous
    - | :math:`e \times a \times s`
      | :math:`[13 \times 172 \times 3]`
    - Scenario value added and environmental flows.
