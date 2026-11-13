.. list-table:: ``model_settings.xlsx`` | ``structure_sets``
   :header-rows: 1
   :class: longtable

   * - set_key
     - description
     - split_problem
     - filters
     - aggregations
   * - products
     - products included in the SUT domain.
     - 
     - type: [power]
     - [medium, high]
   * - accounts
     - include technologies and demand categories.
     - 
     - category: [intermediate, final], type: [power]
     - medium, high
   * - extensions
     - includes factors of production and environmental flows
     - 
     - category: [value_added, environmental_flows]
     - 
   * - scenarios
     - definition of simulated scenarios.
     - True
     - 
     - 
