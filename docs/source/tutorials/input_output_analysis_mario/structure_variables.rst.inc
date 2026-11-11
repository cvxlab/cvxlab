.. list-table:: ``model_settings.xlsx`` | ``structure_variables``
   :header-rows: 1
   :class: longtable

   * - table_key
     - description
     - type
     - coordinates
     - variables_info
     - value
     - blank_fill
     - nonneg
     - products
     - accounts
     - extensions
   * - make_0
     - make table, reference
     - exogenous
     - products, accounts
     - V_0
     - 
     - 
     - 
     - dim: cols
     - dim: rows, filters: {category: intermediate}
     - 
   * - use_0
     - use and final demand table, reference
     - exogenous
     - products, accounts
     - U_0
     - 
     - 
     - 
     - dim: rows
     - dim: cols, filters: {category: intermediate}
     - 
   * - use_0
     - use and final demand table, reference
     - exogenous
     - products, accounts
     - Y_0
     - 
     - 
     - 
     - dim: rows
     - dim: cols, filters: {category: final}
     - 
   * - imports_0
     - imports table, reference
     - exogenous
     - products, accounts
     - M_u_0
     - 
     - 
     - 
     - dim: rows
     - dim: cols, filters: {category: intermediate}
     - 
   * - imports_0
     - imports table, reference
     - exogenous
     - products, accounts
     - M_y_0
     - 
     - 
     - 
     - dim: rows
     - dim: cols, filters: {category: final}
     - 
   * - extensions_0
     - value added and environmental flows table, reference
     - exogenous
     - extensions, accounts
     - F_u_0
     - 
     - 
     - 
     - 
     - dim: cols, filters: {category: intermediate}
     - dim: rows, filters: {category: value_added}
   * - extensions_0
     - value added and environmental flows table, reference
     - exogenous
     - extensions, accounts
     - F_y_0
     - 
     - 
     - 
     - 
     - dim: cols, filters: {category: final}
     - dim: rows, filters: {category: value_added}
   * - extensions_0
     - value added and environmental flows table, reference
     - exogenous
     - extensions, accounts
     - R_u_0
     - 
     - 
     - 
     - 
     - dim: cols, filters: {category: intermediate}
     - dim: rows, filters: {category: environmental_flows}
   * - extensions_0
     - value added and environmental flows table, reference
     - exogenous
     - extensions, accounts
     - R_y_0
     - 
     - 
     - 
     - 
     - dim: cols, filters: {category: final}
     - dim: rows, filters: {category: environmental_flows}
   * - total_demand_0
     - total demand by products vector, reference
     - exogenous
     - products
     - Q_0
     - 
     - 
     - 
     - dim: rows
     - 
     - 
   * - total_activity_0
     - total activity by technology vector, reference
     - exogenous
     - accounts
     - X_0
     - 
     - 
     - 
     - 
     - dim: rows, filters: {category: intermediate}
     - 
   * - delta_make
     - changes in make table
     - exogenous
     - products, accounts, scenarios
     - delta_d
     - 
     - 0
     - 
     - dim: cols
     - dim: rows, filters: {category: intermediate}
     - 
   * - delta_use
     - use coefficients and final demand table changes
     - exogenous
     - products, accounts, scenarios
     - delta_u
     - 
     - 0
     - 
     - dim: rows
     - dim: cols, filters: {category: intermediate}
     - 
   * - delta_use
     - use coefficients and final demand table changes
     - exogenous
     - products, accounts, scenarios
     - delta_Y
     - 
     - 0
     - 
     - dim: rows
     - dim: cols, filters: {category: final}
     - 
   * - delta_imports
     - imports coefficients and final imports demand changes
     - exogenous
     - products, accounts, scenarios
     - delta_m_u
     - 
     - 0
     - 
     - dim: rows
     - dim: cols, filters: {category: intermediate}
     - 
   * - delta_imports
     - imports coefficients and final imports demand changes
     - exogenous
     - products, accounts, scenarios
     - delta_M_y
     - 
     - 0
     - 
     - dim: rows
     - dim: cols, filters: {category: final}
     - 
   * - sum_vector_y
     - constants useful to perform various operations
     - constant
     - accounts
     - i_y
     - sum_vector
     - 
     - 
     - 
     - dim: rows, filters: {category: final}
     - 
   * - market_shares
     - market shares table
     - data_processing: endogenous, impact_analysis: exogenous
     - products, accounts, scenarios
     - d
     - 
     - 0
     - 
     - dim: cols
     - dim: rows, filters: {category: intermediate}
     - 
   * - use_coefficients
     - use and final demand coefficients table
     - data_processing: endogenous, impact_analysis: exogenous
     - products, accounts, scenarios
     - u
     - 
     - 0
     - 
     - dim: rows
     - dim: cols, filters: {category: intermediate}
     - 
   * - imports_coefficients
     - imports coefficients table
     - data_processing: endogenous, impact_analysis: exogenous
     - products, accounts, scenarios
     - m_u
     - 
     - 0
     - 
     - dim: rows
     - dim: cols, filters: {category: intermediate}
     - 
   * - extensions_coefficients
     - value added and environmental coefficients table
     - data_processing: endogenous, impact_analysis: exogenous
     - extensions, accounts, scenarios
     - f
     - 
     - 0
     - 
     - 
     - dim: cols, filters: {category: intermediate}
     - dim: rows, filters: {category: value_added}
   * - extensions_coefficients
     - value added and environmental coefficients table
     - data_processing: endogenous, impact_analysis: exogenous
     - extensions, accounts, scenarios
     - r
     - 
     - 0
     - 
     - 
     - dim: cols, filters: {category: intermediate}
     - dim: rows, filters: {category: environmental_flows}
   * - total_demand
     - total demand by products vector
     - endogenous
     - products, scenarios
     - Q
     - 
     - 
     - 
     - dim: rows
     - 
     - 
   * - total_activity
     - total activity by technology vector
     - endogenous
     - accounts, scenarios
     - X
     - 
     - 
     - 
     - 
     - dim: rows, filters: {category: intermediate}
     - 
   * - make
     - make table
     - endogenous
     - products, accounts, scenarios
     - V
     - 
     - 
     - 
     - dim: cols
     - dim: rows, filters: {category: intermediate}
     - 
   * - use
     - use and final demand table
     - endogenous
     - products, accounts, scenarios
     - U
     - 
     - 
     - 
     - dim: rows
     - dim: cols, filters: {category: intermediate}
     - 
   * - use
     - use and final demand table
     - endogenous
     - products, accounts, scenarios
     - Y
     - 
     - 
     - 
     - dim: rows
     - dim: cols, filters: {category: final}
     - 
   * - imports
     - imports table
     - endogenous
     - products, accounts, scenarios
     - M_u
     - 
     - 
     - 
     - dim: rows
     - dim: cols, filters: {category: intermediate}
     - 
   * - imports
     - imports table
     - endogenous
     - products, accounts, scenarios
     - M_y
     - 
     - 
     - 
     - dim: rows
     - dim: cols, filters: {category: final}
     - 
   * - extensions
     - value added and environmental flows table
     - endogenous
     - extensions, accounts, scenarios
     - F_u
     - 
     - 
     - 
     - 
     - dim: cols, filters: {category: intermediate}
     - dim: rows, filters: {category: value_added}
   * - extensions
     - value added and environmental flows table
     - endogenous
     - extensions, accounts, scenarios
     - F_y
     - 
     - 
     - 
     - 
     - dim: cols, filters: {category: final}
     - dim: rows, filters: {category: value_added}
   * - extensions
     - value added and environmental flows table
     - endogenous
     - extensions, accounts, scenarios
     - R_u
     - 
     - 
     - 
     - 
     - dim: cols, filters: {category: intermediate}
     - dim: rows, filters: {category: environmental_flows}
   * - extensions
     - value added and environmental flows table
     - endogenous
     - extensions, accounts, scenarios
     - R_y
     - 
     - 
     - 
     - 
     - dim: cols, filters: {category: final}
     - dim: rows, filters: {category: environmental_flows}
