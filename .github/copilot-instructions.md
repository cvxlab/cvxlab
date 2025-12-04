# CVXlab — AI Coding Agent Guide

This repo provides a Python framework to model and solve convex optimization problems by orchestrating symbolic definitions, an SQLite-backed data layer, and cvxpy-based numerical solvers. Use these notes to get productive fast and avoid common pitfalls.

## Architecture Overview
- **Top-level API**: `cvxlab.__init__` exposes `Model` and helper functions. Typical user entry is `cvxlab.Model(...)`.
- **Core orchestration**: `cvxlab/backend/core.py` coordinates the main components:
  - `Index`: parses symbolic structure (sets, variables, data tables) and scenarios.
  - `SQLManager` + `Database`: manage SQLite I/O, schema, and table operations.
  - `Problem`: builds cvxpy variables, constraints/objective, and numerical problems.
  - `Core` methods implement the workflow: initialize variables → fetch exogenous data → generate numerical problems → solve (independent or integrated) → export endogenous results.
- **Backend pieces** (key files):
  - `backend/index.py`: variables, sets, data tables, and scenarios (including split-by-set logic).
  - `backend/problem.py`: symbolic parsing, cvxpy variable creation (`create_cvxpy_variable`), numerical problem generation, solving, and status fetching.
  - `backend/database.py`: higher-level DB operations on top of `support/sql_manager.py`.
  - `backend/data_table.py`, `backend/variable.py`, `backend/set_table.py`: typed structures for model elements.
- **Support utilities**: `support/util.py`, `support/util_text.py`, `support/util_operators.py`, `support/file_manager.py`, `support/sql_manager.py` provide text/ops helpers, file copying/renaming, SQLite helpers, norms, etc.
- **Logging & errors**: `log_exc/logger.py` exposes timing and convergence logging helpers; `log_exc/exceptions.py` defines domain-specific exceptions.

## Data & Problem Flow
- **Inputs**: Symbolic definitions come from user-controlled setup files (Excel/YAML). Exogenous data is stored in SQLite tables; constants are embedded; endogenous variables are solved.
- **Coordinates**: Variables/data tables carry coordinates derived from sets. Hybrid variables/data tables can vary by sub-problem; scenarios enumerate combinations of inter-problem sets.
- **Numerical build**: `Core.initialize_problems_variables()` creates dataframes and cvxpy variables (global for endogenous tables; sliced for per-variable).
- **Data fetch**: `Core.data_to_cvxpy_exogenous_vars(...)` reads SQLite tables, validates values types, reshapes, and assigns into cvxpy variables.
- **Solving**:
  - Independent: `Core.solve_independent_problems(**solver_settings)` runs each sub-problem once and records status.
  - Integrated (iterative coupling): `Core.solve_integrated_problems(...)` runs block Gauss–Seidel iterations over sub-problems per scenario, checking convergence by norms on table values and exporting endogenous results to the DB at each iteration.
- **Export**: `Core.cvxpy_endogenous_data_to_database(...)` writes solved endogenous values back to SQLite.

## Conventions & Patterns
- **Types**: `Defaults.SymbolicDefinitions.VARIABLE_TYPES` governs `EXOGENOUS`, `ENDOGENOUS`, `CONSTANT`, plus hybrid dicts keyed by problem.
- **Labels**: Column/field names come from `Defaults.Labels` (e.g., `VALUES_FIELD['values'][0]`, `ID_FIELD['id'][0]`, `CVXPY_VAR`, `SCENARIO_COORDINATES`, `PROBLEM_STATUS`). Use these constants rather than hard-coded strings.
- **DB schema**: Each data table is a normalized SQLite table. Reads/writes go through `SQLManager.table_to_dataframe(...)` and `SQLManager.dataframe_to_table(...)` using `filters_dict` built from variable coordinates.
- **Scenarios**: Scenario selection filters inter-problem set combinations; integrated solving iterates per scenario.
- **Hybrid handling**: For dict-typed `coordinates_dataframe` or `cvxpy_var`, index by `problem_key` or `scenario_idx` explicitly.
- **Logging style**: Use `logger.log_timing(...)` around expensive steps and `logger.convergence_monitor(...)` during integrated solving. Errors should raise domain exceptions (`exc.SettingsError`, `exc.MissingDataError`, `exc.OperationalError`).

## Developer Workflows
- **Install (editable)**:
  ```cmd
  pip install -e .[dev]
  ```
  Optional extras: `.[docs]` for docs, `.[solvers]` for `gurobipy`.
- **Run tests**:
  - Test settings: `tests/integration/tests_settings.yml` controls log level, methods, and overrides.
  - Integration tests dynamically generate fixtures and tests from `tests/integration/fixtures/**`.
  ```cmd
  pytest -q
  ```
- **Typical programmatic run**:
  ```python
  from cvxlab import Model
  m = Model(model_dir_name="model_simple", main_dir_path="path/to/models", log_level="info")
  m.initialize_model()              # sets up files/DB
  m.load_symbolic_problem_from_file(force_overwrite=False)  # via Problem
  m.validate_symbolic_expressions()
  m.generate_numerical_problems(force_overwrite=False)
  m.solve_numerical_problems(integrated_problems=False, solver="ECOS", verbose=False)
  ```
- **Solvers**: cvxpy solvers are passed via `**solver_settings` (e.g., `solver="ECOS"`, `verbose=True`). For integrated runs, tune tolerances via `Defaults.NumericalSettings.MODEL_COUPLING_SETTINGS` or method args.

## Where to Look / Extend
- **Symbolic definitions**: `backend/problem.py` (parsing), `templates/` for user-defined operators/constants.
- **Data access**: `support/sql_manager.py` for table reads/writes and norm computations; `backend/database.py` for higher-level DB flows.
- **Index/scenarios**: `backend/index.py` for variable/data table registration and scenario creation.
- **Defaults/tuning**: `defaults.py` for labels, types, convergence settings, file names (e.g., `SQLITE_DATABASE_FILE`).
- **Error handling**: Keep exceptions specific; avoid generic `Exception` in library code.

## Gotchas
- Always use `Defaults.Labels` headers when merging/reshaping DataFrames and building filters.
- `var_list_to_update` in `data_to_cvxpy_exogenous_vars` must be a list; passing non-list raises.
- Hybrid variables and data tables require mapping by problem and scenario; be explicit.
- Integrated solving temporarily rewrites DB and restores from backup; don’t rely on intermediate DB state outside the loop.

## Docs & Examples
- Full docs: `docs/source/**` and https://cvxlab.readthedocs.io.
- API quick-start: `README.md` and `tests/integration/fixtures/model_simple`.

---

Feedback: If any section is unclear or misses a key workflow, tell me what you want to accomplish (e.g., “add a new solver”, “extend variables”, “change DB schema”) and I’ll refine these notes with targeted guidance.
