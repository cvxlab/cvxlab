"""Integration tests for different model types.

This module contains integrations tests for different types of models, defined as
fixtures in the 'fixtures' directory.
The tests are parameterized based on settings loaded from a YAML file. The 
settings specify the log level, the test methods to call on each model, and 
the paths and names of the models to test.
"""
import os
import shutil
import atexit

from pathlib import Path

from cvxlab.constants import Constants
from tests.integration.conftest import (
    load_test_settings,
    sanitize_fixture_name,
    create_model_fixture,
    create_test_function,
)


# Constants and paths
tests_settings_file = 'tests_settings.yml'
model_fixture_dir = 'fixtures'
db_name = Constants.ConfigFiles.SQLITE_DATABASE_FILE

root_path = Path(__file__).parent
test_settings_path = Path(root_path, tests_settings_file)
fixtures_dir_path = Path(root_path, model_fixture_dir)

# Create an isolated working directory for test runs
work_dir_path = root_path / ".work"
if work_dir_path.exists():
    shutil.rmtree(work_dir_path, ignore_errors=True)
work_dir_path.mkdir(parents=True, exist_ok=True)


@atexit.register
def _cleanup_work_dir():
    shutil.rmtree(work_dir_path, ignore_errors=True)


# Load test settings and list of models
settings = load_test_settings(test_settings_path)
models_list = os.listdir(fixtures_dir_path)

# Generating testing functions and fixtures dynamically
for model_name in models_list:

    # Prepare a per-model working copy of the fixture
    model_src_path = fixtures_dir_path / model_name
    model_work_path = work_dir_path / model_name
    shutil.copytree(model_src_path, model_work_path)

    # Create a valid test function name
    sanitized_model_name = sanitize_fixture_name(model_name)
    test_func_name = f"test_{sanitized_model_name}"
    fixture_name = f"fixture_{sanitized_model_name}"

    # Create and register model fixture (pointing to the working dir)
    model_fixture = create_model_fixture(
        model_name=model_name,
        models_dir_path=work_dir_path,
        log_level=settings['log_level'],
    )
    model_fixture.__name__ = fixture_name
    globals()[fixture_name] = model_fixture

    # Create the test functions for this specific model
    _test_func = create_test_function(
        model_name=model_name,
        test_func_name=test_func_name,
        fixture_name=fixture_name,
        methods=settings['methods'],
        overrides=settings.get('model_overrides', {}),
    )

    # Add the test function to the module's global namespace
    globals()[test_func_name] = _test_func

# Cleanup temporary variable
del _test_func
