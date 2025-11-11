import pytest
from cvxlab.backend.set_table import SetTable


class DummyLogger:
    def get_child(self, name):
        return self


def test_settable_constructor_minimal():
    logger = DummyLogger()
    set_key = "myset"
    set_table = SetTable(logger=logger, key_name=set_key)

    assert set_table.name == set_key
    assert set_table.table_name == "_set_MYSET"
    assert set_table.logger is logger
    assert set_table.split_problem is False
    assert set_table.data is None
