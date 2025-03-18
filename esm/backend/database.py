"""
database.py

@author: Matteo V. Rocco
@institution: Politecnico di Milano

This module provides the Database class which handles all interactions with the 
database and file management for a modeling application. It includes functionalities 
for creating and manipulating database tables, handling data input/output 
operations, and managing data files for a modeling system.
The Database class encapsulates methods for creating blank database tables, 
loading data from Excel files, generating data input files, and managing the 
SQLite database interactions via the SQLManager.
"""

from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from esm.backend.data_table import DataTable
from esm.backend.index import Index
from esm.backend.set_table import SetTable
from esm.backend.variable import Variable
from esm.log_exc import exceptions as exc
from esm.log_exc.logger import Logger
from esm.constants import Constants
from esm.support import util
from esm.support.file_manager import FileManager
from esm.support.sql_manager import SQLManager, db_handler


class Database:
    """
    Manages database operations for the modeling application, including file 
    and SQLite operations.

    Attributes:
        logger (Logger): An instance of Logger for logging information messages.
        files (FileManager): Manages file-related operations with files.
        sqltools (SQLManager): Manages SQL database interactions.
        index (Index): Central index for managing set tables and data tables.
        paths (Dict): Contains paths used throughout operations, such as for files and directories.
        settings (Dict): Configuration settings for the application.

    Parameters:
        logger (Logger): Logger instance for the class.
        files (FileManager): FileManager instance for handling file operations.
        paths (Dict): Dictionary of path configurations.
        sqltools (SQLManager): SQLManager instance for handling SQL operations.
        settings (Dict): Dictionary of settings.
        index (Index): Index instance for accessing and managing data structures.
    """

    def __init__(
            self,
            logger: Logger,
            files: FileManager,
            sqltools: SQLManager,
            index: Index,
            paths: Dict,
            settings: Dict,
    ) -> None:
        """
        Initializes the Database class with the necessary components and settings.

        Parameters:
            logger (Logger): An instance of Logger for logging information and 
                error messages.
            files (FileManager): An instance of FileManager for managing 
                file-related operations.
            sqltools (SQLManager): An instance of SQLManager for managing SQL 
                database interactions.
            index (Index): An instance of Index for managing set tables and data 
                tables.
            paths (Dict[str, str]): A dictionary containing paths used throughout 
                operations, such as for files and directories.
            settings (Dict[str, Any]): A dictionary containing configuration 
                settings for the application.

        Returns:
            None

        Notes:
            The logger is initialized with a child logger using the name of the 
                current module.
            If the 'use_existing_data' setting is False, a blank sets Excel file 
                is created for defining sets.
        """
        self.logger = logger.get_child(__name__)

        self.files = files
        self.sqltools = sqltools
        self.index = index
        self.settings = settings
        self.paths = paths

        if not self.settings['use_existing_data']:
            self.create_blank_sets_xlsx_file()

    def __repr__(self):
        class_name = type(self).__name__
        return f'{class_name}'

    def create_blank_sets_xlsx_file(self) -> None:
        """
        Creates a blank Excel file for sets if it does not exist, or erases it 
        based on settings.
        This method checks if the sets Excel file specified in the settings exists. 
        If it does and 'use_existing_data' is False, the method erases the existing 
        file. If 'use_existing_data' is True or the file does not exist, the method 
        creates a new blank Excel file with headers for each set.

        Returns:
            None

        Notes:
            The method logs information about whether it is using an existing file, 
                erasing an existing file, or creating a new file.
            The headers for the new Excel file are determined based on the 
                'set_excel_file_headers' attribute of each set in the index.
            Sets that have a 'copy_from' attribute are not included in the new 
                Excel file.
        """
        sets_file_name = Constants.ConfigFiles.SETS_FILE

        if Path(self.paths['sets_excel_file']).exists():
            if not self.settings['use_existing_data']:
                self.logger.info(
                    f"Sets excel file '{sets_file_name}' already exists.")

                erased = self.files.erase_file(
                    dir_path=self.paths['model_dir'],
                    file_name=sets_file_name,
                    force_erase=False,
                    confirm=True,
                )

                if erased:
                    self.logger.info(
                        f"Sets excel file '{sets_file_name}' erased and "
                        "overwritten.")
                else:
                    self.logger.info(
                        f"Relying on existing sets excel file '{sets_file_name}'.")
                    return
            else:
                self.logger.info(
                    f"Relying on existing sets excel file '{sets_file_name}'.")
                return
        else:
            self.logger.info(
                f"Generating new sets excel file '{sets_file_name}'.")

        dict_headers = {
            set_value.table_name: set_value.set_excel_file_headers
            for set_value in self.index.sets.values()
            if getattr(set_value, 'copy_from', None) is None
        }

        self.files.dict_to_excel_headers(
            dict_name=dict_headers,
            excel_dir_path=self.paths['model_dir'],
            excel_file_name=sets_file_name,
        )

    def create_blank_sqlite_database(self) -> None:
        """
        Creates a blank SQLite database with table structures defined in the 
        Model.Index class. 
        This method generates a new SQLite database file as specified in the 
        settings. It then iterates over each set in the index, validates that 
        it is an instance of SetTable, and creates a new table in the database 
        for the set. The table's headers are determined based on the 
        'table_headers' attribute of the set.

        Returns:
            None

        Raises:
            AssertionError: If a set in the index is not an instance of SetTable.
            MissingDataError: If the 'table_headers' attribute of a set is None.

        Notes:
            The method logs information about the creation of the database and 
                each table.
            If the 'table_headers' attribute of a set does not include the 
                standard ID field, the method adds it.
        """
        self.logger.debug(
            f"Generating database '{self.settings['sqlite_database_file']}'.")

        with db_handler(self.sqltools):
            for set_instance in self.index.sets.values():
                assert isinstance(set_instance, SetTable), \
                    f"Expected SetTable type, got {type(set_instance)} instead."

                set_name = set_instance.name
                table_name = set_instance.table_name
                table_headers = set_instance.table_headers
                table_id_header = Constants.Labels.ID_FIELD['id']

                if table_headers is not None:
                    if table_id_header not in table_headers.values():
                        table_headers = {
                            **Constants.Labels.ID_FIELD, **table_headers}

                    self.sqltools.create_table(table_name, table_headers)

                else:
                    msg = f"Table fields for set '{set_name}' are not defined."
                    self.logger.error(msg)
                    raise exc.MissingDataError(msg)

    def load_sets_to_sqlite_database(self) -> None:
        """
        Loads the sets data from the in-memory data structures into the SQLite 
        database.
        This method iterates over each set in the index, validates that it is an 
        instance of SetTable, and loads the set's data into the corresponding table 
        in the SQLite database. The data is assumed to be already present in the 
        set instances within the index.

        Returns:
            None

        Raises:
            AssertionError: If a set in the index is not an instance of SetTable.
            MissingDataError: If the 'data' attribute of a set is None, indicating 
                incomplete setup.

        Notes:
            The method logs information about the loading process for each set.
            If the 'table_headers' attribute of a set does not include the 
                standard ID field, the method adds it.
        """
        self.logger.debug(
            f"Loading Sets to '{self.settings['sqlite_database_file']}'.")

        with db_handler(self.sqltools):
            for set_instance in self.index.sets.values():
                assert isinstance(set_instance, SetTable), \
                    f"Expected SetTable type, got {type(set_instance)} instead."

                if set_instance.data is not None:
                    table_name = set_instance.table_name
                    dataframe = set_instance.data.copy()
                    table_headers = set_instance.table_headers
                    table_id_header = Constants.Labels.ID_FIELD['id']
                else:
                    msg = f"Data of set '{set_instance.symbol}' are not defined."
                    self.logger.error(msg)
                    raise exc.MissingDataError(msg)

                if table_headers is not None:
                    if table_id_header not in table_headers.values():
                        util.add_column_to_dataframe(
                            dataframe=dataframe,
                            column_header=table_id_header[0],
                            column_position=0,
                            column_values=None,
                        )

                self.sqltools.dataframe_to_table(
                    table_name, dataframe)

    def generate_blank_sqlite_data_tables(self) -> None:
        """
        Generates empty data tables in the SQLite database for endogenous and 
        exogenous variables.
        This method iterates over each data table in the index. If the table's 
        type is not 'constant', it creates a new table in the SQLite database 
        for the data table. The table's headers and foreign keys are determined 
        based on the 'table_headers' and 'foreign_keys' attributes of the data table.

        Returns:
            None

        Notes:
            The method logs information about the creation of each table.
            Constant tables are skipped as they do not require a separate table 
                in the SQLite database.
        """
        self.logger.debug(
            "Generation of empty data tables in "
            f"'{Constants.ConfigFiles.SQLITE_DATABASE_FILE}'.")

        with db_handler(self.sqltools):
            for table_key, table in self.index.data.items():
                table: DataTable

                if table.type == 'constant':
                    continue

                self.sqltools.create_table(
                    table_name=table_key,
                    table_fields=table.table_headers,
                    foreign_keys=table.foreign_keys,
                )

    def sets_data_to_sql_data_tables(
            self,
            lightweight: bool = True,
    ) -> None:
        """
        Transforms and loads sets data into SQLite tables, preparing them for 
        variable storage.
        This method iterates over each data table in the index. If the table's 
        type is not 'constant', it unpivots the table's coordinates values into 
        a DataFrame, adds an ID column to the DataFrame, and loads the DataFrame 
        into the corresponding table in the SQLite database. It then adds a 
        standard values field to the table.
        Excludes constant types to separate related configuration from variable 
        data.

        Returns:
            None

        Notes:
            The method logs information about the loading process for each table.
            The unpivoting process transforms the coordinates values from a 
                dictionary format into a DataFrame format.
            The standard values field is added to store the values of the variables.
        """
        self.logger.debug(
            "Adding sets information to SQLite data tables in "
            f"'{Constants.ConfigFiles.SQLITE_DATABASE_FILE}'.")

        with db_handler(self.sqltools):
            for table_key, table in self.index.data.items():
                table: DataTable

                if table.type == 'constant':
                    continue

                table_headers_list = [
                    value for value in table.coordinates_headers.values()
                ]

                unpivoted_coords_df = util.unpivot_dict_to_dataframe(
                    data_dict=table.coordinates_values,
                    key_order=table_headers_list
                )

                if lightweight:
                    self.logger.debug(
                        "Generating lightweight SQLite data tables relying only on "
                        "set combinations filtered by model variables.")

                    dicts_list = []
                    for variable in self.index.variables.values():
                        variable: Variable
                        if variable.related_table == table_key:
                            dicts_list.append(
                                variable.all_coordinates_w_headers
                            )

                    coords_dict = util.merge_dicts(
                        dicts_list=dicts_list,
                        unique_values=True
                    )

                    coords_to_keep_df = util.unpivot_dict_to_dataframe(
                        data_dict=coords_dict,
                        key_order=table_headers_list
                    )

                    unpivoted_coords_df = unpivoted_coords_df.merge(
                        coords_to_keep_df,
                        on=table_headers_list,
                        how='inner'
                    )

                    if not util.check_dataframes_equality(
                        df_list=[coords_to_keep_df, unpivoted_coords_df]
                    ):
                        msg = "Dataframes are not equal after merge operation."
                        self.logger.error(msg)
                        raise exc.OperationalError(msg)

                util.add_column_to_dataframe(
                    dataframe=unpivoted_coords_df,
                    column_header=table.table_headers['id'][0],
                    column_position=0,
                    column_values=None
                )

                self.sqltools.dataframe_to_table(
                    table_name=table_key,
                    dataframe=unpivoted_coords_df,
                )

                self.sqltools.add_table_column(
                    table_name=table_key,
                    column_name=Constants.Labels.VALUES_FIELD['values'][0],
                    column_type=Constants.Labels.VALUES_FIELD['values'][1],
                )

    def clear_database_tables(
        self,
        table_names: Optional[List[str] | str] = None,
    ) -> None:
        """
        Clears specified tables or all tables from the SQLite database.
        This method accepts a list of table names or a single table name to 
        clear. If no table names are provided, it clears all tables in the 
        SQLite database. The method logs information about the clearing process 
        and uses the SQLManager instance to drop the tables.

        Parameters:
            table_names (Optional[List[str] | str]): A list of table names or a 
                single table name to clear. If None, all tables in the database 
                will be cleared.

        Returns:
            None

        Notes:
            The method uses a context manager to handle the database connection.
            If a table name is not found in the index, the method skips it.
        """
        with db_handler(self.sqltools):
            existing_tables = self.sqltools.get_existing_tables_names

            if not table_names:
                tables_to_clear = existing_tables
                self.logger.info(
                    "Clearing all tables from SQLite database "
                    f"{Constants.ConfigFiles.SQLITE_DATABASE_FILE}"
                )

            else:
                tables_to_clear = list(table_names)
                self.logger.info(
                    f"Clearing tables '{tables_to_clear}' from SQLite database "
                    f"{Constants.ConfigFiles.SQLITE_DATABASE_FILE}"
                )

            for table_name in tables_to_clear:
                if table_name in self.index.data.keys():
                    self.sqltools.drop_table(table_name)

    def generate_blank_data_input_files(
        self,
        table_key_list: List[str] = [],
        file_extension: str = Constants.ConfigFiles.DATA_FILES_EXTENSION,
    ) -> None:
        """
        Generates blank data input files for exogenous data tables.
        This method iterates over each data table in the index. If the table's 
        type is 'exogenous', it exports the table's data from the SQLite database 
        to an Excel file. The file's name is determined based on the 
        'multiple_input_files' setting and the table's key. If 'multiple_input_files' 
        is True, a separate file is created for each table. Otherwise, all tables 
        are exported to a single file as separate tabs.

        Parameters:
            file_extension (str, optional): The file extension to use for the 
                generated files. Defaults to the 'data_file_extension' class attribute.

        Returns:
            None

        Notes:
            The method logs information about the file generation process.
            If the input data directory does not exist, the method creates it.
            Endogenous and constant tables are skipped as they do not require 
                input files.
        """
        self.logger.debug("Generation of data input file/s.")

        if not Path(self.paths['input_data_dir']).exists():
            self.files.create_dir(self.paths['input_data_dir'])

        with db_handler(self.sqltools):
            for table_key, table in self.index.data.items():

                if table_key_list != [] and table_key not in table_key_list:
                    continue

                if table.type in ['endogenous', 'constant']:
                    continue

                if self.settings['multiple_input_files']:
                    output_file_name = table_key + file_extension
                else:
                    output_file_name = Constants.ConfigFiles.INPUT_DATA_FILE

                self.sqltools.table_to_excel(
                    excel_filename=output_file_name,
                    excel_dir_path=self.paths['input_data_dir'],
                    table_name=table_key,
                    blank_value_field=True
                )

    def load_data_input_files_to_database(
        self,
        file_extension: str = Constants.ConfigFiles.DATA_FILES_EXTENSION,
        force_overwrite: bool = False,
        table_key_list: list[str] = [],
    ) -> None:
        """
        Loads data from user-filled input files into the SQLite database.
        This method checks the 'multiple_input_files' setting to determine whether 
        to load data from multiple files or a single file. If 'multiple_input_files' 
        is True, the method iterates over each exogenous data table in the index, 
        loads the table's data from the corresponding Excel file, and inserts  
        the data in the SQLite database. If 'multiple_input_files' is False, 
        the method loads data from a single Excel file and inserts or updates the 
        data for each table in the SQLite database.

        Parameters:
            empty_data_fill (Any, optional): The value to fill empty data cells
                with. Defaults to None.
            file_extension (str, optional): The extension of the data files to 
                load. Defaults to the 'data_file_extension' class attribute.
            force_overwrite (bool, optional): If True, forces the overwrite of 
                existing data. Defaults to False.

        Returns:
            None
        """
        self.logger.debug(
            "Loading data from input file/s filled by the user "
            "to SQLite database.")

        if table_key_list == []:
            table_key_list = self.index.data.keys()
        else:
            if not util.items_in_list(
                table_key_list,
                self.index.data.keys()
            ):
                msg = "One or more passed tables keys not present in the index."
                self.logger.error(msg)
                raise ValueError(msg)

        if self.settings['multiple_input_files']:
            data = {}

            with db_handler(self.sqltools):
                for table_key, table in self.index.data.items():
                    table: DataTable

                    if table_key not in table_key_list:
                        continue

                    if table.type not in ['endogenous', 'constant']:
                        file_name = table_key + file_extension

                        data.update(
                            self.files.excel_to_dataframes_dict(
                                excel_file_dir_path=self.paths['input_data_dir'],
                                excel_file_name=file_name,
                            )
                        )

                        if table_key not in data.keys():
                            msg = f"Table key '{table_key}' not found as tab name " \
                                f"in xlsx file '{file_name}'."
                            self.logger.error(msg)
                            raise exc.MissingDataError(msg)

                        self.sqltools.dataframe_to_table(
                            table_name=table_key,
                            dataframe=data[table_key],
                            force_overwrite=force_overwrite,
                        )

        else:
            data = self.files.excel_to_dataframes_dict(
                excel_file_dir_path=self.paths['input_data_dir'],
                excel_file_name=Constants.ConfigFiles.INPUT_DATA_FILE,
            )

            with db_handler(self.sqltools):
                for table_key, table in data.items():

                    if table_key not in table_key_list:
                        continue

                    self.sqltools.dataframe_to_table(
                        table_name=table_key,
                        dataframe=table,
                        force_overwrite=force_overwrite,
                    )

    def fill_nan_values_in_database(
            self,
            force_overwrite: bool = False,
            table_key_list: List[str] = [],
    ) -> None:
        """
        The method parse variables and related 'blank_fill' values from the index.
        Then, it iterates over each data table in the index and fills the NaN
        values in the SQLite database with the corresponding 'blank_fill' values.
        This should facilitate the definition of data in the input files.

        Args:
            force_overwrite (bool, optional): If True, forces the overwrite of
                existing data. Defaults to False.
        """
        self.logger.debug(
            "Filling blank data in SQLite data tables based on the 'blank_fill' "
            "attribute of each variable.")

        blank_fill_key = Constants.Labels.BLANK_FILL_KEY
        value_header = Constants.Labels.VALUES_FIELD['values'][0]

        if table_key_list == []:
            table_key_list = self.index.data.keys()
        else:
            if not util.items_in_list(
                table_key_list,
                self.index.data.keys()
            ):
                msg = "One or more passed tables keys not present in the index."
                self.logger.error(msg)
                raise ValueError(msg)

        with db_handler(self.sqltools):

            for var_key, variable in self.index.variables.items():
                variable: Variable

                blank_fill_value = variable.var_info.get(blank_fill_key, None)
                related_table = variable.related_table

                if related_table not in table_key_list:
                    continue

                if blank_fill_value is None:
                    continue

                df_query = self.sqltools.table_to_dataframe(
                    table_name=related_table,
                    filters_dict=variable.all_coordinates_w_headers,
                )

                df_query_nan = df_query[df_query[value_header].isna()]
                df_query_nan.loc[
                    df_query[value_header].isna(), value_header
                ] = blank_fill_value

                self.logger.debug(
                    f"Table '{related_table}' | Filling '{len(df_query_nan)}' "
                    f"entries with value '{blank_fill_value}' (Variable '{var_key}')."
                )

                self.sqltools.dataframe_to_table(
                    table_name=related_table,
                    dataframe=df_query_nan,
                    action='update',
                    force_overwrite=force_overwrite,
                )

    def reinit_sqlite_endogenous_tables(
            self,
            force_overwrite: bool = False,
    ) -> None:
        """
        Reinitializes the endogenous tables in the SQLite database.
        This method iterates over each endogenous data table in the index and 
        clears the table in the SQLite database. 

        Returns:
            None

        Notes:
            The method uses a context manager to handle the database connection.
        """

        with db_handler(self.sqltools):
            for table_key, table in self.index.data.items():

                if table.type == 'endogenous':

                    self.logger.debug(
                        f"Reinitializing endogenous table '{table_key}' "
                        "in SQLite database.")

                    self.sqltools.delete_table_column_data(
                        table_name=table_key,
                        force_operation=force_overwrite,
                        column_name=Constants.Labels.VALUES_FIELD['values'][0],
                    )
