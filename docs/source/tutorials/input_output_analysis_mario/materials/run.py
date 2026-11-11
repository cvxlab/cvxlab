"""Reference workflow for the input-output analysis tutorial.

Customize this script, or copy its individual steps into your own script.
The default configuration solves the existing model using the inputs already
stored in database.db. Run from the directory containing the model folder;
CVXlab uses the current working directory and the default model name "model".

To build a new model, set use_existing_data=False in the constructor and enable
the creation/initialization blocks as needed. Use the commented
SystemExit statements to stop for manual file editing before the next phase.

After editing input_data.xlsx, enable the refresh block before solving.
After changing setup files or coordinates, rebuild the matching data structures.
"""

import cvxlab


# 1. Generate a NEW model directory (optional).
# Uncomment the whole block when starting from scratch. Then fill the setup
# files and comment this block again before continuing with the next steps.
# cvxlab.create_model_dir(
#     settings_file_type="xlsx",  # "xlsx" or "yml".
# )
# raise SystemExit("Fill and save the model setup files, then continue.")

# 2. Fill model setup files (manual action).
# YAML: structure_sets.yml, structure_variables.yml, problem.yml.
# Excel: model_settings.xlsx, with the three corresponding worksheets.
# Keep the named problems data_processing and impact_analysis consistent
# with the coefficient types and the solution chain in step 7.

# 3. Create the Model instance.
# True: load the existing coordinates and initialize problems from SQLite.
# False: prepare the model structure for the coordinate/data-filling steps.
model = cvxlab.Model(
    log_level="debug",
    model_settings_from="xlsx",  # "xlsx" or "yml".
    use_existing_data=True,
    multiple_input_files=False,
    input_data_files_type="xlsx",
    detailed_validation=True,
)

# 4. Fill sets.xlsx (manual action for a new model).
# Enter products, accounts, extensions, and scenarios, with their filters
# and aggregation mappings. Save the workbook before step 5.
# raise SystemExit("Fill and save sets.xlsx, then continue.")

# 5. Initialize data structures (only with use_existing_data=False).
# Uncomment when the coordinates are ready. This creates the database and
# input-data templates. Fill and save input_data/input_data.xlsx afterward.
# model.initialize_model_environment()
# raise SystemExit("Fill and save input_data/input_data.xlsx, then continue.")

# 6. Import input files and initialize/refresh numerical problems (optional).
# Enable this for the first import of a new model, or after changing values
# in input_data.xlsx. It updates SQLite from the workbook and replaces the
# in-memory numerical problems. Leave it commented to reuse SQLite inputs.
# model.refresh_database_and_initialize_problem(force_overwrite=True)

# 7. Solve the two problems sequentially for all scenarios.
# Coefficients solved in data_processing become inputs to impact_analysis.
model.run_model(
    solution_mode="sequential",
    sequential_solution_chain=["data_processing", "impact_analysis"],
    solver="GUROBI",  # Or another installed, compatible CVXPY solver.
    # scenarios_idx=[0],  # Optional: select indices from model.scenarios.
)

# 8. Export endogenous results, replacing previously exported values.
model.load_results_to_database(force_overwrite=True)

# 9. Inspect results in model/database.db (manual or custom analysis).
# total_demand / total_activity: product output and technology activity.
# make / use / imports / extensions: reconstructed scenario SUT flows.
# Compare Reference, High_RES, and High_RES_domestic as in the tutorial.
