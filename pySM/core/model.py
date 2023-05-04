from pathlib import Path
from pySM.log_exc.logger import Logger
from pySM.util.file_manager import FileManager
from pySM.core.database import Database
from pySM.core.problem import Problem


class Model:

    def __init__(
            self,
            logger: Logger,
            files: FileManager,
            file_settings_name: str,
            file_settings_dir_path: str,
    ) -> None:

        self.logger = logger.getChild(__name__)
        self.logger.info(f"Generation of '{str(self)}' object.")

        self.files = files

        self.model_settings = self.files.load_file(
            file_name=file_settings_name,
            dir_path=file_settings_dir_path
        )

        self.database_settings = self.model_settings['database_settings']

        self.model_dir_path = Path(
            self.model_settings['model_data_folder_path'],
            self.model_settings['model_name']
        )

        self.files.create_dir(self.model_dir_path)

        self.database = Database(
            logger=self.logger,
            files=self.files,
            database_dir_path=self.model_dir_path,
            database_name='database.db',
            database_settings=self.database_settings,
        )

        self.problem = Problem(
            logger=self.logger,
            files=self.files,
            problem_settings=self.model_settings['problem_settings'],
        )

        self.logger.info(f"'{str(self)}' generated.")

    def __str__(self):
        class_name = type(self).__name__
        return f'{class_name}'

    def model_cleanup(self):
        self.files.erase_dir(self.model_dir_path)

    def load_sets(self):
        self.sets = self.database.load_sets()
