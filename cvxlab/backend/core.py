"""Module defining the Core class.

The Core class serves as the central management point for the CVXlab package
and orchestrates the interactions among Index (embedding all information about
data tables and variables), Database (handling SQLite database operations, using
SQLManager), and Problem (defining symbolic and numerical problems).
"""
import os
from typing import Any, Dict, List, Optional
from pathlib import Path

import numpy as np
import pandas as pd
import cvxpy as cp

from cvxlab.backend.data_table import DataTable
from cvxlab.backend.database import Database
from cvxlab.backend.index import Index, Variable
from cvxlab.backend.problem import Problem
from cvxlab.log_exc import exceptions as exc
from cvxlab.log_exc.logger import Logger
from cvxlab.constants import Constants
from cvxlab.support import util
from cvxlab.support.file_manager import FileManager
from cvxlab.support.sql_manager import SQLManager, db_handler


class Core:
    """Core class defines the interactions among main components of the package.

    The Core class generates instances of Index (with all the information about 
    sets, data tables and variables), SQLManager (with all the tools necessary 
    to handle SQLite database), Database (handling all database operations), and 
    Problem (defining symbolic and numerical problems). It manages the interactions
    among these components, including data fetching and writing to the database,
    variable initialization, problem definition and solving.
    It also provides methods for initializing variables, loading and validating
    symbolic problems, generating numerical problems, and solving both individual
    and integrated problems.

    Attributes:
        logger (Logger): Logger object for logging information.
        files (FileManager): FileManager object for file operations.
        settings (Dict[str, str]): Settings for various file paths and configurations.
        paths (Dict[str, Path]): Paths to various directories and files used in the model.
        sqltools (SQLManager): SQLManager object for database interactions.
        index (Index): Index object for managing data table and variable indices.
        database (Database): Database object for database operations.
        problem (Problem): Problem object for problem definitions and operations.
    """

    def __init__(
            self,
            logger: Logger,
            files: FileManager,
            settings: Dict[str, str],
            paths: Dict[str, Path],
    ):
        """Initialize the Core class with logger, files, settings and paths.

        Args:
            logger (Logger): An instance of Logger for logging information and
                error messages.
            files (FileManager): An instance of FileManager for managing
                file-related operations.
            settings (Dict[str, str]): A dictionary containing configuration
                settings for the application.
            paths (Dict[str, Path]): A dictionary containing paths used throughout
                operations, such as for files and directories.
        """
        self.logger = logger.get_child(__name__)
        self.files = files
        self.settings = settings
        self.paths = paths

        self.sqltools = SQLManager(
            logger=self.logger,
            database_path=self.paths['sqlite_database'],
            database_name=Constants.ConfigFiles.SQLITE_DATABASE_FILE,
        )

        self.index = Index(
            logger=self.logger,
            files=self.files,
            settings=self.settings,
            paths=self.paths,
        )

        self.database = Database(
            logger=self.logger,
            files=self.files,
            paths=self.paths,
            sqltools=self.sqltools,
            settings=self.settings,
            index=self.index,
        )

        self.problem = Problem(
            logger=self.logger,
            files=self.files,
            paths=self.paths,
            settings=self.settings,
            index=self.index
        )

    def initialize_problems_variables(self) -> None:
        """Initialize data structures for handling problem variables.

        This method first iterates over each endogenous data table, generating 
        the coordinate dataframe and the related cvxpy variable in the data table 
        object (cvxpy variable in endogenous data tables include all data tables 
        entries that will be then sliced to be used in the problem). 
        It then iterates over all variables in the index, generating the variable's
        dataframe (including all variables information and the related cvxpy variable)
        in Problem object.

        Raises:
            SettingsError: If a variable's type is not of the allowed type.
        """
        with self.logger.log_timing(
            message=f"Generating data structures for endogenous data tables...",
            level='info',
        ):
            # generate dataframes and cvxpy var for endogenous data tables
            # and for variables with type defined by problem linking logic
            for data_table_key, data_table in self.index.data.items():
                data_table: DataTable

                if data_table.type == 'endogenous' or \
                        isinstance(data_table.type, dict):

                    self.logger.debug(
                        f"Data table '{data_table_key}' | type: {data_table.type} | "
                        "Generating dataframe and cvxpy variable.")

                    # get all coordinates for the data table based on sets
                    data_table.generate_coordinates_dataframes(
                        sets_split_problems=self.index.sets_split_problem_dict
                    )

                    # data table coordinates dataframe are filtered to keep only
                    # coordinates defined by the variables whithin the data table
                    coordinates_df_filtered = pd.DataFrame()
                    for var_key, variable in self.index.variables.items():
                        if var_key in data_table.variables_list:
                            var_coords_df = util.unpivot_dict_to_dataframe(
                                data_dict=variable.all_coordinates_w_headers
                            )
                            coordinates_df_filtered = pd.concat(
                                objs=[coordinates_df_filtered, var_coords_df],
                                ignore_index=True
                            )

                    coordinates_df_filtered = coordinates_df_filtered.drop_duplicates()

                    if isinstance(data_table.coordinates_dataframe, pd.DataFrame):
                        data_table.coordinates_dataframe = \
                            data_table.coordinates_dataframe.merge(
                                right=coordinates_df_filtered,
                                on=list(coordinates_df_filtered.columns),
                                how='inner'
                            )

                    elif isinstance(data_table.coordinates_dataframe, dict):
                        for problem_key, coord_df in \
                                data_table.coordinates_dataframe.items():

                            coord_df: pd.DataFrame
                            data_table.coordinates_dataframe[problem_key] = \
                                coord_df.merge(
                                    right=coordinates_df_filtered,
                                    on=list(coordinates_df_filtered.columns),
                                    how='inner'
                            )

                    # generate cvxpy variables associated with data tables
                    if isinstance(data_table.coordinates_dataframe, pd.DataFrame):
                        cvxpy_var = self.problem.create_cvxpy_variable(
                            var_type='endogenous',
                            integer=data_table.integer,
                            shape=(data_table.table_length, 1),
                            name=data_table_key,
                        )

                    # in case of problem with sets split, multiple endogenous variables
                    # are created and stored in a dictionary.
                    elif isinstance(data_table.coordinates_dataframe, dict):
                        cvxpy_var = {}

                        for problem_key, coord_df in data_table.coordinates_dataframe.items():
                            cvxpy_var[problem_key] = self.problem.create_cvxpy_variable(
                                var_type='endogenous',
                                integer=data_table.integer,
                                shape=(len(coord_df), 1),
                                name=f"{data_table_key}_{problem_key}",
                            )

                    data_table.cvxpy_var = cvxpy_var

        # generating variables dataframes with cvxpy var and filters dictionary
        # (endogenous vars will be sliced from existing cvxpy var in data table)
        with self.logger.log_timing(
            message=f"Generating data structures for all variables and constants...",
            level='info',
        ):
            for var_key, variable in self.index.variables.items():
                variable: Variable

                # for constants, values are directly generated (no dataframes needed)
                if variable.type == 'constant':

                    self.logger.debug(
                        f"Variable '{var_key}' | type: {variable.type} | Constant "
                        f"value '{variable.value}'.")

                    variable.data = self.problem.generate_constant_data(
                        variable_name=var_key,
                        variable=variable
                    )

                # for variables whose type is univocally defined, only one data structure
                # is generated and stored in variable.data
                elif variable.type in ['exogenous', 'endogenous']:

                    self.logger.debug(
                        f"Variable '{var_key}' | type: {variable.type} | Generating "
                        "data structure.")

                    variable.data = self.problem.generate_vars_dataframe(
                        variable_name=var_key,
                        variable=variable
                    )

                # for variable whose type varies depending on the problem, both
                # endogenous/exogenous variable dataframes are stored in
                # variable.data defined as a dictionary
                elif isinstance(variable.type, dict):
                    variable.data = {}

                    self.logger.debug(
                        f"Variable '{var_key}' | type: {variable.type} | Generating "
                        "data structure.")

                    for problem_key, problem_var_type in variable.type.items():
                        variable.data[problem_key] = self.problem.generate_vars_dataframe(
                            variable_name=var_key,
                            variable=variable,
                            variable_type=problem_var_type,
                        )

                else:
                    msg = f"Variable type '{variable.type}' not allowed. Available " \
                        f"types: {Constants.SymbolicDefinitions.ALLOWED_VARIABLES_TYPES}"
                    self.logger.error(msg)
                    raise exc.SettingsError(msg)

    def data_to_cvxpy_exogenous_vars(
            self,
            scenarios_idx: Optional[List[int] | int] = None,
            allow_none_values: bool = True,
            var_list_to_update: List[str] = [],
    ) -> None:
        """Fetch data from the database and assign it to cvxpy exogenous variables.

        This method iterates over each exogenous variable in the Index, getting 
        related data from the SQLite database and assigns it to the cvxpy variable.
        The method handles variables whose type is defined by the problem separately.
        The method can fetch data for all scenarios or for a subset of scenarios 
        (scenarios_idx): scenarios are linear combinations of inter-problem sets 
        values defined in the index. 
        The method can update all exogenous variables or a specified list of variables 
        (var_list_to_update): this may be useful for continuous user model run, 
        when only a subset of exogenous variables need to be updated.

        Args:
            scenarios_idx (Optional[List[int] | int], optional): List of indices
                of scenarios for which to fetch data. If None, fetches data for
                all scenarios. Defaults to None.
            allow_none_values (bool, optional): If True, allows None values in
                the data for the variable. Defaults to True.
            var_list_to_update (List[str], optional): List of variable keys to
                update. If empty, updates all exogenous variables. Defaults to [].

        Raises:
            TypeError: If 'var_list_to_update' is not a list.
            SettingsError: If one or more items in 'var_list_to_update' are not
                in the index variables.
            MissingDataError: If no data or related table is defined for a variable,
                or if the data for a variable contains non-allowed values types.
        """
        with self.logger.log_timing(
            message=f"Fetching data from '{self.settings['sqlite_database_file']}' "
                "to cvxpy exogenous variables...",
            level='info',
        ):
            filter_header = Constants.Labels.FILTER_DICT_KEY
            cvxpy_var_header = Constants.Labels.CVXPY_VAR
            values_header = Constants.Labels.VALUES_FIELD['values'][0]
            id_header = Constants.Labels.ID_FIELD['id'][0]
            allowed_values_types = Constants.NumericalSettings.ALLOWED_VALUES_TYPES

            if not isinstance(var_list_to_update, list):
                msg = "Passed method parameter must be a list."
                self.logger.error(msg)
                raise TypeError(msg)

            if not var_list_to_update == [] and \
                    not util.items_in_list(var_list_to_update, self.index.variables.keys()):
                msg = "One or more passed items are not in the index variables."
                self.logger.error(msg)
                raise exc.SettingsError(msg)

            if var_list_to_update == []:
                var_list_to_update = self.index.list_variables

            with db_handler(self.sqltools):
                for var_key, variable in self.index.variables.items():
                    variable: Variable

                    if var_key not in var_list_to_update:
                        continue

                    if variable.type in ['endogenous', 'constant']:
                        continue

                    self.logger.debug(
                        f"Fetching data to variables | Variable '{var_key}'")

                    err_msg = []

                    if variable.data is None:
                        err_msg.append(
                            f"No data defined for variable '{var_key}'.")

                    if variable.related_table is None:
                        err_msg.append(
                            f"No related table defined for variable '{var_key}'.")

                    if err_msg:
                        self.logger.error("\n".join(err_msg))
                        raise exc.MissingDataError("\n".join(err_msg))

                    # for variables whose type is end/exo depending on the problem,
                    # fetch exogenous variable data.
                    # notice that a variable may be exogenous for more than one problem.
                    if isinstance(variable.type, dict):
                        problem_keys = util.find_dict_keys_corresponding_to_value(
                            variable.type, 'exogenous')
                    else:
                        problem_keys = [None]

                    for problem_key in problem_keys:

                        if problem_key is not None:
                            variable_data = variable.data[problem_key]
                        else:
                            variable_data = variable.data

                        # case when all values of variables need to be fetched
                        if scenarios_idx is None:
                            sets_parsing_hierarchy_idx = list(
                                variable_data.index)

                        # case when values of variables need to be fetched for a
                        # sub-set of inter-problem sets defined by scenarios_idx
                        # (typically when solving integrated problems)
                        else:
                            if isinstance(scenarios_idx, int):
                                scenarios_idx = [scenarios_idx]

                            # case of variable not defined for any inter-problem sets
                            if not variable.coordinates['inter']:
                                sets_parsing_hierarchy_idx = \
                                    list(variable_data.index)

                            # case of variable defined for one or more inter-problem sets
                            # find the index of variable_data that matches the combination
                            # of inter-problem-sets defined by scenarios_idx
                            else:
                                info_label = Constants.Labels.SCENARIO_COORDINATES
                                scenarios_to_fetch = \
                                    self.index.scenarios_info.loc[scenarios_idx].drop(
                                        columns=[info_label]
                                    )

                                var_inter_set_headers = list(
                                    variable.coordinates_info['inter'].values()
                                )

                                variable_data = variable_data.reset_index()

                                variable_data_filtered = variable_data.merge(
                                    right=scenarios_to_fetch,
                                    on=var_inter_set_headers,
                                    how='inner'
                                ).set_index('index')

                                sets_parsing_hierarchy_idx = \
                                    list(variable_data_filtered.index)

                        for combination in sets_parsing_hierarchy_idx:
                            # get raw data from database
                            raw_data = self.database.sqltools.table_to_dataframe(
                                table_name=variable.related_table,
                                filters_dict=variable_data[filter_header][combination]
                            )

                            # check if variable data are int or float
                            non_allowed_ids = util.find_non_allowed_types(
                                dataframe=raw_data,
                                allowed_types=allowed_values_types,
                                target_col_header=values_header,
                                return_col_header=id_header,
                                allow_none=allow_none_values,
                            )

                            if non_allowed_ids:
                                if len(non_allowed_ids) > 5:
                                    non_allowed_ids = non_allowed_ids[:5] + \
                                        [f"(total items {len(non_allowed_ids)})"]
                                msg = f"Data for variable '{var_key}' in table " \
                                    f"'{variable.related_table}' contains " \
                                    f"non-allowed values types in rows: " \
                                    f"{non_allowed_ids}."
                                self.logger.error(msg)
                                raise exc.MissingDataError(msg)

                            # pivoting and reshaping data to fit variables
                            pivoted_data = variable.reshaping_sqlite_table_data(
                                data=raw_data,
                            )

                            self.problem.data_to_cvxpy_variable(
                                var_key=var_key,
                                cvxpy_var=variable_data[cvxpy_var_header][combination],
                                data=pivoted_data
                            )

    def cvxpy_endogenous_data_to_database(
            self,
            scenarios_idx: Optional[List[int] | int] = None,
            force_overwrite: bool = False,
            suppress_warnings: bool = False,
    ) -> None:
        """Export data from cvxpy endogenous variables to the SQLite database.

        This method iterates over each endogenous data table in the Index, and it
        exports the data from the related cvxpy variable into the corresponding 
        data table in the SQLite database. 
        The method can export data for all scenarios or for a subset of scenarios
        (scenarios_idx): scenarios are linear combinations of inter-problem sets
        values defined in the index.
        The method can optionally suppress warnings during the export process (
        force_overwrite, useful for testing purpose).
        The method can optionally force the re-export of data even if the data
        table already exists (suppress_warnings, useful for continuous user model
        run, when only a subset of endogenous variables need to be exported).

        Parameters:
            scenarios_idx (Optional[List[int] | int], optional): List of indices
                of scenarios for which to fetch data. If None, fetches data for
                all scenarios. Defaults to None.
            force_overwrite (bool, optional): If True, forces the re-export of 
                data even if the data table already exists. Defaults to False.
            suppress_warnings (bool, optional): If True, suppresses warnings 
                during the data export process. Defaults to False.
        """
        self.logger.debug(
            "Exporting data from cvxpy endogenous variable (in data table) "
            f"to SQLite database '{self.settings['sqlite_database_file']}' ")

        values_headers = Constants.Labels.VALUES_FIELD['values'][0]

        if scenarios_idx is None:
            scenarios_list = list(self.index.scenarios_info.index)
        else:
            if isinstance(scenarios_idx, int):
                scenarios_list = [scenarios_idx]

        with db_handler(self.sqltools):
            for data_table_key, data_table in self.index.data.items():
                data_table: DataTable

                if data_table.type in ['exogenous', 'constant']:
                    continue

                if isinstance(data_table.coordinates_dataframe, pd.DataFrame):
                    data_table_dataframe = data_table.coordinates_dataframe

                elif isinstance(data_table.coordinates_dataframe, dict):
                    dataframes_list = [
                        dataframe for df_key, dataframe
                        in data_table.coordinates_dataframe.items()
                        if df_key in scenarios_list
                    ]
                    data_table_dataframe = pd.concat(
                        objs=dataframes_list,
                        ignore_index=True
                    )

                if not util.add_column_to_dataframe(
                    dataframe=data_table_dataframe,
                    column_header=values_headers,
                ):
                    if self.settings['log_level'] == 'debug' or \
                            not suppress_warnings:
                        self.logger.warning(
                            f"Column '{values_headers}' already exists in data "
                            f"table '{data_table_key}'")

                if data_table.cvxpy_var is None:
                    if self.settings['log_level'] == 'debug' or \
                            not suppress_warnings:
                        self.logger.warning(
                            f"No data available in cvxpy variable '{data_table_key}'")
                    continue

                if isinstance(data_table.cvxpy_var, dict):
                    cvxpy_var_values_list = []
                    for cvxpy_var_key, cvxpy_var in data_table.cvxpy_var.items():
                        cvxpy_var: cp.Variable
                        if cvxpy_var_key in scenarios_list:
                            cvxpy_var_values_list.append(cvxpy_var.value)

                    cvxpy_var_data = np.vstack(cvxpy_var_values_list)

                else:
                    cvxpy_var_data = data_table.cvxpy_var.value

                data_table_dataframe[values_headers] = cvxpy_var_data

                self.sqltools.dataframe_to_table(
                    table_name=data_table_key,
                    dataframe=data_table_dataframe,
                    action='update',
                    force_overwrite=force_overwrite,
                    suppress_warnings=suppress_warnings,
                )

    def check_exogenous_data_coherence(self) -> None:
        """Check coherence of exogenous data in the SQLite database.

        The method parses all exogenous data tables in the Database, checking 
        for NULL entries in the 'values' column. Since all exogenous data are 
        expected to be filled by the user before running the model, in case NULL 
        entries are found, the method logs the table name and the corresponding 
        row IDs, and raises an error.

        Raises:
            exc.MissingDataError: If NULL entries are found in any data table.
        """
        with self.logger.log_timing(
            message=f"Checking exogenous data coherence...",
            level='info',
        ):
            null_entries = {}
            column_to_inspect = Constants.Labels.VALUES_FIELD['values'][0]
            column_with_info = Constants.Labels.ID_FIELD['id'][0]

            with db_handler(self.sqltools):
                for table_name, data_table in self.index.data.items():
                    data_table: DataTable

                    if data_table.type in ('endogenous', 'constant'):
                        continue

                    null_list = self.sqltools.get_null_values(
                        table_name=table_name,
                        column_to_inspect=column_to_inspect,
                        column_with_info=column_with_info,
                    )

                    if null_list:
                        null_entries[table_name] = null_list

            if null_entries:
                for table, rows in null_entries.items():
                    if len(rows) > 5:
                        rows = rows[:5] + [f"(total items {len(rows)})"]
                    self.logger.error(
                        f"Data coherence check | Table '{table}' | "
                        f"NULLs at id rows: {rows}."
                    )
                raise exc.MissingDataError(
                    "Data coherence check | NULL entries found in "
                    f"data tables: {list(null_entries.keys())}"
                )

    def load_and_validate_symbolic_problem(
            self,
            force_overwrite: bool = False,
    ) -> None:
        """Call methods to load and validate symbolic problem.

        The method calls the 'load_symbolic_problem_from_file' and
        'validate_symbolic_expressions' methods of the Problem instance to load
        and validate the symbolic problem definitions from a file.
        """
        with self.logger.log_timing(
            message=f"Loading and validating symbolic problem...",
            level='info',
        ):
            self.problem.load_symbolic_problem_from_file(force_overwrite)
            self.problem.validate_symbolic_expressions()

    def generate_numerical_problem(
            self,
            force_overwrite: bool,
            allow_none_values: bool,
    ) -> None:
        """Call methods to generate numerical problems.

        The method initializes problem variables, fetch data from SQLite database
        to exogenous variables, and generate numerical problems. 
        The method can optionally overwrite existing problem definitions without
        prompting the user (force_overwrite, useful for testing purpose).
        The method can allow None values in the data for exogenous variables

        Args:
            force_overwrite (bool, optional): If True, forces the redefinition 
                of problems without prompting the user. Defaults to False.
            allow_none_values (bool, optional): If True, allows None values in
                the data for exogenous variables.
        """
        self.initialize_problems_variables()
        self.data_to_cvxpy_exogenous_vars(allow_none_values=allow_none_values)
        self.problem.generate_numerical_problems(force_overwrite)

    def solve_numerical_problems(
            self,
            solver: str,
            solver_verbose: bool,
            integrated_problems: bool,
            force_overwrite: bool,
            maximum_iterations: Optional[int] = None,
            numerical_tolerance: Optional[float] = None,
            **kwargs: Any,
    ) -> None:
        """Solve independent or integrated numerical problems.

        The method solves all defined numerical problems using the specified 
        solver, verbosity and numerical settings.
        The method checks if numerical problems have been defined and if they 
        have already been solved. If the problems have not been solved or if 
        'force_overwrite' is True, the method solves the problems using the 
        specified solver. The method can solve the problems individually or as 
        an integrated problem, depending on the 'integrated_problems' setting.
        The method logs information about the problem solving process.
        The method fetches the problem status after solving the problems.

        Args:
            solver (str): The solver to use for solving the problems. 
            solver_verbose (bool): If True, enables verbose output of solver 
                during problem solving.
            integrated_problems (bool): If True, solves the problems as an 
                integrated problem. If False, solves the problems as independent.
            force_overwrite (bool): If True, forces the re-solution of problems 
                even if they have already been solved without prompting the user.
            maximum_iterations (Optional[int], optional): The maximum number of 
                iterations for the solver. Overwrite default setting in Constants. 
                Defaults to None.
            numerical_tolerance (Optional[float], optional): The numerical 
                tolerance for the solver. Overwrite default setting in Constants. 
                Defaults to None.
            **kwargs: Additional keyword arguments passed to the solver.

        Raises:
            OperationalError: If numerical problems have not been defined.
        """
        if self.problem.numerical_problems is None:
            msg = "Numerical problems must be defined first."
            self.logger.warning(msg)
            raise exc.OperationalError(msg)

        problem_status = self.problem.problem_status

        if (isinstance(problem_status, dict) and
            not all(value is None for value in problem_status.values())) or \
                (problem_status is not None and not isinstance(problem_status, dict)):

            if not force_overwrite:
                self.logger.warning("Numeric problems already solved.")
                if not util.get_user_confirmation("Solve again numeric problems?"):
                    self.logger.warning("Numeric problem NOT solved.")
                    return

        if integrated_problems:
            self.solve_integrated_problems(
                solver=solver,
                solver_verbose=solver_verbose,
                numerical_tolerance=numerical_tolerance,
                maximum_iterations=maximum_iterations,
                **kwargs,
            )
        else:
            self.solve_independent_problems(
                solver=solver,
                solver_verbose=solver_verbose,
                **kwargs
            )

        self.problem.fetch_problem_status()

    def check_results_as_expected(
            self,
            values_relative_diff_tolerance: float,
    ) -> None:
        """Check if results match expected results in a reference SQLite database.

        The method checks if the results of the model SQLite database match the 
        expected results in a reference SQLite database.
        This method uses the 'check_databases_equality' method to compare the 
        current database with a test database. The test database is specified 
        by the 'sqlite_database_file_test' setting and is located in the model 
        directory.

        Args:
            values_relative_diff_tolerance (float): The relative difference 
                tolerance (%) to use when comparing the databases. It overwrites
                the default setting in Constants.
        """
        with db_handler(self.sqltools):
            self.sqltools.check_databases_equality(
                other_db_dir_path=self.paths['model_dir'],
                other_db_name=Constants.ConfigFiles.SQLITE_DATABASE_FILE_TEST,
                tolerance_percentage=values_relative_diff_tolerance,
            )

    def solve_independent_problems(
            self,
            solver: str,
            solver_verbose: bool,
            **kwargs: Any,
    ) -> None:
        """Solve independent numerical problems.

        This method get and solve the numerical problem/s in the Problem instance
        based on a defined solver and verbosity settings. Eventually, additional
        arguments can be passed to the solver.
        The method updates the 'status' field of the input DataFrame(s) in-place 
        to reflect the solution status of each problem.

        Parameters:
            solver (str): The solver to use. If None, default solver will be chosen
                automatically.
            verbose (bool): If set to True, the solver will print progress information.
            **kwargs (Any): Additional arguments to pass to the solver.

        Raises:
            exc.OperationalError: If 'numerical_problems' has not defined as Problem
                property.
        """
        numerical_problems = self.problem.numerical_problems

        if isinstance(numerical_problems, pd.DataFrame):
            self.problem.solve_problem_dataframe(
                problem_dataframe=numerical_problems,
                solver_verbose=solver_verbose,
                solver=solver,
                **kwargs
            )
        elif isinstance(numerical_problems, dict):
            for sub_problem in numerical_problems.keys():
                self.problem.solve_problem_dataframe(
                    problem_dataframe=numerical_problems[sub_problem],
                    problem_name=sub_problem,
                    solver_verbose=solver_verbose,
                    solver=solver,
                    **kwargs
                )
        else:
            if numerical_problems is None:
                msg = "Numerical problems must be defined first."
                self.logger.warning(msg)
                raise exc.OperationalError(msg)

    def solve_integrated_problems(
            self,
            solver: str,
            solver_verbose: bool,
            numerical_tolerance: Optional[float] = None,
            maximum_iterations: Optional[int] = None,
            **kwargs: Any,
    ) -> None:
        """Solve integrated numerical problems iteratively.

        Nonlinear problems are formulated by the user as sequence of convex problems
        (i.e. decomposed into coupled convex subproblems). These problems are 
        solved iteratively using a block Gauss-Seidel (alternating optimization) 
        scheme, where updated endogenous variables are exchanged until convergence.

        This method implement such iterative algorithm, solving problems using the 
        specified solver and verbosity settings.
        First, the method creates a backup copy of the original database, which is
        used to restore the database at the end of the iterations.
        Then, for each scenario defined in the index, the method iteratively solves
        all sub-problems until convergence is reached or until the maximum number
        of iterations is reached.
        The method calculates the relative difference between the solutions in 
        consecutive iterations using the 'get_tables_values_relative_difference' 
        method of the SQLTools instance.
        The method handles the database operations required for each iteration, 
        including updating the data for exogenous variables and exporting the 
        data for endogenous variables.
        Differently with respect to solve_independent_problems() method, this method
        solve all sub-problems iteratively for the same case (combination of sets).

        Args:
            solver (str): The solver to use. If None, default solver will be chosen
                automatically.
            solver_verbose (bool): If True, enables verbose output during problem 
                solving.
            maximum_iterations (Optional[int], optional): The maximum number of 
                iterations for the solver. Overwrite default setting in Constants. 
                Defaults to None.
            numerical_tolerance (Optional[float], optional): The numerical 
                tolerance for the solver. Overwrite default setting in Constants. 
                Defaults to None.
            **kwargs (Any): Additional arguments to pass to the solver.
        """
        if maximum_iterations is None:
            maximum_iterations = \
                Constants.NumericalSettings.MAXIMUM_ITERATIONS_MODEL_COUPLING

        if numerical_tolerance is None:
            numerical_tolerance = \
                Constants.NumericalSettings.TOLERANCE_MODEL_COUPLING_CONVERGENCE

        sqlite_db_file_name = Constants.ConfigFiles.SQLITE_DATABASE_FILE
        sqlite_db_file_name_bkp = Constants.ConfigFiles.SQLITE_DATABASE_FILE_BKP
        scenarios_header = Constants.Labels.SCENARIO_COORDINATES
        problem_status_header = Constants.Labels.PROBLEM_STATUS

        sqlite_db_path = self.paths['model_dir']
        base_name, extension = os.path.splitext(sqlite_db_file_name)
        sqlite_db_file_name_previous = f"{base_name}_previous{extension}"

        tables_to_check = self.problem.endogenous_tables
        sub_problems_keys = list(self.problem.numerical_problems.keys())
        scenarios_df = self.index.scenarios_info

        problems_status = pd.DataFrame(
            index=scenarios_df.index,
            columns=sub_problems_keys,
        )

        # create a backup copy of the original database
        self.files.copy_file_to_destination(
            path_destination=sqlite_db_path,
            path_source=sqlite_db_path,
            file_name=sqlite_db_file_name,
            file_new_name=sqlite_db_file_name_bkp,
            force_overwrite=True,
        )

        try:
            for scenario_idx in scenarios_df.index:

                scenario_coords = scenarios_df.loc[
                    scenario_idx,
                    scenarios_header
                ]

                self.logger.info("=================================")
                if scenario_coords:
                    self.logger.info(
                        f"Solving integrated problems for scenario {scenario_coords}"
                    )
                else:
                    self.logger.info("Solving integrated problems")

                iter_count = 0

                while True:
                    try:
                        iter_count += 1
                        self.logger.info(
                            f"Iteration count: {iter_count} | "
                            f"iterations limit: {maximum_iterations}")

                        if iter_count > maximum_iterations:
                            self.logger.warning(
                                "Maximum number of iterations hit before reaching "
                                f"convergence (tolerance: {numerical_tolerance*100}%).")
                            break

                        if iter_count > 1:
                            self.logger.info(
                                "Updating exogenous variables data from "
                                "previous iteration.")

                            self.data_to_cvxpy_exogenous_vars(
                                scenarios_idx=scenario_idx)

                        self.files.copy_file_to_destination(
                            path_destination=sqlite_db_path,
                            path_source=sqlite_db_path,
                            file_name=sqlite_db_file_name,
                            file_new_name=sqlite_db_file_name_previous,
                            force_overwrite=True,
                        )

                        for sub_problem, problem_df \
                                in self.problem.numerical_problems.items():

                            self.problem.solve_problem_dataframe(
                                problem_name=sub_problem,
                                problem_dataframe=problem_df,
                                scenarios_idx=scenario_idx,
                                solver=solver,
                                solver_verbose=solver_verbose,
                                **kwargs
                            )

                            status = problem_df.loc[
                                scenario_idx,
                                problem_status_header
                            ]

                            problems_status.at[scenario_idx, sub_problem] = \
                                status

                        if not all(
                            problems_status.loc[scenario_idx] == 'optimal'
                        ):
                            self.logger.warning(
                                "One or more sub-problems infeasible for scenario "
                                f"{scenario_coords}."
                            )
                            break

                        self.logger.info(
                            "Problems solved successfully. Exporting data to "
                            "SQLite database.")

                        self.cvxpy_endogenous_data_to_database(
                            scenarios_idx=scenario_idx,
                            force_overwrite=True,
                            suppress_warnings=True,
                        )

                        if iter_count == 1:
                            continue

                        # relative error must be computed for scenarios_idx only
                        # funziona lo stesso, perchè se il problema è infeasible i
                        # risultati non vengono esportati (break qui sopra) e il
                        # database rimane sempre uguale
                        with db_handler(self.sqltools):
                            relative_difference = \
                                self.sqltools.get_tables_values_relative_difference(
                                    other_db_dir_path=sqlite_db_path,
                                    other_db_name=sqlite_db_file_name_previous,
                                    tables_names=tables_to_check,
                                )

                        relative_difference_above = {
                            table: value
                            for table, value in relative_difference.items()
                            if value > numerical_tolerance
                        }

                        if relative_difference_above:
                            self.logger.info(
                                "Data tables with highest relative difference above "
                                f"treshold ({numerical_tolerance} %):"
                            )
                            for table, value in relative_difference_above.items():
                                self.logger.info(
                                    f"Data table '{table}': {round(value, 5)}")
                        else:
                            self.logger.info(
                                f"Numerical convergence reached in {iter_count} "
                                f"iterations | Scenario {scenario_coords}.")
                            break

                    finally:
                        self.files.erase_file(
                            dir_path=sqlite_db_path,
                            file_name=sqlite_db_file_name_previous,
                            force_erase=True,
                            confirm=False,
                        )

        finally:
            # after iterations are concluded for all scenarios
            # erase the database modified during the iterations
            # and restore original database from backup
            self.files.erase_file(
                dir_path=sqlite_db_path,
                file_name=sqlite_db_file_name,
                force_erase=True,
                confirm=False,
            )

            self.files.rename_file(
                dir_path=sqlite_db_path,
                name_old=sqlite_db_file_name_bkp,
                name_new=sqlite_db_file_name,
            )

    def __repr__(self):
        """Return a string representation of the Core instance."""
        class_name = type(self).__name__
        return f'{class_name}'
