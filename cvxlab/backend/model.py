"""Module defining the Model class.

This module defines the Model class, the main object of the CVXLab package,
in charge of getting the main model settings and paths, and providing all the 
methods useful for the user to handle the model and its main functionalities.
The Model class integrates various components such as logging, file management,
and core functionalities, ensuring a cohesive workflow from numerical problem
conceptualization, database generation and data input, numerical problem generation
and solution, results export to database.
The Model class embeds the generation of the Core class, which provides the centralized
data indexing, functionalities for SQLite database management, problem formulation 
and solution through cvxpy package. 
"""
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

import pandas as pd
import cvxpy as cp

from cvxlab.constants import Constants
from cvxlab.backend.core import Core
from cvxlab.log_exc import exceptions as exc
from cvxlab.log_exc.logger import Logger
from cvxlab.support.dotdict import DotDict
from cvxlab.support.file_manager import FileManager
from cvxlab.support import util


class Model:
    """Central class for generating and handling a CVXLab models.

    The Model class represents a modeling environment that handles SQLite data 
    generation and processing, database interactions, numerical optimization 
    model generation and handling with cvxpy package. 
    This class initializes with a configuration for managing directories, 
    logging, and file management for a specific model. It also sets up various
    components including a logger, file manager, and core functionalities.

    Attributes:
        logger (Logger): Logger object for logging information, warnings, and errors.
        files (FileManager): An instance of FileManager to manage file operations.
        settings (DotDict): A dictionary-like object storing configurations such as 
            model name, file paths, and operational flags.
        paths (DotDict): A dictionary-like object storing the paths for model 
            directories and associated files.
        core (Core): An instance of Core that manages the core functionality 
            of the model (it embeds Index, Database and Problem instances).
    """

    def __init__(
            self,
            model_dir_name: str,
            main_dir_path: str,
            model_settings_from: Literal['yml', 'xlsx'] = 'xlsx',
            use_existing_data: bool = False,
            multiple_input_files: bool = False,
            log_level: Literal['info', 'debug', 'warning', 'error'] = 'info',
            log_format: Literal['standard', 'detailed'] = 'standard',
            detailed_validation: bool = False,
    ):
        """Initialize the Model instance with specified configurations.

        This constructor sets up the Model instance by initializing logging,
        file management, and core functionalities. It also checks for the
        existence of the model directory and required setup files. If the
        'use_existing_data' flag is set to True, it loads existing sets data
        and variable coordinates to the Model.Index and initializes numerical
        problems (the configuration files and model database should have been
        already generated).

        Args:
            model_dir_name (str): The name of the model directory.
            main_dir_path (str): The main directory path where the model
                directory is located or where it will be generated.
            model_settings_from (Literal['yml', 'xlsx'], optional): The format
                of the model settings file. Can be either 'yml' or 'xlsx'. 
                Defaults to 'xlsx'.
            use_existing_data (bool, optional): if True, generation of Model
                instance is also loading model coordinates and initializing
                numerical problems. Note that setup files and model database should
                have been already generated. Defaults to False.
            multiple_input_files (bool, optional): if True, input data Excel files
                are generated as one file per data table. If False, all data tables
                are generated in a single Excel file with multiple tabs. Defaults 
                to False.
            log_level (Literal['info', 'debug', 'warning', 'error'], optional):
                The logging level for the logger. Defaults to 'info'.
            log_format (Literal['standard', 'detailed'], optional): The logging 
                format for the logger. Defaults to 'standard'.
            detailed_validation (bool, optional): if True, performs detailed
                validation logging of data and model settings during initialization.
                Defaults to False.
        """
        config = Constants.ConfigFiles
        model_dir_path = Path(main_dir_path) / model_dir_name

        self.logger = Logger(
            logger_name=str(self),
            log_level=log_level.upper(),
            log_format=log_format,
        )

        with self.logger.log_timing(
            message=f"Model instance generation...",
            level='info',
        ):
            self.files = FileManager(logger=self.logger)

            self.settings = DotDict({
                'log_level': log_level,
                'model_name': model_dir_name,
                'model_settings_from': model_settings_from,
                'use_existing_data': use_existing_data,
                'multiple_input_files': multiple_input_files,
                'detailed_validation': detailed_validation,
                'sets_xlsx_file': config.SETS_FILE,
                'input_data_dir': config.INPUT_DATA_DIR,
                'input_data_file': config.INPUT_DATA_FILE,
                'sqlite_database_file': config.SQLITE_DATABASE_FILE,
                'sqlite_database_file_test': config.SQLITE_DATABASE_FILE_TEST,
            })

            self.paths = DotDict({
                'model_dir': model_dir_path,
                'input_data_dir': model_dir_path / config.INPUT_DATA_DIR,
                'sets_excel_file': model_dir_path / config.SETS_FILE,
                'sqlite_database': model_dir_path / config.SQLITE_DATABASE_FILE,
            })

            self.check_model_dir()

            self.core = Core(
                logger=self.logger,
                files=self.files,
                settings=self.settings,
                paths=self.paths,
            )

            if self.settings['use_existing_data']:
                self.load_model_coordinates()
                self.initialize_problems()

    @property
    def sets(self) -> List[str]:
        """List of sets names available in the model.

        Returns:
            List[str]: A list of set names.
        """
        return self.core.index.list_sets

    @property
    def data_tables(self) -> List[str]:
        """List of data tables names available in the model.

        Returns:
            List[str]: A list of data table names.
        """
        return self.core.index.list_data_tables

    @property
    def variables(self) -> List[str]:
        """List of variables names available in the model.

        Returns:
            List[str]: A list of variable names.
        """
        return self.core.index.list_variables

    @property
    def is_problem_solved(self) -> bool:
        """Status of the problem solution.

        Checks if the numerical problem has been solved (even if it has not 
        found a numerical solution).

        Returns:
            bool: True if the problem has been solved, False otherwise.
        """
        if self.core.problem.problem_status is None:
            return False
        else:
            return True

    def check_model_dir(self) -> None:
        """Validate the existence of the model directory and required setup files.

        This method checks if the model directory and all the required setup 
        files exist based on the attribute 'model_settings_from'.
        This method is called during the initialization of the Model instance, 
        and it is not meant to be called directly by the user.

        Raises:
            exc.SettingsError: If the 'model_settings_from' parameter is not recognized.
            exc.SettingsError: If the model directory or any of the required 
                setup files are missing.
        """
        files_type = self.settings['model_settings_from']

        if files_type == 'yml':
            setup_files = [
                file + '.yml'
                for file in Constants.ConfigFiles.SETUP_INFO.values()
            ]
        elif files_type == 'xlsx':
            setup_files = [Constants.ConfigFiles.SETUP_XLSX_FILE]
        else:
            msg = "Parameter 'model_settings_from' not recognized."
            self.logger.error(msg)
            raise exc.SettingsError(msg)

        if self.files.dir_files_check(
            dir_path=self.paths['model_dir'],
            files_names_list=setup_files,
        ):
            self.logger.debug(
                f"Model directory and setup '{files_type}' file/s already "
                "exist.")

        else:
            msg = f"Model directory or setup '{files_type}' file/s missing."
            self.logger.error(msg)
            raise exc.SettingsError(msg)

    def load_model_coordinates(self, fetch_foreign_keys: bool = True) -> None:
        """Load sets data and define data tables/variables coordinates.

        This method fetches sets data from Excel to sets instances. It then 
        loads such data (referred as coordinates) to data tables and to variables. 
        Then, it filter variables coordinates based on user defined filters, and 
        checks variables coherence.
        If 'fetch_foreign_keys' flag is enabled, the method finally fetches 
        foreign keys to data tables to enable SQLite foreign keys constraints.

        If the 'use_existing_data' flag is set to True, this method is called 
        during the initialization of the Model instance, and it is not meant to
        be called directly by the user.
        If the 'use_existing_data' flag is set to False, the user can call this
        method directly, after having generated the model instance, filled the 
        sets Excel file with data, defined model settings (data tables, variables,
        symbolic problem).

        Raises:
            exc.SettingsError: If the sets Excel file specified in the settings 
                is missing.
        """
        with self.logger.log_timing(
            message=f"Loading sets and variables coordinates...",
            level='info',
        ):
            try:
                sets_xlsx_file = Constants.ConfigFiles.SETS_FILE
                self.core.index.load_sets_data_to_index(
                    excel_file_name=sets_xlsx_file,
                    excel_file_dir_path=self.paths['model_dir']
                )
            except FileNotFoundError as e:
                msg = f"'{sets_xlsx_file}' file missing. Set 'use_existing_data' " \
                    "to False to generate a new settings file."
                self.logger.error(msg)
                raise exc.SettingsError(msg) from e

            self.core.index.load_coordinates_to_data_index()
            self.core.index.load_all_coordinates_to_variables_index()
            self.core.index.filter_coordinates_in_variables_index()
            self.core.index.check_variables_coherence()

            if fetch_foreign_keys:
                self.core.index.fetch_foreign_keys_to_data_tables()

    def initialize_blank_data_structure(self) -> None:
        """Initialize blank data structure for the model.

        This method generates the fundamental blank data structure for the model.
        If the SQLite database already exists, it gives the option to erase it 
        and generate a new one, or to work with the existing SQLite database.
        Same for the input data directory.
        Specifically, the method creates:
            A blank SQLite database with set tables and data tables, filling data 
                tables with sets information.
            A blank Excel input data file/s with normalized data tables for getting
                exogenous variables data from the user. 
        """
        use_existing_data = self.settings['use_existing_data']
        sqlite_db_name = Constants.ConfigFiles.SQLITE_DATABASE_FILE
        sqlite_db_path = Path(self.paths['sqlite_database'])
        input_files_dir_path = Path(self.paths['input_data_dir'])

        erased_db = False
        erased_input_dir = False

        if use_existing_data:
            self.logger.info(
                "Relying on existing SQLite database and input excel file/s.")
            return

        with self.logger.log_timing(
            message=f"Generation of blank data structures...",
            level='info',
        ):
            if sqlite_db_path.exists():
                erased_db = self.files.erase_file(
                    dir_path=self.paths['model_dir'],
                    file_name=sqlite_db_name,
                    force_erase=False,
                    confirm=True,
                )

            if erased_db:
                self.logger.info(
                    f"Existing SQLite database '{sqlite_db_name}' erased.")

            if erased_db or not sqlite_db_path.exists():
                self.logger.info(
                    f"Creating new blank SQLite database '{sqlite_db_name}'.")
                self.core.database.create_blank_sqlite_database()
                self.core.database.load_sets_to_sqlite_database()
                self.core.database.generate_blank_sqlite_data_tables()
                self.core.database.sets_data_to_sql_data_tables()
            else:
                self.logger.info(
                    f"Relying on existing SQLite database '{sqlite_db_name}' ")

            if input_files_dir_path.exists():
                erased_input_dir = self.files.erase_dir(
                    dir_path=input_files_dir_path,
                    force_erase=False,
                )

                if erased_input_dir:
                    self.logger.info("Existing input data directory erased.")

            if erased_input_dir or not input_files_dir_path.exists():
                self.logger.info(
                    "Generating new blank input data directory and related file/s.")
                self.core.database.generate_blank_data_input_files()
            else:
                self.logger.info("Relying on existing input data directory.")

    def generate_input_data_files(self, table_key_list: List[str] = []) -> None:
        """Generate blank Excel files for data input.

        This method generates blank Excel files for data input, based on the
        data tables defined in the model. If the input data directory already
        exists, it gives the option to erase it and generate a new one, or to
        work with the existing input data directory.
        This method is called within the 'initialize_blank_data_structure'
        method. However, the user can call it directly to regenerate input
        data file/s, for all or for specific data tables (with the 'table_key_list'
        attribute). This is especially useful in adjusting the input data without 
        regenerating the whole blank data structure. This feature works also in
        case of one single Excel file, since it can overwrite only the tabs
        related to the specified data tables.

        Args:
            table_key_list (List[str], optional): A list of data table keys 
                for which to generate input data files. If empty, all data 
                tables are generated. Defaults to [].

        Raises:
            exc.SettingsError: If the input data directory is missing.
            exc.SettingsError: If any of the specified table keys are invalid 
                (i.e., not exogenous data tables).
        """
        input_files_dir_path = Path(self.paths['input_data_dir'])

        if not input_files_dir_path.exists():
            msg = "Input data directory missing. Initialize blank data " \
                "structure first."
            self.logger.error(msg)
            raise exc.SettingsError(msg)

        if table_key_list != [] and not util.items_in_list(
            table_key_list,
            self.core.index.list_exogenous_data_tables
        ):
            msg = "Invalid table key/s provided. Only exogenous data tables " \
                "can be exported to input data files."
            self.logger.error(msg)
            raise exc.SettingsError(msg)

        if table_key_list != []:
            msg = f"Generating input data files for tables: '{table_key_list}'..."
        else:
            msg = "Generating all input data files..."

        with self.logger.log_timing(
            message=msg,
            level='info',
        ):
            self.core.database.generate_blank_data_input_files(table_key_list)

    def load_exogenous_data_to_sqlite_database(
            self,
            force_overwrite: bool = False,
            table_key_list: list[str] = [],
    ) -> None:
        """Load exogenous (input) data to the SQLite database.

        This method loads exogenous (input) data from Excel file/s to the
        SQLite database. It also fills NaN values in the database with Null
        values, to ensure proper handling of missing data in SQLite.
        This method is called directly by the user after having filled the
        input data Excel file/s with exogenous data.
        However, the method is also called within the 'update_database_and_problem'
        method, which can be used in case some changes in exogenous data have been
        made, so that the SQLite database and the problems can be updated without
        re-generating the Model instance.
        The user can choose to load data for all exogenous data tables, or for
        specific data tables (with the 'table_key_list' attribute).

        Args:
            force_overwrite (bool, optional): Whether to force overwrite existing 
                data without asking for user permission. Defaults to False.
            table_key_list (list[str], optional): A list of data table keys 
                for which to load exogenous data. If empty, all exogenous data
                tables are loaded. Defaults to [].
        """
        with self.logger.log_timing(
            message=f"Loading input data to SQLite database...",
            level='info',
        ):
            self.core.database.load_data_input_files_to_database(
                force_overwrite=force_overwrite,
                table_key_list=table_key_list,
            )

            self.core.database.fill_nan_values_in_database(
                force_overwrite=force_overwrite,
                table_key_list=table_key_list,
            )

    def initialize_problems(
            self,
            force_overwrite: bool = False,
            allow_none_values: bool = True,
    ) -> None:
        """Initialize numerical problems in the Model instance.

        This method intializes numerical problems in the Model instance. 
        Specifically, the method loads and validates symbolic mathematical problems,
        checks if all exogenous data have coherently defined by user, and finally
        generates numercal problem (i.e. initializes variables, feeds data to 
        exogenous variables, and generates cvxpy problem/s).

        Args:
            force_overwrite (bool, optional): If True, forces the overwrite 
                of existing numerical problems without asking for user 
                permission. Used for testing purposes. Defaults to False.
            allow_none_values (bool, optional): If True, allows None values in
                the exogenous data. Defaults to True.
        """
        with self.logger.log_timing(
            message=f"Numerical model generation...",
            level='info',
        ):
            self.core.load_and_validate_symbolic_problem(force_overwrite)
            self.core.check_exogenous_data_coherence()
            self.core.generate_numerical_problem(
                allow_none_values, force_overwrite)

    def run_model(
        self,
        verbose: bool = False,
        force_overwrite: bool = False,
        integrated_problems: bool = False,
        solver: Optional[str] = None,
        numerical_tolerance: Optional[float] = None,
        maximum_iterations: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        """Solve numerical problems defined by the model instance.

        This method first performs some coherence checks (if solver is supported,
        if numerical problems are defined, if integrated problems are possible).
        Then, it solves the numerical problems, either independently or in an
        integrated manner, based on the 'integrated_problems' flag.
        Finally, it logs a summary of the problems status.

        Args:
            verbose (bool, optional): If True, logs verbose output related to 
                numerical solver operation during the model run. Defaults to False.
            force_overwrite (bool, optional): If True, overwrites existing results. 
                Defaults to False.
            integrated_problems (bool, optional): If True, solve problems iteratively 
                using a block Gauss-Seidel (alternating optimization) scheme, where 
                updated endogenous variables are exchanged until convergence. 
                Defaults to False.
            solver (str, optional): The solver to use for solving numerical 
                problems. Defaults to None, in which case the default solver 
                specified in 'Constants.NumericalSettings.DEFAULT_SOLVER' is used.
            numerical_tolerance (float, optional): The numerical tolerance for 
                solving integrated problems. In case it is not defined, this is set
                as 'Constants.NumericalSettings.TOLERANCE_MODEL_COUPLING_CONVERGENCE'.
            maximum_iterations (int, optional): The maximum number of iterations 
                for solving integrated problems. In case it is not defined, this is
                set as 'Constants.NumericalSettings.MAXIMUM_ITERATIONS_MODEL_COUPLING'.
            **kwargs: Additional keyword arguments to be passed to the solver.

        Raises:
            exc.SettingsError: In case solver is not supported by current cvxpy version.
            exc.SettingsError: If no numerical problems are found, or if integrated
                problems are requested but only one problem is found.
        """
        sub_problems = self.core.problem.number_of_sub_problems
        problem_scenarios = len(self.core.index.scenarios_info)
        allowed_solvers = Constants.NumericalSettings.ALLOWED_SOLVERS

        if solver is None:
            solver = Constants.NumericalSettings.DEFAULT_SOLVER

        if solver not in allowed_solvers:
            msg = f"Solver '{solver}' not supported by current CVXPY version. " \
                f"Available solvers: {allowed_solvers}"
            self.logger.error(msg)
            raise exc.SettingsError(msg)

        if sub_problems == 0:
            msg = "Numerical problem not found. Initialize problem first."
            self.logger.error(msg)
            raise exc.SettingsError(msg)

        if integrated_problems and sub_problems == 1:
            msg = "Only one problem found. Integrated problems not possible."
            self.logger.error(msg)
            raise exc.SettingsError(msg)

        if integrated_problems and sub_problems > 1:
            solution_type = 'integrated'
        else:
            solution_type = 'independent'

        problem_count = '1' if sub_problems == 1 else f'{sub_problems}'

        self.logger.info(
            f"Model run summary: "
            f"\n\tNumber of problems: {problem_count} "
            f"\n\tSolution mode: '{solution_type}' "
            f"\n\tScenarios number: {problem_scenarios} "
            f"\n\tSolver: '{solver}'\n")

        if verbose:
            self.logger.info("="*30)
            self.logger.info("cvxpy logs below.")

        with self.logger.log_timing(
            message=f"Solving numerical problems...",
            level='info',
        ):
            self.core.solve_numerical_problems(
                solver=solver,
                solver_verbose=verbose,
                force_overwrite=force_overwrite,
                integrated_problems=integrated_problems,
                numerical_tolerance=numerical_tolerance,
                maximum_iterations=maximum_iterations,
                canon_backend=cp.SCIPY_CANON_BACKEND,
                ignore_dpp=True,
                **kwargs,
            )

        self.logger.info("="*30)
        self.logger.info("Numerical problems status report:")
        for info, status in self.core.problem.problem_status.items():
            self.logger.info(f"{info}: {status}")

    def load_results_to_database(
        self,
        scenarios_idx: Optional[List[int] | int] = None,
        force_overwrite: bool = False,
        suppress_warnings: bool = False,
    ) -> None:
        """Export model results to the SQLite database.

        This method exports the results of the numerical problems to the SQLite
        database. It can export results for all scenarios or for specific scenarios
        (defined as the linear combinations of inter-problem sets that identify 
        independent numerical problems), based on the 'scenarios_idx' attribute 

        Args:
            scenarios_idx (Optional[List[int] | int], optional): A list of
                scenario indices or a single scenario index for which to export
                results. If None, results for all scenarios are exported. Defaults
                to None.
            force_overwrite (bool, optional): Whether to overwrite/update 
                existing data without asking user permission. Defaults to False.
            suppress_warnings (bool, optional): Whether to suppress warnings 
                during the data loading process. Defaults to False.
        """
        with self.logger.log_timing(
            message=f"Exporting endogenous model results to SQLite database...",
            level='info',
        ):
            if not self.is_problem_solved:
                self.logger.warning(
                    "Numerical problem has not solved yet and results "
                    "cannot be exported.")
            else:
                self.core.cvxpy_endogenous_data_to_database(
                    scenarios_idx=scenarios_idx,
                    force_overwrite=force_overwrite,
                    suppress_warnings=suppress_warnings
                )

    def update_database_and_problem(self, force_overwrite: bool = False) -> None:
        """Update SQLite database with exogenous data and initialize problems.

        This method updates the SQLite database and initializes numerical problems. 
        To be used in case some changes in exogenous data have been made, so that 
        the SQLite database and the problems can be updated without re-generating the
        Model instance.

        Args:
            force_overwrite (bool, optional): Whether to overwrite/update 
                existing data without asking user permission. Defaults to False.
        """
        sqlite_db_file = Constants.ConfigFiles.SQLITE_DATABASE_FILE

        self.logger.info(
            f"Updating SQLite database '{sqlite_db_file}' "
            "and initialize problems.")

        self.load_exogenous_data_to_sqlite_database(force_overwrite)
        self.initialize_problems(force_overwrite)

    def reinitialize_sqlite_database(self, force_overwrite: bool = False) -> None:
        """Reinitialize SQLite database tables and reimport input data.

        This method reinitializes endogenous tables in SQLite database to Null 
        values, and reimports input data to exogenous tables.

        Args:
            force_overwrite (bool, optional): Whether to force overwrite 
                existing data. Used for testing purposes. Defaults to False.
        """
        sqlite_db_file = Constants.ConfigFiles.SQLITE_DATABASE_FILE

        self.logger.info(
            f"Reinitializing SQLite database '{sqlite_db_file}' "
            "endogenous tables.")

        self.core.database.reinit_sqlite_endogenous_tables(force_overwrite)
        self.load_exogenous_data_to_sqlite_database(force_overwrite)

    def check_model_results(
            self,
            numerical_tolerance: Optional[float] = None,
    ) -> None:
        """Compare model results with expected results.

        This method compares the results of the model SQLite database with results
        of another SQLite database. Mostly used for testing purposes.
        This method uses the 'check_results_as_expected' method to compare the 
        results of the current model's computations with the expected results. 
        The expected results are stored in a test database specified by the 
        'sqlite_database_file_test' setting and located in the model directory.

        Args:
            numerical_tolerance (float, optional): The relative difference 
                (non-percentage) tolerance for comparing numerical values in 
                different databases. If None, it is set to
                'Constants.NumericalSettings.TOLERANCE_TESTS_RESULTS_CHECK'.
        """
        if not numerical_tolerance:
            numerical_tolerance = \
                Constants.NumericalSettings.TOLERANCE_TESTS_RESULTS_CHECK

        with self.logger.log_timing(
            message=f"Check model results...",
            level='info',
        ):
            self.core.check_results_as_expected(
                values_relative_diff_tolerance=numerical_tolerance)

    def variable(
            self,
            name: str,
            problem_key: Optional[str | int] = None,
            scenario_key: Optional[int] = None,
    ) -> Optional[pd.DataFrame]:
        """Fetch variable data.

        This method fetches data for a specific variable. In case the model is 
        defined by multiple numerical problmes and for multiple scenarios (linear 
        combination of inter-problem sets), the related keys must be passed to
        univocally identify the values of the variable.
        Useful for inspecting variables data during model generation and debugging.

        Args:
            name (str): The name of the variable.
            problem_key (Optional[str | int], optional): The symbolic problem key. 
                Defaults to None.
            scenario_key (Optional[int], optional): The scenario index, corresponding
                to a problem identified by the linear combination of inter-problem
                sets. Defaults to None.

        Returns:
            Optional[pd.DataFrame]: The data for the specified variable.
        """
        return self.core.index.fetch_variable_data(
            var_key=name,
            problem_key=problem_key,
            scenario_key=scenario_key,
        )

    def set(self, name: str) -> Optional[pd.DataFrame]:
        """Fetch set data.

        Useful for inspecting variables data during model generation and debugging.

        Args:
            name (str): The name of the set.

        Returns:
            Optional[pd.DataFrame]: The data for the specified set.
        """
        return self.core.index.fetch_set_data(set_key=name)

    def __repr__(self):
        """Return a string representation of the Database instance."""
        class_name = type(self).__name__
        return f'{class_name}'
