"""Module defining the DotDict class.

The DotDict class extends the standard Python dictionary to allow access to values
using both key-based indexing (e.g., dict_instance['key']) and dot notation
(e.g., dict_instance.key). All standard dictionary methods are inherited.
"""

from typing import Any


class DotDict(dict):
    """DotDict class extends the standard dictionary with attribute-style access.

    This class allows values to be accessed and modified using both key-based
    indexing and dot notation. All standard dictionary methods are inherited.
    """

    def __getattr__(self, name: str) -> Any:
        """Retrieve the value associated with the given attribute name.

        Args:
            name (str): The name of the attribute to retrieve.

        Returns:
            Any: The value associated with the attribute.

        Raises:
            AttributeError: If the attribute does not exist in the dictionary.
        """
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(f"No such attribute: {name}") from error

    def __setattr__(self, name: str, value: Any) -> None:
        """Set the value associated with the given attribute name.

        Args:
            name (str): The name of the attribute to set.
            value (Any): The value to associate with the attribute.
        """
        self[name] = value

    def __delattr__(self, name: str) -> None:
        """Delete the attribute with the given name.

        Args:
            name (str): The name of the attribute to delete.

        Raises:
            AttributeError: If the attribute does not exist in the dictionary.
        """
        try:
            del self[name]
        except KeyError as error:
            raise AttributeError(f"No such attribute: {name}") from error
