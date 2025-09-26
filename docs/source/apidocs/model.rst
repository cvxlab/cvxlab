Model
=====

The cvxlab.Model class includes all the main package APIs necessary to
generate, handle and solve the numerical model.

.. autoclass:: cvxlab.Model
   :no-members:
   :no-undoc-members:


Model initialization and setup
------------------------------

.. automethod:: cvxlab.Model.__init__
.. automethod:: cvxlab.Model.load_model_coordinates
.. automethod:: cvxlab.Model.initialize_problems
.. automethod:: cvxlab.Model.run_model
.. automethod:: cvxlab.Model.update_database_and_problem


Model data management methods
-----------------------------

.. automethod:: cvxlab.Model.initialize_blank_data_structure
.. automethod:: cvxlab.Model.generate_input_data_files
.. automethod:: cvxlab.Model.load_exogenous_data_to_sqlite_database
.. automethod:: cvxlab.Model.load_results_to_database


Attributes and properties
-------------------------

.. autoattribute:: cvxlab.Model.sets
.. autoattribute:: cvxlab.Model.data_tables
.. autoattribute:: cvxlab.Model.variables
.. autoattribute:: cvxlab.Model.is_problem_solved


Helper methods
--------------

.. automethod:: cvxlab.Model.set
.. automethod:: cvxlab.Model.variable
.. automethod:: cvxlab.Model.reinitialize_sqlite_database
.. automethod:: cvxlab.Model.check_model_results
.. automethod:: cvxlab.Model.check_model_dir




