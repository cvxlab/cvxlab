"""Unit tests for the Constants class in cvxlab.constants module."""

from cvxlab.constants import Constants
from tests.unit.conftest import run_test_cases


def test_getattr_method():
    """Test the '__getattr__' method of the Constants class."""

    test_cases = [
        ('SETUP_XLSX_FILE', 'model_settings.xlsx', None),
        ('NAME', 'name', None),
        ('NON_EXISTENT_CONSTANT', None, AttributeError),
        ('NONE_SYMBOLS', [None, 'nan', 'None', 'null', '', [], {}], None),
    ]

    run_test_cases(Constants.__getattr__, test_cases)
