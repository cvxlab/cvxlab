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
    - :math:`|a_i| \times |p|`
    - —
    - Reference supply table.
  * - use_0
    - U_0
    - :math:`|p| \times |a_i|`
    - —
    - Reference domestic use table.
  * - use_0
    - Y_0
    - :math:`|p| \times |a_f|`
    - —
    - Reference domestic final demand.
  * - imports_0
    - M_u_0
    - :math:`|p| \times |a_i|`
    - —
    - Reference intermediate imports.
  * - imports_0
    - M_y_0
    - :math:`|p| \times |a_f|`
    - —
    - Reference final imports.
  * - extensions_0
    - F_u_0
    - :math:`|e_v| \times |a_i|`
    - —
    - Reference value added by technology.
  * - extensions_0
    - F_y_0
    - :math:`|e_v| \times |a_f|`
    - —
    - Reference value added associated with final demand.
  * - extensions_0
    - R_u_0
    - :math:`|e_r| \times |a_i|`
    - —
    - Reference environmental flows by technology.
  * - extensions_0
    - R_y_0
    - :math:`|e_r| \times |a_f|`
    - —
    - Reference environmental flows associated with final demand.
  * - total_demand_0
    - Q_0
    - :math:`|p| \times 1`
    - —
    - Reference domestic product output.
  * - total_activity_0
    - X_0
    - :math:`|a_i| \times 1`
    - —
    - Reference technology activity.
  * - delta_make
    - delta_d
    - :math:`|a_i| \times |p|`
    - :math:`s\;[3]`
    - Additive changes to technology market shares.
  * - delta_use
    - delta_u
    - :math:`|p| \times |a_i|`
    - :math:`s\;[3]`
    - Additive changes to domestic use coefficients.
  * - delta_use
    - delta_Y
    - :math:`|p| \times |a_f|`
    - :math:`s\;[3]`
    - Additive changes to domestic final demand.
  * - delta_imports
    - delta_m_u
    - :math:`|p| \times |a_i|`
    - :math:`s\;[3]`
    - Additive changes to intermediate import coefficients.
  * - delta_imports
    - delta_M_y
    - :math:`|p| \times |a_f|`
    - :math:`s\;[3]`
    - Additive changes to final imports.
  * - sum_vector_y
    - i_y
    - :math:`|a_f| \times 1`
    - —
    - Final-demand sum vector (ones).
  * - market_shares
    - d
    - :math:`|a_i| \times |p|`
    - :math:`s\;[3]`
    - Technology market shares.
  * - use_coefficients
    - u
    - :math:`|p| \times |a_i|`
    - :math:`s\;[3]`
    - Domestic use coefficients.
  * - imports_coefficients
    - m_u
    - :math:`|p| \times |a_i|`
    - :math:`s\;[3]`
    - Intermediate import coefficients.
  * - extensions_coefficients
    - f
    - :math:`|e_v| \times |a_i|`
    - :math:`s\;[3]`
    - Value added coefficients.
  * - extensions_coefficients
    - r
    - :math:`|e_r| \times |a_i|`
    - :math:`s\;[3]`
    - Environmental flow coefficients.
  * - total_demand
    - Q
    - :math:`|p| \times 1`
    - :math:`s\;[3]`
    - Domestic product output.
  * - total_activity
    - X
    - :math:`|a_i| \times 1`
    - :math:`s\;[3]`
    - Technology activity.
  * - make
    - V
    - :math:`|a_i| \times |p|`
    - :math:`s\;[3]`
    - Supply table.
  * - use
    - U
    - :math:`|p| \times |a_i|`
    - :math:`s\;[3]`
    - Domestic use table.
  * - use
    - Y
    - :math:`|p| \times |a_f|`
    - :math:`s\;[3]`
    - Domestic final demand.
  * - imports
    - M_u
    - :math:`|p| \times |a_i|`
    - :math:`s\;[3]`
    - Intermediate imports.
  * - imports
    - M_y
    - :math:`|p| \times |a_f|`
    - :math:`s\;[3]`
    - Final imports.
  * - extensions
    - F_u
    - :math:`|e_v| \times |a_i|`
    - :math:`s\;[3]`
    - Value added by technology.
  * - extensions
    - F_y
    - :math:`|e_v| \times |a_f|`
    - :math:`s\;[3]`
    - Value added associated with final demand.
  * - extensions
    - R_u
    - :math:`|e_r| \times |a_i|`
    - :math:`s\;[3]`
    - Environmental flows by technology.
  * - extensions
    - R_y
    - :math:`|e_r| \times |a_f|`
    - :math:`s\;[3]`
    - Environmental flows associated with final demand.
