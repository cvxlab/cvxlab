.. list-table:: ``model_settings.xlsx`` | ``problem``
   :header-rows: 1
   :class: longtable

   * - problem_key
     - objective
     - expressions
     - description
   * - data_processing
     - 
     - u == U_0 @ minv(diag(X_0)) + delta_u
     - domestic use coefficients
   * - data_processing
     - 
     - d == V_0 @ minv(diag(Q_0)) + delta_d
     - technology market shares
   * - data_processing
     - 
     - m_u == M_u_0 @ minv(diag(X_0)) + delta_m_u
     - intermediate import coefficients
   * - data_processing
     - 
     - f == F_u_0 @ minv(diag(X_0))
     - value added coefficients
   * - data_processing
     - 
     - r == R_u_0 @ minv(diag(X_0))
     - environmental flow coefficients
   * - impact_analysis
     - 
     - Q == u @ X + Y @ i_y
     - products total demand-supply balance
   * - impact_analysis
     - 
     - X == d @ Q
     - industry technology assumption
   * - impact_analysis
     - 
     - Y == Y_0 + delta_Y
     - scenario domestic final demand
   * - impact_analysis
     - 
     - U == u @ diag(X)
     - domestic intermediate use table
   * - impact_analysis
     - 
     - V == d @ diag(Q)
     - make table
   * - impact_analysis
     - 
     - M_u == m_u @ diag(X)
     - intermediate imports table
   * - impact_analysis
     - 
     - M_y == M_y_0 + delta_M_y
     - scenario final imports
   * - impact_analysis
     - 
     - F_u == f @ diag(X)
     - value added by technology
   * - impact_analysis
     - 
     - F_y == F_y_0
     - value added associated with final demand
   * - impact_analysis
     - 
     - R_u == r @ diag(X)
     - environmental flows by technology
   * - impact_analysis
     - 
     - R_y == R_y_0
     - environmental flows associated with final demand
