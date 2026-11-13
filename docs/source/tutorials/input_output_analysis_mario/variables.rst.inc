.. list-table:: Variables of the tutorial model
  :header-rows: 1
  :widths: 23 12 20 15 30

  * - Source Data Table
    - Variable
    - Shape [rows x columns]
    - Inter-problem sets
    - Description
  * - make_0
    - V_0
    - :math:`163 \times 189`
    - —
    - Reference supply table.
  * - use_0
    - U_0
    - :math:`189 \times 163`
    - —
    - Reference domestic use table.
  * - use_0
    - Y_0
    - :math:`189 \times 9`
    - —
    - Reference domestic final demand.
  * - imports_0
    - M_u_0
    - :math:`189 \times 163`
    - —
    - Reference intermediate imports.
  * - imports_0
    - M_y_0
    - :math:`189 \times 9`
    - —
    - Reference final imports.
  * - extensions_0
    - F_u_0
    - :math:`12 \times 163`
    - —
    - Reference value added by technology.
  * - extensions_0
    - F_y_0
    - :math:`12 \times 9`
    - —
    - Reference value added associated with final demand.
  * - extensions_0
    - R_u_0
    - :math:`1 \times 163`
    - —
    - Reference greenhouse-gas emissions by technology.
  * - extensions_0
    - R_y_0
    - :math:`1 \times 9`
    - —
    - Reference greenhouse-gas emissions associated with final demand.
  * - total_demand_0
    - Q_0
    - :math:`189 \times 1`
    - —
    - Reference domestic product output.
  * - total_activity_0
    - X_0
    - :math:`163 \times 1`
    - —
    - Reference technology activity.
  * - delta_make
    - delta_d
    - :math:`163 \times 189`
    - :math:`s\;[3]`
    - Additive changes to technology market shares.
  * - delta_use
    - delta_u
    - :math:`189 \times 163`
    - :math:`s\;[3]`
    - Additive changes to domestic use coefficients.
  * - delta_use
    - delta_Y
    - :math:`189 \times 9`
    - :math:`s\;[3]`
    - Additive changes to domestic final demand.
  * - delta_imports
    - delta_m_u
    - :math:`189 \times 163`
    - :math:`s\;[3]`
    - Additive changes to intermediate import coefficients.
  * - delta_imports
    - delta_M_y
    - :math:`189 \times 9`
    - :math:`s\;[3]`
    - Additive changes to final imports.
  * - sum_vector_y
    - i_y
    - :math:`9 \times 1`
    - —
    - Final-demand sum vector (ones).
  * - market_shares
    - d
    - :math:`163 \times 189`
    - :math:`s\;[3]`
    - Technology market shares.
  * - use_coefficients
    - u
    - :math:`189 \times 163`
    - :math:`s\;[3]`
    - Domestic use coefficients.
  * - imports_coefficients
    - m_u
    - :math:`189 \times 163`
    - :math:`s\;[3]`
    - Intermediate import coefficients.
  * - extensions_coefficients
    - f
    - :math:`12 \times 163`
    - :math:`s\;[3]`
    - Value added coefficients.
  * - extensions_coefficients
    - r
    - :math:`1 \times 163`
    - :math:`s\;[3]`
    - Greenhouse-gas emission coefficients.
  * - total_demand
    - Q
    - :math:`189 \times 1`
    - :math:`s\;[3]`
    - Domestic product output.
  * - total_activity
    - X
    - :math:`163 \times 1`
    - :math:`s\;[3]`
    - Technology activity.
  * - make
    - V
    - :math:`163 \times 189`
    - :math:`s\;[3]`
    - Supply table.
  * - use
    - U
    - :math:`189 \times 163`
    - :math:`s\;[3]`
    - Domestic use table.
  * - use
    - Y
    - :math:`189 \times 9`
    - :math:`s\;[3]`
    - Domestic final demand.
  * - imports
    - M_u
    - :math:`189 \times 163`
    - :math:`s\;[3]`
    - Intermediate imports.
  * - imports
    - M_y
    - :math:`189 \times 9`
    - :math:`s\;[3]`
    - Final imports.
  * - extensions
    - F_u
    - :math:`12 \times 163`
    - :math:`s\;[3]`
    - Value added by technology.
  * - extensions
    - F_y
    - :math:`12 \times 9`
    - :math:`s\;[3]`
    - Value added associated with final demand.
  * - extensions
    - R_u
    - :math:`1 \times 163`
    - :math:`s\;[3]`
    - Greenhouse-gas emissions by technology.
  * - extensions
    - R_y
    - :math:`1 \times 9`
    - :math:`s\;[3]`
    - Greenhouse-gas emissions associated with final demand.
