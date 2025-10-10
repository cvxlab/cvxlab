"""Module defining the exceptions in CVXlab package.

This module includes all the exceptions classes necessary to clearly identify
exceptions in executing the package.
"""


class CVXLabError(Exception):
    """Base exception for CVXlab package.

    Attributes:
        message (str): Explanation of the error.
    """

    def __init__(self, message=None):
        """Initialize CVXLabError with a default or custom message.

        Args:
            message (_type_, optional): Custom error message. Defaults to None.
        """
        if message is None:
            message = getattr(self, 'default_message', 'CVXLab error.')
        self.message = message
        super().__init__(self.message)


class ModelFolderError(CVXLabError):
    """Raise and handle errors related to the model folder."""

    default_message = 'Model directory error.'


class ConceptualModelError(CVXLabError):
    """Raise and handle errors related to the conceptual model."""

    default_message = 'Conceptual Model error.'


class SettingsError(CVXLabError):
    """Raise and handle errors related to settings configurations."""

    default_message = 'Settings error.'


class MissingDataError(CVXLabError):
    """Raise and handle errors related to missing data in model input."""

    default_message = 'Missing data error.'


class OperationalError(CVXLabError):
    """Raise and handle operational errors."""

    default_message = 'Operational error.'


class IntegrityError(CVXLabError):
    """Raise and handle integrity errors in sqlite databases."""

    default_message = 'Integrity error'


class NumericalProblemError(CVXLabError):
    """Raise and handle numerical problem errors."""

    default_message = 'Numerical problem error'


class TableNotFoundError(CVXLabError):
    """Raise and handle database table not found errors."""

    default_message = 'Table not found.'


class ResultsError(CVXLabError):
    """Raise and handle errors related to model results."""

    default_message = 'Results error.'
