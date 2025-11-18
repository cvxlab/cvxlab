"""Module defining the FileManager class.

The FileManager class provides methods for handling file and directory operations
such as creating and erasing directories, copying files, and managing data files
like JSON, YAML, and Excel. It is designed to facilitate robust management of
file operations required in model setups, ensuring data integrity and ease of
data manipulation across various components of the application.
"""
from types import NoneType
from typing import List, Dict, Any, Literal, Optional
from pathlib import Path

import importlib.util
import os
import shutil
import json
import yaml

import pandas as pd
import numpy as np

from cvxlab.defaults import Defaults
from cvxlab.log_exc import exceptions as exc
from cvxlab.log_exc.logger import Logger
from cvxlab.support import util


class FileManager:
    """FileManager class for managing file and directory operations.

    The FileManager class provides methods to handle directories and file interactions,
    including creating, deleting, loading, and copying files across directories.
    It simplifies file operations required in various parts of a modeling application,
    ensuring that file manipulations are handled efficiently and reliably.

    Attributes:
    - logger (Logger): Logger object for logging information and errors.
    - xls_engine (str): Default Excel engine to use ('openpyxl' or 'xlsxwriter').
    """

    def __init__(
        self,
        logger: Logger,
        xls_engine: Literal['openpyxl', 'xlsxwriter', None] = None,
    ) -> None:
        """Initialize FileManager with logger and optional Excel engine.

        Args:
            logger (Logger): Logger object for logging messages.
            xls_engine (Literal['openpyxl', 'xlsxwriter', None], optional): Excel 
                engine for reading/writing files.
        """
        self.logger = logger.get_child(__name__)

        if xls_engine is None:
            self.xls_engine = 'openpyxl'
        else:
            self.xls_engine = xls_engine

    def create_dir(
            self,
            dir_path: Path,
            force_overwrite: bool = False,
    ) -> None:
        """Create a directory at the specified path.

        Args:
            dir_path (Path): Path where the directory will be created.
            force_overwrite (bool): If True, overwrite existing directory.
        """
        dir_name = dir_path.name

        if os.path.exists(dir_path) and not force_overwrite:
            self.logger.warning(f"Directory '{dir_name}' already exists.")
            if not util.get_user_confirmation(f"Overwrite directory '{dir_name}'?"):
                self.logger.debug(f"Directory '{dir_name}' not overwritten.")
                return

        if os.path.exists(dir_path) and force_overwrite:
            shutil.rmtree(dir_path)

        os.makedirs(dir_path, exist_ok=True)
        self.logger.debug(f"Directory '{dir_name}' created.")

    def erase_dir(
            self,
            dir_path: Path,
            force_erase: bool = False,
    ) -> bool:
        """Erase the directory at the specified path.

        Args:
            dir_path (Path): Path of the directory to erase.
            force_erase (bool): If True, erase without confirmation.

        Returns:
            bool: True if erased, False otherwise.
        """
        dir_name = str(dir_path).rsplit('\\', maxsplit=1)[-1]

        if os.path.exists(dir_path):
            if not force_erase:
                if not util.get_user_confirmation(
                    f"Do you really want to erase the directory '{dir_name}'?"
                ):
                    self.logger.debug(
                        f"Directory '{dir_name}' and its content not erased.")
                    return False

            try:
                shutil.rmtree(dir_path)
            except OSError as error:
                self.logger.error(f"Error: '{dir_name}' : {error.strerror}")
                return False
            else:
                self.logger.debug(f"Directory '{dir_name}' have been erased.")
                return True

        else:
            self.logger.warning(
                f"Folder '{dir_name}' does not exist. The folder cannot be erased.")
            return False

    def load_structured_file(
            self,
            file_name: str,
            dir_path: Path,
            file_type: str = 'yml',
    ) -> Dict[str, Any]:
        """Load a JSON or YAML file from the specified directory.

        Args:
            file_name (str): Name of the file to load.
            dir_path (Path): Directory containing the file.
            file_type (str): Format of the file ('json' or 'yml').

        Returns:
            Dict[str, Any]: Contents of the file as a dictionary.
        """
        if file_type == 'json':
            loader = json.load
        elif file_type in {'yml', 'yaml'}:
            loader = yaml.safe_load
        else:
            self.logger.error(
                'Invalid file type. Only JSON and YAML are allowed.')
            return {}

        file_path = Path(dir_path, file_name)

        try:
            with open(file_path, 'r', encoding='utf-8') as file_obj:
                file_contents = loader(file_obj)
                self.logger.debug(f"File '{file_name}' loaded.")
                return file_contents
        except FileNotFoundError as error:
            self.logger.error(
                f"Could not load file '{file_name}': {str(error)}")
            return {}

    def load_functions_from_module(
            self,
            file_name: str,
            dir_path: Path | str,
    ) -> list[callable]:
        """Load functions from a Python module.

        Returns:
            list[callable]: List of functions defined in the file.
        """
        file_path = Path(dir_path) / file_name

        if not os.path.exists(file_path):
            self.logger.error(f"File '{file_name}' does not exist.")
            return []

        spec = importlib.util.spec_from_file_location(
            "module.name", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        functions_list = [
            getattr(module, attr) for attr in dir(module)
            if callable(getattr(module, attr))
        ]

        self.logger.debug(f"Functions loaded from '{file_name}'.")
        return functions_list

    def erase_file(
            self,
            dir_path: Path | str,
            file_name: str,
            force_erase: bool = False,
            confirm: bool = True,
    ) -> bool:
        """Erase a specified file from a directory.

        Args:
            dir_path (Path | str): Directory containing the file.
            file_name (str): Name of the file to erase.
            force_erase (bool): If True, erase without confirmation.
            confirm (bool): If True, prompt for confirmation.

        Returns:
            bool: True if erased, False otherwise.
        """
        file_path = Path(dir_path) / file_name

        if not os.path.exists(file_path):
            self.logger.warning(
                f"File '{file_name}' does not exist. The file cannot be erased.")
            return False

        if confirm and not force_erase:
            if not util.get_user_confirmation(
                    f"Do you really want to erase file '{file_name}'? "
            ):
                self.logger.debug(f"File '{file_name}' not erased.")
                return False

        try:
            os.remove(file_path)
            self.logger.debug(f"File '{file_name}' have been erased.")
            return True
        except OSError as error:
            self.logger.error(f"Error: '{file_name}' : {error.strerror}")
            return False

    def dir_files_check(
            self,
            dir_path: str | Path,
            files_names_list: List[str],
    ) -> bool:
        """Check if directory exists and all listed files are present.

        Args:
            dir_path (str | Path): Directory path to check.
            files_names_list (List[str]): List of file names to check.

        Returns:
            bool: True if directory and all files exist.

        Raises:
            ModelFolderError: If directory or any file is missing.
        """
        msg = ''

        if not Path(dir_path).is_dir():
            msg = f"Directory '{dir_path}' does not exist."

        missing_files = [
            file_name for file_name in files_names_list
            if not (Path(dir_path) / file_name).is_file()]

        if missing_files:
            msg = f"Model setup files '{missing_files}' are missing."

        if msg:
            self.logger.error(msg)
            raise exc.ModelFolderError(msg)

        return True

    def copy_file_to_destination(
            self,
            path_destination: str | Path,
            path_source: str,
            file_name: str,
            file_new_name: Optional[str] = None,
            force_overwrite: bool = False,
    ) -> None:
        """Copy a file from source to destination.

        Args:
            path_destination (str | Path): Destination path.
            path_source (str): Source path.
            file_name (str): Name of the file to copy.
            file_new_name (Optional[str]): New name for the file at destination.
            force_overwrite (bool): If True, overwrite existing file.

        Raises:
            FileNotFoundError: If source file does not exist.
        """
        root_path = Path(__file__).parents[2]
        source_path = Path(root_path) / path_source / file_name
        destination_file_name = file_new_name or source_path.name
        destination_file_path = Path(path_destination) / destination_file_name

        if destination_file_path.exists() and not force_overwrite:
            self.logger.warning(f"'{file_name}' already exists.")
            if not util.get_user_confirmation(f"Overwrite '{file_name}'?"):
                self.logger.debug(f"'{file_name}' NOT overwritten.")
                return

        if source_path.exists() and source_path.is_file():
            shutil.copy2(source_path, destination_file_path)
            self.logger.debug(
                f"File '{file_name}' successfully copied as '{file_new_name}'.")
        else:
            msg = f"The source file '{source_path}' does not exist."
            self.logger.error(msg)
            raise FileNotFoundError(msg)

    def copy_all_files_to_destination(
            self,
            path_source: str | Path,
            path_destination: str | Path,
            force_overwrite: bool = False,
    ) -> None:
        """Copy all files and directories from source to destination.

        Args:
            path_source (str | Path): Source directory.
            path_destination (str | Path): Destination directory.
            force_overwrite (bool): If True, overwrite existing content.

        Raises:
            ModelFolderError: If source path does not exist or is not a directory.
        """
        path_source = Path(path_source)
        path_destination = Path(path_destination)

        if not path_source.exists():
            msg = "The passed source path does not exists."
            self.logger.error(msg)
            raise exc.ModelFolderError(msg)

        if not os.path.isdir(path_source):
            msg = "The passed source path is not a directory."
            self.logger.error(msg)
            raise exc.ModelFolderError(msg)

        if not path_destination.exists():
            self.create_dir(path_destination)

        if os.listdir(path_destination) and not force_overwrite:
            dir_destination = os.path.basename(path_destination)

            self.logger.warning(f"Directory '{dir_destination}' not empty.")
            if not util.get_user_confirmation(
                f"Overwrite content of '{dir_destination}'?"
            ):
                self.logger.debug(f"'{dir_destination}' NOT overwritten.")
                return

        try:
            shutil.copytree(
                src=path_source,
                dst=path_destination,
                dirs_exist_ok=True
            )
            self.logger.debug(
                f"Directory '{os.path.basename(path_source)}' and all its "
                "content successfully copied.")
        except shutil.Error as msg:
            self.logger.error(f"Error copying items: {msg}")

    def rename_file(
            self,
            dir_path: str | Path,
            name_old: str,
            name_new: str,
            file_extension: Optional[str] = None,
    ) -> None:
        """Rename a file in the specified directory.

        Args:
            dir_path (str | Path): Directory containing the file.
            name_old (str): Current name of the file.
            name_new (str): New name for the file.
            file_extension (Optional[str]): File extension if not included.

        Raises:
            FileNotFoundError: If file does not exist.
            FileExistsError: If new file name already exists.
        """
        dir_path = Path(dir_path)

        if file_extension:
            name_old = f"{name_old}.{file_extension.lstrip('.')}"
            name_new = f"{name_new}.{file_extension.lstrip('.')}"
        else:
            if '.' not in name_old or '.' not in name_new:
                raise ValueError(
                    "File extension must be specified when not included "
                    "in the file name.")

        file_path = dir_path / name_old
        new_file_path = dir_path / name_new

        if not file_path.exists():
            raise FileNotFoundError(f"File '{file_path}' does not exist.")

        if new_file_path.exists():
            raise FileExistsError(
                f"A file named '{name_new}' already exists. Operation aborted.")

        file_path.rename(new_file_path)
        self.logger.debug(f"File '{name_old}' renamed to '{name_new}'.")

    def dict_to_excel_headers(
            self,
            dict_name: Dict[str, Any],
            excel_dir_path: Path,
            excel_file_name: str,
            writer_engine: Optional[Literal['openpyxl', 'xlsxwriter']] = None,
    ) -> None:
        """Generate an Excel file with sheets named by dictionary keys and headers.

        Args:
            dict_name (Dict[str, Any]): Dictionary with sheet names and column headers.
            excel_dir_path (Path): Directory to save the Excel file.
            excel_file_name (str): Filename for the Excel file.
            writer_engine (Optional[Literal['openpyxl', 'xlsxwriter']]): Excel writing engine.

        Raises:
            TypeError: If dict_name is not a dictionary.
            SettingsError: If any sheet headers list is invalid.
        """
        if writer_engine is None:
            writer_engine = self.xls_engine

        if not isinstance(dict_name, Dict):
            error_msg = f"{dict_name} is not a dictionary."
            self.logger.error(error_msg)
            raise TypeError(error_msg)

        def write_excel(
                excel_file_path: str | Path,
                dict_name: Dict[str, Any]
        ) -> None:
            """Support function to generate excel."""
            with pd.ExcelWriter(
                excel_file_path,
                engine=writer_engine,
            ) as writer:
                for sheet_name, headers_list in dict_name.items():
                    if not isinstance(headers_list, List):
                        msg = f"Invalid headers list for table '{sheet_name}'."
                        self.logger.error(msg)
                        raise exc.SettingsError(msg)

                    dataframe = pd.DataFrame(columns=headers_list)
                    sheet = writer.book.create_sheet(sheet_name)
                    writer.sheets[sheet_name] = sheet
                    dataframe.to_excel(
                        writer,
                        sheet_name=sheet_name,
                        index=False
                    )
                    self.logger.debug(
                        f"Excel tab name '{sheet_name}' inserted "
                        f"into '{os.path.basename(excel_file_path)}'."
                    )

        excel_file_path = Path(excel_dir_path, excel_file_name)

        if os.path.exists(excel_file_path):
            self.logger.warning(
                f"Excel file '{excel_file_name}' already exists.")
            if not util.get_user_confirmation(
                f"Do you really want to overwrite the file '{excel_file_name}'?"
            ):
                write_excel(excel_file_path, dict_name)
            else:
                self.logger.debug(
                    f"Excel file '{excel_file_name}' not overwritten.")
        else:
            write_excel(excel_file_path, dict_name)

    def dataframe_to_excel(
            self,
            dataframe: pd.DataFrame,
            excel_filename: str,
            excel_dir_path: str,
            sheet_name: Optional[str] = None,
            writer_engine: Optional[Literal['openpyxl', 'xlsxwriter']] = None,
            force_overwrite: bool = False,
    ) -> None:
        """Export a DataFrame to an Excel file.

        Optionally allows overwriting an existing file.

        Args:
            dataframe (pd.DataFrame): DataFrame to export.
            excel_filename (str): Name of the Excel file.
            excel_dir_path (str): Directory to save the Excel file.
            sheet_name (Optional[str]): Name of the sheet.
            writer_engine (Optional[Literal['openpyxl', 'xlsxwriter']]): Excel 
                writing engine.
            force_overwrite (bool): If True, overwrite existing file.

        Raises:
            Warning: If file exists and not overwritten.
        """
        if writer_engine is None:
            writer_engine = self.xls_engine

        excel_file_path = Path(excel_dir_path, excel_filename)

        if not force_overwrite:
            if excel_file_path.exists():
                self.logger.warning(
                    f"Excel file '{excel_filename}' already exists.")
                if not util.get_user_confirmation(
                    f"Do you want to overwrite  '{excel_filename}'?"
                ):
                    self.logger.warning(
                        f"File '{excel_filename}' not overwritten.")
                    return

        mode = 'a' if excel_file_path.exists() else 'w'
        if_sheet_exists = 'replace' if mode == 'a' else None

        self.logger.debug(
            f"Exporting dataframe '{sheet_name}' to '{excel_filename}'.")

        if sheet_name is None:
            sheet_name = str(dataframe)

        with pd.ExcelWriter(
            excel_file_path,
            engine=writer_engine,
            mode=mode,
            if_sheet_exists=if_sheet_exists,
        ) as writer:
            dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

    def excel_to_dataframes_dict(
            self,
            excel_file_name: str,
            excel_file_dir_path: Path | str,
            empty_data_fill: Optional[Any] = None,
            set_values_type: bool = True,
            values_normalization: bool = True,
    ) -> Dict[str, pd.DataFrame]:
        """Read an Excel file with multiple sheets into a dictionary of DataFrames.

        Args:
            excel_file_name (str): Name of the Excel file.
            excel_file_dir_path (Path | str): Directory containing the Excel file.
            empty_data_fill (Optional[Any]): Value to fill empty cells.
            set_values_type (bool): If True, set values column type.
            values_normalization (bool): If True, normalize values.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary of DataFrames for each sheet.

        Raises:
            FileNotFoundError: If Excel file does not exist.
        """
        file_path = Path(excel_file_dir_path, excel_file_name)

        if set_values_type:
            values_dtype = Defaults.NumericalSettings.STD_VALUES_TYPE
            values_name = Defaults.Labels.VALUES_FIELD['values'][0]

        if not os.path.exists(file_path):
            self.logger.error(f'{excel_file_name} does not exist.')
            raise FileNotFoundError(f"{excel_file_name} does not exist.")

        try:
            df_dict = pd.read_excel(io=file_path, sheet_name=None)
        except Exception as error:
            msg = f"Error reading Excel file: {str(error)}"
            self.logger.error(msg)
            raise exc.OperationalError(msg)

        if not values_normalization:
            return df_dict

        for df_key, dataframe in df_dict.items():
            try:
                # Convert 'values' column if needed
                if set_values_type and values_name in dataframe.columns:
                    dataframe[values_name] = \
                        dataframe[values_name].astype(values_dtype)

                # Explicitly replace all NaN types (including numpy.float64('nan'))
                # with None and then replace NaN with None
                dataframe.replace({pd.NA: None, np.nan: None}, inplace=True)

                # replace None with empty_data_fill
                if empty_data_fill is not None:
                    dataframe.fillna(empty_data_fill, inplace=True)

                df_dict[df_key] = dataframe

            except ValueError as ve:
                msg = f"Normalization error | xlsx sheet '{df_key}' | {str(ve)}"
                self.logger.error(msg)
                raise exc.OperationalError(msg)
            except Exception as e:
                msg = f"Unexpected error | xlsx sheet '{df_key}' | {str(e)}"
                self.logger.error(msg)
                raise exc.OperationalError(msg)

        return df_dict

    def excel_tab_to_dataframe(
            self,
            excel_file_name: str,
            excel_file_dir_path: Path | str,
            tab_name: str = None,
            convert_native_types: bool = False,
    ) -> pd.DataFrame:
        """Read a specific tab from an Excel file as a DataFrame.

        Args:
            excel_file_name (str): Name of the Excel file.
            excel_file_dir_path (Path | str): Directory containing the Excel file.
            tab_name (str, optional): Name of the tab to read. If None, reads first tab.
            convert_native_types (bool): If True, keep native types.

        Returns:
            pd.DataFrame: DataFrame from the specified tab.

        Raises:
            FileNotFoundError: If Excel file does not exist.
        """
        file_path = Path(excel_file_dir_path, excel_file_name)

        if not os.path.exists(file_path):
            msg = f"{excel_file_name} does not exist."
            self.logger.error(msg)
            raise FileNotFoundError(msg)

        xlsx_file = pd.ExcelFile(file_path)
        sheet_names = xlsx_file.sheet_names

        if tab_name is None:
            if len(sheet_names) > 1:
                msg = f"Multiple tabs found in '{excel_file_name}'. Specify " \
                    f"one of the following tabs: '{sheet_names}'."
                self.logger.error(msg)
                raise ValueError(msg)
            tab_name = sheet_names[0]
        else:
            if tab_name not in sheet_names:
                msg = f"Tab '{tab_name}' not found in '{excel_file_name}'. " \
                    f"Available tabs: '{sheet_names}'."
                self.logger.error(msg)
                raise ValueError(msg)

        dataframe = xlsx_file.parse(
            sheet_name=tab_name,
            keep_default_na=convert_native_types,
        )

        # case of native types from excel
        if not convert_native_types:
            # replace empty strings with None
            dataframe = dataframe.replace('', None).infer_objects(copy=False)
            # replace true/True/TRUE/false/False/FALSE with bool
            dataframe = dataframe.replace(
                Defaults.DefaultStructures.ALLOWED_BOOL
            ).infer_objects(copy=False)

        # replace NaN with None
        dataframe = dataframe.astype(object).where(pd.notna(dataframe), None)

        self.logger.debug(
            f"Excel tab '{tab_name}' loaded from '{excel_file_name}'.")

        return dataframe

    def load_data_structure(
            self,
            structure_key: str,
            source: str,
            dir_path: Path | str,
    ) -> Dict:
        """Load a data structure from YAML or Excel source.

        Args:
            structure_key (str): Key for the structure to load.
            source (str): Source type ('yml' or 'xlsx').
            dir_path (Path | str): Directory containing the source file.

        Returns:
            Dict: Loaded data structure.

        Raises:
            SettingsError: If file or tab is empty or source not recognized.
        """
        available_sources = Defaults.ConfigFiles.AVAILABLE_SOURCES
        util.validate_selection(
            selection=source,
            valid_selections=available_sources
        )

        if source == 'yml':
            file_name = structure_key + '.yml'
            data = self.load_structured_file(file_name, dir_path)

            if not data:
                msg = f"File '{file_name}' is empty."
                self.logger.error(msg)
                raise exc.SettingsError(msg)

        elif source == 'xlsx':
            file_name = Defaults.ConfigFiles.SETUP_XLSX_FILE
            raw_data = self.excel_tab_to_dataframe(
                file_name, dir_path, structure_key)

            if raw_data.empty:
                msg = f"Excel tab '{structure_key}' is empty."
                self.logger.error(msg)
                raise exc.SettingsError(msg)

            data_pivot_keys = Defaults.DefaultStructures.XLSX_PIVOT_KEYS
            merge_dict = True if \
                structure_key == Defaults.ConfigFiles.SETUP_INFO[2] else False

            skip_process_str = True if structure_key == 'problem' else False

            data = util.pivot_dataframe_to_data_structure(
                data=raw_data,
                primary_key=data_pivot_keys[structure_key][0],
                secondary_key=data_pivot_keys[structure_key][1],
                merge_dict=merge_dict,
                skip_process_str=skip_process_str,
            )

        else:
            msg = "Model settings source not recognized. Available sources: " \
                f"{available_sources}."
            self.logger.error(msg)
            raise exc.SettingsError(msg)

        return data

    def validate_data_structure(
            self,
            data: Dict,
            validation_structure: Dict,
            path: str = '',
    ) -> Dict[str, str]:
        """Validate a data structure against a validation schema.

        Args:
            data (Dict): Data structure to validate.
            validation_structure (Dict): Validation schema.
            path (str, optional): Path for nested validation.

        Returns:
            Dict[str, str]: Dictionary of problems found.
        """
        problems = {}
        optional_label = Defaults.DefaultStructures.OPTIONAL
        any_label = Defaults.DefaultStructures.ANY
        all_optional_fields = False

        if all(
            isinstance(v_exp, tuple) and v_exp[0] == optional_label
            for v_exp in validation_structure.values()
        ):
            all_optional_fields = True

        for k_exp, v_exp in validation_structure.items():
            current_path = f"{path}.{k_exp}" if path else k_exp

            # if no data are passed, all keys must be optional
            if not data:
                if all_optional_fields:
                    continue
                else:
                    problems[current_path] = f"Data structure is empty, but " \
                        "there are mandatory key-value pairs."

            # check for keys and related values
            if isinstance(v_exp, tuple) and v_exp[0] == optional_label:
                optional = True
                expected_value = v_exp[1:]
            else:
                optional = False
                expected_value = v_exp

            # generic keys are checked in the other for loop
            if k_exp == any_label:
                continue

            # check if mandatory keys are missing
            elif k_exp not in data:
                if optional:
                    continue
                problems[current_path] = f"Missing key-value pair."

            # check values types and content for mandatory keys
            else:
                value = data[k_exp]

                if isinstance(expected_value, type):
                    if not isinstance(value, expected_value | NoneType):
                        problems[current_path] = \
                            f"Expected {expected_value}, got {type(value)}"
                    if not optional and not value:
                        problems[current_path] = "Empty value."

                elif isinstance(expected_value, tuple):
                    if all(isinstance(v, type) for v in expected_value):
                        if not any(isinstance(value, v | NoneType) for v in expected_value):
                            problems[current_path] = \
                                f"Expected {expected_value}, got {type(value)}"
                        if not optional and not value:
                            problems[current_path] = "Empty value."

                # check for nested dictionaries
                elif isinstance(expected_value, dict):
                    if isinstance(value, dict):
                        problems.update(
                            self.validate_data_structure(
                                value, expected_value, current_path)
                        )
                    else:
                        problems[current_path] = \
                            f"Expected dict, got {type(value).__name__}"

                else:
                    problems[current_path] = "Unexpected value."

        # in case data is empty, no further checks required
        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key

                if key not in validation_structure:

                    # check for unexpected keys
                    if any_label not in validation_structure:
                        problems[current_path] = "Unexpected key-value pair."

                    # check for nested dictionaries
                    else:
                        if isinstance(validation_structure[any_label], tuple) \
                                and validation_structure[any_label][0] == optional_label:
                            expected_value = validation_structure[any_label][1]
                        else:
                            expected_value = validation_structure[any_label]

                        if isinstance(value, dict):
                            problems.update(
                                self.validate_data_structure(
                                    value, expected_value, current_path)
                            )

        problems = util.remove_empty_items_from_dict(
            problems, empty_values=[{}])

        return problems

    def __repr__(self):
        """Return string representation of FileManager instance."""
        class_name = type(self).__name__
        return f'{class_name}'
