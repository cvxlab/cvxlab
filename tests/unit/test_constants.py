import pytest
from cvxlab.constants import Constants


def test_getattr_method():
    assert Constants.__getattr__('SETUP_XLSX_FILE') == 'model_settings.xlsx'
    assert Constants.__getattr__('NAME') == 'name'
    with pytest.raises(AttributeError):
        Constants.__getattr__('NON_EXISTENT_CONSTANT')
