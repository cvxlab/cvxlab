"""
model.py 

@author: Matteo V. Rocco
@institution: Politecnico di Milano

This module defines the Model class, the main object of the CVXLab package.

The Model class gets the main user settings and data model path, and it provides
all the methods useful for the user to handle the model and its main 
functionalities.
The Model class integrates various components such as logging, file management,
and core functionalities, ensuring a cohesive workflow from numerical problem
conceptualization, database generation and data input, numerical problem generation
and solution, results export to database.
The Model class embeds the generation of the Core class, which provides 
functionalities for SQLite database management, problem formulation and solution
through CVXPY. 

The primary focus of this module is to streamline operations across database 
interactions, data file management, numerical problem formulation, making it 
suitable for applications in scientific computing, economic modeling, or any 
domain requiring robust data analysis and optimization capabilities.

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
    """
    Class representing a modeling environment that handles SQLite data 
    generation and processing, database interactions, numerical optimization 
    model generation and handling with CVXPY. 

    This class initializes with a configuration for managing directories, 
    logging, and file management for a specific model. It also sets up various
    components including a logger, file manager, and core functionalities.

    Attributes:
        logger (Logger): An instance of Logger to handle logging across the class.
        files (FileManager): An instance of FileManager to manage file operations.
        settings (DotDict): A dictionary-like object storing configurations such as 
            model name, file paths, and operational flags.
        paths (DotDict): A dictionary-like object storing the paths for model 
            directories and associated files.
        core (Core): An instance of Core that manages the core functionality 
            of the model.

    Parameters of settings attribute:
        model_dir_name (str): Name of the directory for the model (and name of 
            the model itself).
        main_dir_path (str): Path to the main directory where the model 
            directory will be located.
        model_settings_from (Literal['yml', 'xlsx']): Format of the model 
            settings file.
        use_existing_data (bool, optional): Flag to indicate whether to use 
            existing data files and SQLite database. Defaults to False.
        multiple_input_files (bool, optional): Flag to indicate whether 
            multiple input files are expected. Defaults to False.
        log_level (Literal['info', 'debug', 'warning', 'error'], optional): 
            Determines the logging level. Defaults to 'info'.
        log_format (Literal['standard', 'minimal'], optional): Specifies the 
            format of the logs. Defaults to 'minimal'.
        detailed_validation (bool, optional): Flag to indicate whether to 
            perform detailed validation logging at the end of the analysis of 
            the model formulation. Defaults to False.

    Raises:
        SettingsError: If any critical configurations are invalid or not found.
        FileNotFoundError: If necessary files are not found in the specified paths.
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
    ) -> None:

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
        """
        Returns a list of sets names available in the model, that can be 
        interpreted as the 'coordinates' of the model.

        Returns:
            List[str]: A list of set names.
        """
        return self.core.index.list_sets

    @property
    def data_tables(self) -> List[str]:
        """
        Returns a list of data tables names available in the model, from where
        all the problems variables are defined.

        Returns:
            List[str]: A list of data table names.
        """
        return self.core.index.list_data_tables

    @property
    def variables(self) -> Dict[str, List[str]]:
        """
        Returns a dictionary of variables, where keys represent variable types 
        (endogenous, exogenous, constants) and values are lists of related 
        variables keys.

        Returns:
            Dict[str, List[str]]: A dictionary of variable types and related 
            variables keys.
        """
        return self.core.index.list_variables

    @property
    def is_problem_solved(self) -> bool:
        """
        Checks if the numerical problem has been solved (even if it has not 
        found a numerical solution).

        Returns:
            bool: True if the problem has been solved, False otherwise.
        """
        if self.core.problem.problem_status is None:
            return False
        else:
            return True

    def __repr__(self):
        """
        Returns a string representation of the Model instance.

        Returns:
            str: The class name of the Model instance.
        """
        class_name = type(self).__name__
        return f'{class_name}'

    def check_model_dir(self) -> None:
        """
        Validates the existence of the model directory and required setup files.
        This method checks if the model directory and all the required setup 
        files exist based on the 'model_settings_from' setting. It uses the 
        'dir_files_check' method from the 'files' object to perform the check.

        Raises:
            SettingsError: If the 'model_settings_from' parameter is not recognized.
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

    def load_model_coordinates(
            self,
            fetch_foreign_keys: bool = True,
    ) -> None:
        """
        Loads sets data and variable coordinates to the Model.Index.
        If the 'use_existing_data' setting is True, it loads existing sets 
        data and variable coordinates provided by SQLite database.
        Otherwise, it loads new sets data and variable coordinates to 
        Model.Index.
        Based on Model settings, SQLite tables foreign keys can be enabled.

        Raises:
            FileNotFoundError: If the sets_xlsx_file specified in the 
            settings is missing and 'use_existing_data' is True.

        Return:
            None
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
            self.core.index.fetch_scenarios_info()

            if fetch_foreign_keys:
                self.core.index.fetch_foreign_keys_to_data_tables()

    def initialize_blank_data_structure(self) -> None:
        """
        Initializes the blank data structure for the model:
            - Creates a blank SQLite database with set tables and data tables.
            - Fills the SQLite tables with sets information.
            - Creates blank Excel input data files.

        If the SQLite database already exists, it gives the option to erase it 
        and generate a new one, or to work with the existing SQLite database.
        Same for the input data directory.
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

    def generate_input_data_files(
            self,
            table_key_list: List[str] = [],
    ) -> None:
        """
        Generates only one or more input data files for the model.
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
        """
        Loads input (exogenous) data to the SQLite database. 

        Args:
            force_overwrite (bool, optional): Whether to force overwrite existing 
                data without asking for user permission. Defaults to False.
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
        """
        Initializes numerical problems in the Model instance. Specifically, the
        method initializes variables, feeds data to exogenous variables, and
        generates numerical problems based on the symbolic formulation.

        Args:
            force_overwrite (bool, optional): If True, forces the overwrite 
                of existing numerical problems without asking for user 
                permission. Used for testing purposes. Defaults to False.
            allow_none_values (bool, optional): If True, allows None values in
                the exogenous data. Defaults to True.

        Return:
            None
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
        """
        Solves numerical problems defined by the model instance.

        Parameters:
            verbose (bool, optional): If True, prints verbose output during the 
                model run. Defaults to False.
            force_overwrite (bool, optional): If True, overwrites existing results. 
                Defaults to False.
            integrated_problems (bool, optional): If True, solves problems in 
                an integrated manner. Defaults to False.
            solver (str, optional): The solver to use for solving numerical 
                problems. Defaults to None, in which case the default solver 
                specified in Constants is used.
            numerical_tolerance (float, optional): The numerical tolerance for 
                the solver. Defaults to None.
            maximum_iterations (int, optional): The maximum number of iterations 
                for solving integrated problems. Defaults to None.
            **kwargs: Additional keyword arguments to be passed to the solver.

        Raises:
            SettingsError: If the specified solver is not supported by the 
                current CVXPY version.
            OperationalError: If no numerical problems are found.
            SettingsError: If integrated problems are requested but only one 
                problem is found.

        Returns:
            None
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
            raise exc.OperationalError(msg)

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
        """
        Loads the endogenous model results to a SQLite database. 

        Args:
            force_overwrite (bool, optional): Whether to overwrite/update 
                existing data without asking user permission. Defaults to False.
            suppress_warnings (bool, optional): Whether to suppress warnings 
                during the data loading process. Defaults to False.

        Returns:
            None
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

    def update_database_and_problem(
            self,
            force_overwrite: bool = False,
    ) -> None:
        """
        Updates the SQLite database and initializes problems. To be used in 
        case some changes in exogenous data have been made, so that the SQLite 
        database and the problems can be updated without re-generating the
        Model instance.

        Args:
            force_overwrite (bool, optional): Whether to overwrite/update 
                existing data without asking user permission. Defaults to False.

        Returns:
            None
        """
        sqlite_db_file = Constants.ConfigFiles.SQLITE_DATABASE_FILE

        self.logger.info(
            f"Updating SQLite database '{sqlite_db_file}' "
            "and initialize problems.")

        self.load_exogenous_data_to_sqlite_database(force_overwrite)
        self.initialize_problems(force_overwrite)

    def reinitialize_sqlite_database(
            self,
            force_overwrite: bool = False,
    ) -> None:
        """
        Initializes endogenous tables in SQLite database to Null values, and
        reimports input data to exogenous tables.

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
        """
        Checks the results of the model's computations. This is mainly called
        for testing purposes.

        This method uses the 'check_results_as_expected' method to compare the 
        results of the current model's computations with the expected results. 
        The expected results are stored in a test database specified by the 
        'sqlite_database_file_test' setting and located in the model directory.

        Args:
            numerical_tolerance (float, optional): The relative difference 
                (non-percentage) tolerance for comparing numerical values in 
                different databases.

        Raises:
            OperationalError: If the connection or cursor of the database to be 
                checked are not initialized.
            ModelFolderError: If the test database does not exist or is not 
                correctly named.
            ResultsError: If the databases are not identical in terms of table 
                presence, structure, or contents.
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
            problem_key: Optional[int] = None,
            sub_problem_key: Optional[int] = None,
    ) -> Optional[pd.DataFrame]:
        """
        Fetches data for a specific variable.

        Args:
            name (str): The name of the variable.
            problem_key (int, optional): The problem index. Defaults to None.
            sub_problem_key (int, optional): The sub-problem index. Defaults 
                to None.

        Returns:
            Optional[pd.DataFrame]: The data for the specified variable.
        """
        return self.core.index.fetch_variable_data(
            var_key=name,
            problem_index=problem_key,
            sub_problem_index=sub_problem_key,
        )

    def set(self, name: str) -> Optional[pd.DataFrame]:
        """
        Fetches data for a specific set.

        Args:
            name (str): The name of the set.

        Returns:
            Optional[pd.DataFrame]: The data for the specified set.
        """
        return self.core.index.fetch_set_data(set_key=name)
