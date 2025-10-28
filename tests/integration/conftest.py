"""Pytest configuration for integration tests."""
import os
import yaml
import pytest
import shutil

from pathlib import Path
from typing import Dict

from cvxlab import Model

_model_instances = {}


def load_test_settings(settings_file: str | Path) -> Dict:
    """Load test settings from a YAML file.

    Args:
        settings_file (str | Path): Path to the settings YAML file.

    Returns:
        Dict: Dictionary containing the loaded settings.

    Raises:
        FileNotFoundError: If the settings file does not exist.
    """
    settings_path = Path(settings_file)

    if not settings_path.exists():
        raise FileNotFoundError(
            f"Expected settings file does not exist: '{settings_path}'")

    with open(settings_path, 'r') as file:
        settings = yaml.safe_load(file)

    return settings


def sanitize_fixture_name(name: str) -> str:
    """Sanitize a string to be used as a valid pytest fixture name.

    Args:
        name (str): The original name.

    Returns:
        str: The sanitized fixture name.
    """
    return name.replace('-', '_').replace(' ', '_').replace('.', '_')


def create_model_fixture(
        model_name: str,
        models_dir_path: Path | str,
        log_level: str
):
    """Create and returns a Model instance for the specified model name."""
    @pytest.fixture(scope='module')
    def model_fixture():
        if model_name not in _model_instances:
            _model_instances[model_name] = Model(
                model_dir_name=model_name,
                main_dir_path=models_dir_path,
                log_level=log_level,
                use_existing_data=True,
            )
        return _model_instances[model_name]

    return model_fixture


def create_test_function(
        model_name: str,
        test_func_name: str,
        fixture_name: str,
        methods: Dict,
        overrides: Dict = None,
) -> callable:
    """Create a pytest test function for a specific model.

    The test function calls the specified methods on the model.

    Args:
        model_name (str): The name of the model to test.
        test_func_name (str): The name to give the test function.
        fixture_name (str): The name of the model fixture to use.
        models_dir_path (Path | str): The directory path where the models are located.
        methods (Dict): A dictionary containing the methods to call on the model 
            and the arguments to pass to each method.
        overrides (Dict): Optional dictionary containing model-specific overrides
            for method arguments. Structure: {model_name: {method_name: kwargs}}

    Returns:
        function: A pytest test function.

    Notes:
        The test function is parameterized with the method names.
        This creates a hierarchical structure in VS Code: test_model_name -> method_name.
        All test methods share the same model instance via a fixture.
        Model-specific overrides can be provided to customize method arguments per model.
        If a method call raises an exception, the test function fails the test with 
            a message indicating the name of the model and method.
    """
    overrides = overrides or {}

    # Get model-specific method overrides if they exist
    model_specific_methods = {'initialize_model': {}}

    for method_name, method_kwargs in methods.items():
        if model_name in overrides and method_name in overrides[model_name]:
            # Merge default kwargs with model-specific overrides
            model_specific_methods[method_name] = {
                **method_kwargs, **overrides[model_name][method_name]}
        else:
            model_specific_methods[method_name] = method_kwargs

    def test_func(
            request: pytest.FixtureRequest,
            method_name: str,
    ):
        model = request.getfixturevalue(fixture_name)

        # special handling for model initiazation
        if method_name == 'initialize_model':
            assert model is not None, f"Failed to initialize model: {model_name}"
            # further checks can be added here
            return

        # regular method calls
        method_kwargs = model_specific_methods[method_name]

        try:
            getattr(model, method_name)(**method_kwargs)
        except Exception as e:
            pytest.fail(f"Test failed: {model_name} - {method_name}: {str(e)}")

    test_func = pytest.mark.parametrize(
        "method_name",
        model_specific_methods.keys(),
        ids=lambda x: x
    )(test_func)

    test_func.__name__ = test_func_name
    return test_func
