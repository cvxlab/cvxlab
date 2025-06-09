""" 
constants.py

@author: Matteo V. Rocco
@institution: Politecnico di Milano

This module collects all the fundamental constants of the package, necessary 
for simplifying renaming package labels and for validation purposes.
The module also collects allowed operators and constants labels necessary for 
defining symbolic problem.
To avoid direct access and eventual unexpected modification of protected items 
may occur in other modules, constants are defined as class variables of the 
Constants class, accessible through the '__getattr__' getter method.

Classes:
    Constants: Centralized repository of constants grouped into meaningful
        categories for clarity and ease of access. Supports direct attribute
        access of constants using '__getattr__' method.
"""
from typing import Union
import cvxpy as cp
import numpy as np

from cvxlab.support import util_constants, util_operators


class Constants:
    """
    Centralized repository of constants grouped into meaningful categories for 
    clarity and ease of access. Supports direct attribute access of constants 
    using the '__getattr__' method.

    Subgroups:
        ConfigFiles: Constants related to configuration and file management.
        Labels: Standard headers and field names.
        DefaultStructures: Default structures for data validation.
        SymbolicDefinitions: Allowed constants and operators for symbolic 
            problem definitions.
        NumericalSettings: Settings for numerical solvers and tolerances.
        TextNotes: Text notes and messages for user.

    Usage:
        Direct access:
            >>> Constants.ConfigFiles.SETUP_FILES
    """

    _SUBGROUPS = []

    class ConfigFiles:
        """Constants related to configuration and file management."""
        SETUP_INFO = {
            0: 'structure_sets',
            1: 'structure_variables',
            2: 'problem'
        }
        SETUP_XLSX_FILE = 'model_settings.xlsx'
        SETS_FILE = 'sets.xlsx'
        AVAILABLE_SOURCES = ['yml', 'xlsx']
        INPUT_DATA_DIR = 'input_data'
        INPUT_DATA_FILE = 'input_data.xlsx'
        DATA_FILES_EXTENSION = '.xlsx'
        SQLITE_DATABASE_FILE = 'database.db'
        SQLITE_DATABASE_FILE_BKP = 'database_bkp.db'
        SQLITE_DATABASE_FILE_TEST = 'database_expected.db'
        TUTORIAL_FILE_NAME = 'API_usage_guide.ipynb'
        TUTORIALS_FILE_PATH = 'tutorials'
        TEMPLATES_DIR = 'default'
        INSTANCES_DIR = 'instances'

    class Labels:
        """Standard headers and field names."""
        NAME = 'name'
        FILTERS = 'filters'
        AGGREGATIONS = 'aggregations'
        CVXPY_VAR = 'variable'
        SUB_PROBLEM_KEY = 'sub_problem_key'
        FILTER_DICT_KEY = 'filter'
        PROBLEM = 'problem'
        SCENARIO_COORDINATES = 'info'
        PROBLEM_STATUS = 'status'
        OBJECTIVE = 'objective'
        EXPRESSIONS = 'expressions'

        COORDINATES_KEY = 'coordinates'
        VARIABLES_INFO_KEY = 'variables_info'
        VALUE_KEY = 'value'
        BLANK_FILL_KEY = 'blank_fill'

        GENERIC_FIELD_TYPE = 'TEXT'
        VALUES_FIELD = {'values': ['values', 'REAL']}
        ID_FIELD = {'id': ['id', 'INTEGER PRIMARY KEY']}

        SET_TABLE_NAME_PREFIX = '_set_'
        COLUMN_NAME_SUFFIX = '_Name'
        COLUMN_AGGREGATION_SUFFIX = '_agg_'

    class DefaultStructures:
        """Default structures for data validation and for generating templates."""
        OPTIONAL = object()
        ANY = object()

        SET_STRUCTURE = (
            # set name (case insensitive: 'e' and 'E' are the same set)
            'set_key:',
            {
                # metadata
                'description': (OPTIONAL, str),
                # in case the set defines independent numerical sub-problems
                'split_problem': (OPTIONAL, bool),
                # key of another set to copy the data from
                'copy_from': (OPTIONAL, str),
                # dictionary with keys as the filters name and values as the
                # list of filter values
                'filters': (OPTIONAL, {ANY: list}),
                # list of set aggregations (useful for visualization)
                'aggregations': (OPTIONAL, Union[int, str, list]),
            }
        )

        DATA_TABLE_STRUCTURE = (
            # data table name (case insensitive: 'e' and 'E' are the same table)
            'table_key:',
            {
                # metadata
                'description': (OPTIONAL, str),
                # ALLOWED_VARIABLES_TYPES (or dictionary with keys as problem
                # name and corresponding values as allowed types)
                'type': (str, dict),
                # if variables of the table are integers (default: False)
                'integer': (OPTIONAL, bool),
                # list of table coordinates (set_key symbols)
                'coordinates': (str, list),
                # definition of the variables based on the same data table
                'variables_info': {
                    # dictionary with keys as variables names and values as dict
                    # with variable info. Variables are case sensitive.
                    ANY: {
                        # ALLOWED_CONSTANTS (only for constants!)
                        'value': (OPTIONAL, str),
                        # numerical value that will be used to fill variables in
                        # case of blank or nan values
                        'blank_fill': (OPTIONAL, float),
                        # dictionary with keys as set_key symbols and values
                        # defining the dimension and filters for the set
                        ANY: (OPTIONAL, {
                            # ALLOWED_DIMENSIONS (included in 'coordinates')
                            'dim': (OPTIONAL, str),
                            # dictionary with keys as the filters key of the set
                            # and values as the list of values to filter
                            'filters': (OPTIONAL, dict),
                        })
                    }
                }
            }
        )

        PROBLEM_STRUCTURE = (
            # problem name defined in case of multiple problems
            'problem_key: # optional',
            {
                # Minimize() or Maximize() with an expression resulting in a scalar
                'objective': (OPTIONAL, list),
                # definition of additional expressions (equalities/inequalities)
                'expressions': list,
                # metadata
                'description': (OPTIONAL, list),
            }
        )

        XLSX_PIVOT_KEYS = {
            'structure_sets': ('set_key', None),
            'structure_variables': ('table_key', 'variables_info'),
            'problem': ('problem_key', None),
        }

        XLSX_TEMPLATE_COLUMNS = {
            'structure_sets': [
                'set_key',
                *SET_STRUCTURE[1].keys()
            ],
            'structure_variables': [
                'table_key',
                *DATA_TABLE_STRUCTURE[1].keys(),
                'value',
                'blank_fill',
                'set_keys ...'
            ],
            'problem': [
                'problem_key',
                *PROBLEM_STRUCTURE[1].keys()
            ],
        }

        ALLOWED_BOOL = {
            'true': True, 'True': True, 'TRUE': True,
            'false': False, 'False': False, 'FALSE': False,
        }

    class SymbolicDefinitions:
        """Allowed constants and operators for symbolic problem definitions."""
        TOKEN_PATTERNS = {
            'text': r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
            'numbers': r"\b(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?\b",
            'operators': [
                r"==", r">=", r"<=",
                r"\+", r"-", r"\*", r"/", r"@", f",",
            ],
            'parentheses': [r"\(", r"\)"],
        }

        NONE_SYMBOLS = [None, 'nan', 'None', 'null', '', [], {}]

        ALLOWED_DIMENSIONS = ['rows', 'cols', 'intra', 'inter']
        ALLOWED_VARIABLES_TYPES = ['constant', 'exogenous', 'endogenous']

        USER_DEFINED_CONSTANTS = {
            'sum_vector': (np.ones, {}),
            'identity': (np.eye, {}),
            'set_length': (np.max, {}),
            'arange_1': (util_constants.arange, {}),
            'arange_0': (util_constants.arange, {'start_from': 0}),
            'lower_triangular': (util_constants.tril, {}),
        }

        USER_DEFINED_OPERATORS = {
            'tran': cp.transpose,
            'diag': cp.diag,
            'sum': cp.sum,
            'mult': cp.multiply,
            'shift': util_operators.shift,
            'pow': util_operators.power,
            'minv': util_operators.matrix_inverse,
            'weib': util_operators.weibull_distribution,
            'annuity': util_operators.annuity,
            'Minimize': cp.Minimize,
            'Maximize': cp.Maximize,
        }

    class NumericalSettings:
        """Settings for numerical solvers and tolerances."""
        STD_VALUES_TYPE = float
        ALLOWED_VALUES_TYPES = (
            int, float, np.dtype('float64'), np.dtype('int64'))
        ALLOWED_TEXT_TYPE = str
        ALLOWED_SOLVERS = cp.installed_solvers()
        DEFAULT_SOLVER = 'GUROBI'
        TOLERANCE_TESTS_RESULTS_CHECK = 0.02
        TOLERANCE_MODEL_COUPLING_CONVERGENCE = 0.01
        MAXIMUM_ITERATIONS_MODEL_COUPLING = 20
        ROUNDING_DIGITS_RELATIVE_DIFFERENCE_DB = 5
        SPARSE_MATRIX_ZEROS_THRESHOLD = 0.3
        SQL_BATCH_SIZE = 1000

    class TextNotes:
        """Text notes and messages for user."""
        GENERIC_NOTE = ("")

    _SUBGROUPS = [
        ConfigFiles,
        Labels,
        DefaultStructures,
        SymbolicDefinitions,
        NumericalSettings,
        TextNotes,
    ]

    @classmethod
    def __getattr__(cls, name):
        """
        Provides direct access to constants by searching nested groups.

        Args:
            name (str): The name of the attribute to retrieve.

        Returns:
            Any: The requested constant or attribute.

        Raises:
            AttributeError: If the attribute is not found.
        """
        for subgroup in cls._SUBGROUPS:
            if hasattr(subgroup, name):
                return getattr(subgroup, name)
        raise AttributeError(
            f"Constant or group '{name}' not found in {cls.__name__}.")
