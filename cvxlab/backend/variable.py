"""Module defining the Variable class.

The Variable class manages the characteristics and behaviors of variables used 
in optimization models. It facilitates operations such as defining constants, 
reshaping data, and interfacing with SQL database tables for data manipulation.
The class incorporates functionality to handle complex variable structures 
that may include dimensions, mapping of related tables, and operations that 
convert SQL data to formats usable by optimization tools like cvxpy.
"""
from typing import Any, Dict, Iterator, List, Optional, Tuple

import cvxpy as cp
import pandas as pd

from cvxlab.defaults import Defaults
from cvxlab.log_exc import exceptions as exc
from cvxlab.log_exc.logger import Logger
from cvxlab.support import util


class Variable:
    """Manages the operations of variables used in optimization models.

    Attributes:

    - logger (Logger): Logger object for logging information, warnings, and errors.
    - symbol (Optional[str]): The symbolic name of the variable.
    - type (Optional[str]): The type of the variable (available types defined 
        in Defaults.SymbolicDefinitions.VARIABLE_TYPES).
    - rows (Dict[str, Any]): Information about the rows dimension of the variable.
    - cols (Dict[str, Any]): Information about the columns dimension of the variable.
    - value (Optional[str]): Value type of the variable, only defined in case 
        of Defaults (e.g. identity matrix, ...).
    - blank_fill (Optional[float]): Value to fill in case of missing data. Only 
        defined for exogenous variables, reducing effort in inserting numerical 
        data by the user.
    - related_table (Optional[str]): The database table that collect the subset
        numerical data associated to the variable.
    - var_info (Optional[Dict[str, Any]]): Raw information about the variable
        fetched from the model setup file/s.
    - coordinates_info (Dict[str, Any]): Maps the basic information about the 
        variable coordinates, including sets defining variable shapes (rows, cols), 
        inter-problem and intra-problem dimensions. Basic information includes
        the set names and the related database table headers.
    - coordinates (Dict[str, Any]): Mapping specific coordinates values to the 
        corresponding variable dimensions (rows, cols), inter-problem and
        intra-problem sets, including set key and related values.
    - data (Optional[pd.DataFrame]): Defines dataframe (or a dictionary of 
        dataframes in case the variable is of multiple types) identifying 
        information about data associated to the variable. Specifically, the 
        dataframe includes the number of scenarios (linear combination of 
        inter-problem sets, if any), the cvxpy variables, the associated filters
        (identifying the related variable data in data tables), and the key of
        the related numerical problem.

    """

    def __init__(
            self,
            logger: Logger,
            **variable_info,
    ):
        """Initialize a new instance of the Variable class.

        This constructor initializes a Variable object with various attributes
        that define its properties and behavior provided by the 'variable_info'
        dictionary. Such attributes are fetched and rearranged based on the 
        'fetch_attributes' and 'rearrange_var_info' methods.

        Args:
            logger (Logger): Logger object for logging operations within the class.
            **variable_info: Keyword arguments defining variable features.
        """
        self.logger = logger.get_child(__name__)

        self.symbol: Optional[str] = None
        self.type: Optional[str] = None
        self.rows: Dict[str, Any] = {}
        self.cols: Dict[str, Any] = {}
        self.value: Optional[str] = None
        self.blank_fill: Optional[float] = None
        self.related_table: Optional[str] = None
        self.var_info: Optional[Dict[str, Any]] = None

        self.fetch_attributes(variable_info)
        self.rearrange_var_info()

        self.coordinates_info: Dict[str, Any] = {}
        self.coordinates: Dict[str, Any] = {}
        self.data: Optional[pd.DataFrame | dict] = None

    def fetch_attributes(self, variable_info: Dict[str, Any]) -> None:
        """Fetch and set attributes from the provided variable information.

        This method iterates over the provided dictionary of variable attributes
        and sets the corresponding attributes of the Variable instance if they
        are not None. This method is called upon initialization of the Variable class.

        Args:
            variable_info (Dict[str, Any]): Dictionary containing variable attributes.
        """
        for key, value in variable_info.items():
            if value is not None:
                setattr(self, key, value)

    def rearrange_var_info(self) -> None:
        """Rearrange the raw information provided by var_info.

        This method takes the raw variable attributes and rearrange the information
        in the variable instance attributes. This method is called upon initialization 
        of the Variable class.
        """
        value_key = Defaults.Labels.VALUE_KEY
        blank_fill_key = Defaults.Labels.BLANK_FILL_KEY
        filter_key = Defaults.Labels.FILTERS
        set_key = Defaults.Labels.SET
        dim_key = Defaults.Labels.DIM
        allowed_constants = Defaults.SymbolicDefinitions.ALLOWED_CONSTANTS
        dimensions = Defaults.SymbolicDefinitions.DIMENSIONS

        if self.var_info is None:
            return

        constant_value = self.var_info.get(value_key, None)
        if constant_value and constant_value in allowed_constants:
            self.value = constant_value

        blank_fill_value = self.var_info.get(blank_fill_key, None)
        if blank_fill_value is not None and \
                isinstance(blank_fill_value, (int, float)):
            self.blank_fill = blank_fill_value

        for dimension in [dimensions['ROWS'], dimensions['COLS']]:
            shape_set = util.fetch_dict_primary_key(
                dictionary=self.var_info,
                second_level_key=dim_key,
                second_level_value=dimension,
            )
            dim_info_yml: dict | None = self.var_info.get(shape_set, None)
            if not dim_info_yml:
                continue

            dim_info = {
                set_key: shape_set,
                filter_key: dim_info_yml.get(filter_key, None),
            }

            if dimension == dimensions['ROWS']:
                self.rows = dim_info
            elif dimension == dimensions['COLS']:
                self.cols = dim_info

    @property
    def shape_sets(self) -> List[str | int]:
        """Return the sets defining the shape of the variable (rows, cols).

        Returns:
            List[Union[str, int]]: A list containing set identifiers or 
                rows and cols of the variable. In of a monodimensional variable,
                the missing dimension is represented by 1.
        """
        set_key = Defaults.Labels.SET

        if self.rows is None and self.cols is None:
            return []

        rows_shape = self.rows.get(set_key, 1)
        cols_shape = self.cols.get(set_key, 1)
        return [rows_shape, cols_shape]

    @property
    def intra_sets(self) -> List[str]:
        """Return a list of intra-problem sets of the variable.

        Returns:
            List[Union[str, int]]: A list containing the intra-problem sets keys.
        """
        intra_dim_key = Defaults.SymbolicDefinitions.DIMENSIONS['INTRA']

        if self.coordinates_info[intra_dim_key] is None:
            return []

        return list(self.coordinates_info[intra_dim_key].keys())

    @property
    def shape_size(self) -> Tuple[int]:
        """Return the rows-cols dimension size of the variable.

        Computes and returns the size of each dimension in the variable. 
        This is useful for determining the dimensionality of the data associated 
        with the variable. If a dimension is not defined, it is considered to have
        a size of 1.

        Returns:
            Tuple[int]: A tuple containing the size of each dimension.
        """
        dimensions = Defaults.SymbolicDefinitions.DIMENSIONS

        if not self.coordinates:
            return ()

        shape_size = []

        for dimension in [dimensions['ROWS'], dimensions['COLS']]:
            if self.coordinates[dimension]:
                shape_size.append(len(*self.coordinates[dimension].values()))
            else:
                shape_size.append(1)

        return tuple(shape_size)

    @property
    def dims_labels(self) -> List[Optional[str]]:
        """Return the tables headers defining the variable dimensions.

        This property retrieves the name labels for each dimension of the variable, 
        typically used for identifying matrix dimensions.

        Returns:
            List[str]: A list containing labels for each dimension of the variable.
        """
        dimensions = Defaults.SymbolicDefinitions.DIMENSIONS

        if not self.coordinates_info:
            return []

        return [
            next(iter(self.coordinates_info[dim].values()), None)
            if self.coordinates_info[dim] else None
            for dim in [dimensions['ROWS'], dimensions['COLS']]
        ]

    @property
    def dims_items(self) -> List[Optional[List[str]]]:
        """Return the list of items in each dimension of the variable.

        This property retrieves the items for each dimension of the variable 
        (rows, cols), returning a list of two lists including them.

        Returns:
            List[List[str]]: Lists of items for each dimension.
        """
        dimensions = Defaults.SymbolicDefinitions.DIMENSIONS

        if not self.coordinates:
            return []

        return [
            list(*self.coordinates[dim].values())
            if self.coordinates[dim] else None
            for dim in [dimensions['ROWS'], dimensions['COLS']]
        ]

    @property
    def dims_labels_items(self) -> Dict[str, List[str]]:
        """Return a dictionary combining dimension labels and items.

        This property returns a dictionary of keys as labels of the set dimensions
        and values as the related list of items. 

        Returns:
            Dict[str, List[str]]: Dictionary with dimension labels as keys and 
            the corresponding items as values.
        """
        return {
            self.dims_labels[dim]: self.dims_items[dim]
            for dim in [0, 1]
        }

    @property
    def dims_sets(self) -> Dict[str, str]:
        """Return a dictionary associating variable dimension with set key.

        Returns:
            Dict[str]: A dictionary containing dimension name as keys and 
                corresponding set name as values.
        """
        dimensions = Defaults.SymbolicDefinitions.DIMENSIONS

        if not self.coordinates_info:
            return []

        dims_sets = {}

        for dim in [dimensions['ROWS'], dimensions['COLS']]:
            if dim in self.coordinates_info:
                dim_set: dict = self.coordinates_info[dim]

                if dim_set:
                    dims_sets[dim] = next(iter(dim_set.keys()), None)
                else:
                    dims_sets[dim] = None

        return dims_sets

    @property
    def is_square(self) -> bool:
        """Return True if the variable matrix is square.

        Returns:
            bool: True if the variable matrix is square, False otherwise.
        """
        if len(self.shape_sets) != 2:
            return False

        if len(self.shape_size) == 2 and \
                self.shape_size[0] == self.shape_size[1]:
            return True
        else:
            return False

    @property
    def is_vector(self) -> bool:
        """Return True if the variable is a vector.

        Returns:
            bool: True if the variable is a vector, False otherwise.
        """
        if len(self.shape_size) == 1 or 1 in self.shape_size:
            return True
        return False

    @property
    def sets_parsing_hierarchy(self) -> Dict[str, str]:
        """Return a dictionary representing the hierarchy of variable dimensions.

        Retrieves the hierarchical structure of sets parsing for the variable,
        specifically related to inter-problem and intra-problem sets.

        Returns:
            Dict[str, str]: Dictionary representing the hierarchy of sets parsing.
        """
        dimensions = Defaults.SymbolicDefinitions.DIMENSIONS

        if not self.coordinates_info:
            self.logger.warning(
                f"Coordinates_info not defined for variable '{self.symbol}'.")
            return []

        return {
            **self.coordinates_info[dimensions['INTER']],
            **self.coordinates_info[dimensions['INTRA']],
        }

    @property
    def sets_parsing_hierarchy_values(self) -> Dict[str, str]:
        """Return a dictionary representing the hierarchy of variable dimensions with items.

        Retrieves the hierarchical structure of sets parsing for the variable,
        specifically related to inter-problem and intra-problem sets. Reports the
        actual items of the sets, instead of the set names.

        Returns:
            Dict[str, str]: Dictionary with parsing hierarchy keys and the related
                list of items as values.
        """
        dimensions = Defaults.SymbolicDefinitions.DIMENSIONS

        if not self.coordinates_info:
            self.logger.warning(
                f"Coordinates_info not defined for variable '{self.symbol}'.")
            return []

        return {
            **self.coordinates[dimensions['INTRA']],
            **self.coordinates[dimensions['INTER']],
        }

    @property
    def all_coordinates(self) -> Dict[str, List[str] | None]:
        """Return a dictionary of all coordinates key-values related to the variable.

        The property returns a dictionary with keys as set keys and values the 
        related set items, for all dimensions of the variable. 
        In case a variable has the same coordinates in different dimensions, 
        only one of them is reported. This occurs in case a variable has rows and
        columns defined by the same set.

        Returns:
            Dict[str, List[str] | None]: Dictionary containing coordinates keys
                and related items.
        """
        if not self.coordinates_info:
            self.logger.warning(
                f"Coordinates not defined for variable '{self.symbol}'.")
            return []

        all_coordinates = {}
        for coordinates in self.coordinates.values():
            all_coordinates.update(coordinates)
        return all_coordinates

    @property
    def all_coordinates_w_headers(self) -> Dict[str, List[str] | None]:
        """Return a dictionary of all coordinates headers-values related to the variable.

        The property returns a dictionary with keys as set name headers and values 
        the related set items, for all dimensions of the variable. 
        In case a variable has the same coordinates in different dimensions, 
        only one of them is reported. This occurs in case a variable has rows and
        columns defined by the same set.

        Returns:
            Dict[str, List[str] | None]: Dictionary containing coordinates name
                headers and and related items as values.
        """
        if not self.coordinates_info:
            self.logger.warning(
                f"Coordinates not defined for variable '{self.symbol}'.")
            return []

        if not self.coordinates:
            self.logger.warning(
                f"Coordinates not defined for variable '{self.symbol}'.")
            return []

        all_coords_w_headers = {}
        for category in Defaults.SymbolicDefinitions.DIMENSIONS.values():
            coords_info = self.coordinates_info.get(category, {})
            coords = self.coordinates.get(category, {})

            for key, table_header in coords_info.items():
                table_values = coords.get(key, [])

                if table_header in all_coords_w_headers:
                    all_coords_w_headers[table_header].extend(table_values)
                else:
                    all_coords_w_headers[table_header] = table_values

        # remove duplicates
        for key in all_coords_w_headers:
            all_coords_w_headers[key] = list(
                dict.fromkeys(all_coords_w_headers[key])
            )

        return all_coords_w_headers

    def none_data_coordinates(self, row: int) -> Dict[str, Any] | None:
        """Return coordinates of None data values in cvxpy variables.

        This method checks if there are None data values in the cvxpy variables 
        and returns the related coordinates (rows in Variable.data and related 
        hierarchy coordinates).

        Args:
            row (int): Identifies the row of Variable.data item (i.e., one 
                specific cvxpy variable).

        Returns:
            Optional[Dict[str, Any]]: Dictionary with keys being the rows where 
                cvxpy variable values are None and values being the names of 
                the sets that identify the variable. Returns None if all data 
                is present.

        Raises:
            ValueError: If the data attribute is not initialized correctly or
                the cxvpy variable header is missing.
            KeyError: If the passed row number is out of bounds.
        """
        cvxpy_var_header = Defaults.Labels.CVXPY_VAR

        if self.data is None \
                or not isinstance(self.data, pd.DataFrame) \
                or cvxpy_var_header not in self.data.columns:
            msg = "Data is not initialized correctly or CVXPY variable header is missing."
            self.logger.error(msg)
            raise ValueError(msg)

        if row < 0 or row > len(self.data):
            msg = f"Passed row number out of bound for variable " \
                f"table '{self.related_table}'. Valid rows between " \
                f"0 and {len(self.data)}."
            self.logger.error(msg)
            raise KeyError(msg)

        cvxpy_var: cp.Variable | cp.Parameter | cp.Constant = \
            self.data.at[row, cvxpy_var_header]

        if cvxpy_var.value is None:
            return {
                key: self.data.loc[row, value]
                for key, value in self.sets_parsing_hierarchy.items()
            }

        return None

    def reshaping_sqlite_table_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Reshape SQLite table data to match cvxpy variable shape.

        This method takes a Dataframe with data fetched from SQLite database variable
        table, and elaborate it to get the shape required by the cvxpy variable 
        (two-dimensions matrix).

        Args:
            data (pd.DataFrame): data filtered from the SQLite variable table,
            related to a unique cvxpy variable.

        Returns:
            pd.DataFrame: data reshaped and pivoted to be used as cvxpy values.
        """
        values_header = Defaults.Labels.VALUES_FIELD['values'][0]

        index_label, columns_label = self.dims_labels
        index_items, columns_items = self.dims_items

        # case of a scalar with no rows/cols labels (scalars)
        if all(item is None for item in self.dims_labels):
            index_label = ''

        pivoted_data = data.pivot_table(
            index=index_label,
            columns=columns_label,
            values=values_header,
            aggfunc='first'
        )

        # ensure matching data types for reindexing
        if columns_items is not None:
            columns_items = [
                type(pivoted_data.columns[0])(item) for item in columns_items
            ]

        if index_items is not None:
            index_items = [
                type(pivoted_data.index[0])(item) for item in index_items
            ]

        # Reindex to ensure the correct order of the data
        pivoted_data = pivoted_data.reindex(
            index=index_items,
            columns=columns_items,
        )

        return pivoted_data

    def define_constant(self, value_type: str) -> None:
        """Define values of a constant of a specific user-defined types.

        This method validates the provided value type against a set of allowed 
        values. Depending on the value type, the method either creates a constant 
        of the specified type or raises an error if the value type is not supported.

        NOTICE THAT the constant creation receives as argument the variable shape 
        size only. More complex constants may require additional arguments, which can be 
        added in future developments.

        Args:
            value_type (str): The type of the constant to be created. User-defined 
            constants are defined in util_constants module and registered in
            Defaults.SymbolicDefinitions.ALLOWED_CONSTANTS.

        Raises:
            exc.SettingsError: If the provided value type is not supported.
        """
        allowed_constants = Defaults.SymbolicDefinitions.ALLOWED_CONSTANTS

        factory_function = allowed_constants[value_type]

        if value_type not in allowed_constants:
            msg = f"Constant definition | type: '{value_type}' not supported. " \
                f"Supported value types: {allowed_constants.keys()}"
            self.logger.error(msg)
            raise exc.SettingsError(msg)

        return factory_function(self.shape_size)

    def __repr__(self) -> str:
        """Provide a string representation of the Variable object."""
        excluded_keys = ['data', 'logger', 'var_info']

        output = ''
        for key, value in self.__dict__.items():
            if key not in excluded_keys:
                output += f'\n{key}: {value}'
        return output

    def __iter__(self) -> Iterator[Tuple[Any, Any]]:
        """Iterate over the instance's attributes, excluding data and logger."""
        for key, value in self.__dict__.items():
            if key not in ('data', 'logger'):
                yield key, value
