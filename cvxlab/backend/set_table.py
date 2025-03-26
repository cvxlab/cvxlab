"""
set_table.py 

@author: Matteo V. Rocco
@institution: Politecnico di Milano

This module provides the SetTable class for handling and manipulating data sets 
in a structured format. It allows for managing data sets with detailed logging 
and interaction with a SQLite database. The SetTable class integrates with 
pandas for data manipulation, providing tools to fetch, update, and manage 
data efficiently.
"""

from typing import Any, Dict, Iterator, List, Optional, Tuple
import pandas as pd

from cvxlab.constants import Constants
from cvxlab.log_exc.logger import Logger


class SetTable:
    """
    A class to represent and manipulate data sets with specific attributes and 
    methods. This class encapsulates operations related to data sets such as 
    fetching headers, filters, and maintaining data integrity. It interfaces 
    with a logger to log activities and a DataFrame to handle the data.

    Args:
        logger (Logger): An instance of the Logger class used for logging 
            activities.
        data (pd.DataFrame, optional): A pandas DataFrame containing the initial 
            set data. Defaults to None.
        **kwargs: Arbitrary keyword arguments defining attributes of the set like 
            symbols, table names, etc.

    Attributes:
        logger (Logger): An instance for logging.
        symbol (str): The symbol representing the set.
        table_name (str): The name of the associated SQLite table.
        copy_from (str): The name of the set table the values of which are 
            copied from (this avoid replicating identical set tables in excel 
            input files).
        table_structure (Dict[str, Any]): Structure of the SQLite table used 
            for data handling.
        table_headers (Dict[str, Any]): Headers of the SQLite table, fetched 
            based on the table structure.
        table_filters (Dict[int, Any]): Filters applicable to the table, 
            derived from the table structure.
        set_categories (Dict[str, Any]): Categories applicable to the set.
        split_problem (bool): Indicates whether the set defines multiple 
            numerical problems. Defaults to False.
        data (pd.DataFrame): The DataFrame containing the set's data.

    Methods:
        set_name_header: Returns the standard name header from the table headers.
        set_aggregation_header: Returns the aggregation header from the table 
            headers.
        set_excel_file_headers: List of headers formatted for Excel files.
        set_filters_dict: Dictionary representing filters with headers as keys 
            and filter values as lists.
        set_filters_headers: Dictionary of filter indices and their corresponding 
            headers.
        set_items: List of items in the set from the DataFrame based on the name 
            header.
        fetching_headers_and_filters: Fetches and constructs headers and filters 
            from the table structure.
    """

    def __init__(
            self,
            logger: Logger,
            key_name: str,
            **set_info,
    ) -> None:

        self.logger = logger.get_child(__name__)

        self.name: Optional[str] = None
        self.table_name: Optional[str] = None

        self.split_problem: bool = False
        self.description: Optional[str] = None
        self.copy_from: Optional[str] = None

        self.table_structure: Dict[str, Any] = {}
        self.table_headers: Dict[str, List[str]] = {}
        self.table_filters: Dict[int, Any] = {}
        self.set_categories: Dict[str, Any] = {}
        self.data: Optional[pd.DataFrame] = None

        self.fetch_names(key_name)
        self.fetch_attributes(set_info)
        self.fetch_headers_and_filters()

    @property
    def set_name_header(self) -> str | None:
        """
        Retrieves the standard name header from the table headers based on the 
        configuration constants.

        Returns:
            str | None: The standard name header if available, otherwise None.
        """
        if self.table_headers is not None:
            return self.table_headers[Constants.Labels.NAME][0]
        return None

    @property
    def set_aggregation_header(self) -> str | None:
        """
        Retrieves the aggregation header from the table headers, used for data 
        aggregation operations.

        Returns:
            str | None: The aggregation header if defined in the table headers, 
                otherwise None.
        """
        if self.table_headers is not None:
            aggregation_key = Constants.Labels.AGGREGATION

            if aggregation_key in self.table_headers:
                return self.table_headers[aggregation_key][0]
        return None

    @property
    def set_excel_file_headers(self) -> List | None:
        """
        Provides a list of headers formatted for use in Excel files. This list 
        includes only the primary header from each table header set.

        Returns:
            List[str] | None: A list of headers suitable for Excel, or None if 
                no headers are defined.
        """
        if self.table_headers is not None:
            return [
                item[0] for item in list(self.table_headers.values())
            ]
        return None

    @property
    def set_filters_dict(self) -> Dict[str, List[str]] | None:
        """
        Constructs a dictionary of filter headers with their corresponding 
        filter values. Each entry represents a filterable attribute of the data.

        Returns:
            Dict[str, List[str]] | None: A dictionary where keys are filter 
                headers and values are lists of filter criteria, or None if 
                no filters are set.
        """
        if self.table_filters:
            return {
                filter_items['header']: filter_items['values']
                for filter_items in self.table_filters.values()
            }
        return None

    @property
    def set_filters_headers(self) -> Dict[int, str] | None:
        """
        Provides a mapping from filter index to their corresponding headers. 
        Useful for identifying filters by index.

        Returns:
            Dict[int, str] | None: A dictionary mapping filter indices to their 
                headers, or None if no filters are defined.
        """
        if self.table_filters:
            return {
                key: value['header']
                for key, value in self.table_filters.items()
            }
        return None

    @property
    def set_items(self) -> List[str] | None:
        """
        Generates a list of items in the data set based on the standard name 
        header.

        Returns:
            List[str] | None: A list of item names from the data set, or None 
                if the data is empty or the name header is undefined.
        """
        if self.data is not None:
            return list(self.data[self.set_name_header])
        return None

    def fetch_names(self, set_key: str) -> None:
        prefix = Constants.Labels.SET_TABLE_NAME_PREFIX
        self.name = set_key
        self.table_name = prefix+set_key.upper()

    def fetch_attributes(self, set_info: dict) -> None:

        col_name_suffix = Constants.Labels.COLUMN_NAME_SUFFIX
        col_agg_suffix = Constants.Labels.COLUMN_AGGREGATION_SUFFIX
        filters_header = Constants.Labels.FILTERS
        name_header = Constants.Labels.NAME
        aggregation_header = Constants.Labels.AGGREGATION

        for key, value in set_info.items():
            if key != filters_header and value is not None:
                setattr(self, key, value)

        self.table_structure[name_header] = self.name + col_name_suffix

        if not self.split_problem:
            self.table_structure[aggregation_header] = \
                self.name + col_agg_suffix

        if filters_header in set_info:
            self.table_structure[filters_header] = {}
            filters_info: dict = set_info[filters_header]

            if filters_info:
                for filter_key, filter_values in filters_info.items():
                    self.table_structure[filters_header][filter_key] = {
                        'header': self.name + '_' + filter_key,
                        'values': filter_values
                    }

    def fetch_headers_and_filters(self) -> None:
        """
        Fetches and initializes the table headers and filters based on the 
        predefined table structure. This method updates the instance's 
        table_headers and table_filters attributes based on constants.
        This setup process includes extracting specific headers for name, 
        filters, and aggregation from the table's structural definition, and 
        setting them up for easy access throughout the class's methods.

        Side Effects:
            Modifies the table_headers and table_filters attributes of the instance.
        """
        name_key = Constants.Labels.NAME
        filters_key = Constants.Labels.FILTERS
        aggregation_key = Constants.Labels.AGGREGATION
        generic_field_type = Constants.Labels.GENERIC_FIELD_TYPE

        # Fetching filters
        self.table_filters = self.table_structure.get(filters_key, None)

        # Fetching table headers
        name_header = self.table_structure.get(name_key, None)
        aggregation_header = self.table_structure.get(
            aggregation_key, None)

        filters_headers = {
            'filter_' + str(key): value['header']
            for key, value in self.table_structure.get(filters_key, {}).items()
        }

        self.table_headers = {
            key: [value, generic_field_type]
            for key, value in {name_key: name_header, **filters_headers}.items()
        }

        if aggregation_header:
            self.table_headers[aggregation_key] = [
                aggregation_header, generic_field_type
            ]

    def __repr__(self) -> str:
        output = ''
        for key, value in self.__dict__.items():
            if key in ('data', 'logger'):
                pass
            elif key != 'values':
                output += f'\n{key}: {value}'
            else:
                output += f'\n{key}: \n{value}'
        return output

    def __iter__(self) -> Iterator[Tuple[Any, Any]]:
        for key, value in self.__dict__.items():
            if key not in ('data', 'logger'):
                yield key, value
