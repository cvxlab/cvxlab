import ast
import re
from typing import Any, Iterable, List, Optional


def str_to_be_evaluated(value: str) -> bool:
    """
    Checks if a string should be evaluated (i.e. if it is a dictionary, list or
    a tuple). Raises ValueError if parentheses, brackets, or braces are not
    correctly opened/closed.
    """
    if not isinstance(value, str):
        raise TypeError(f'Passed value {value} must be a string.')

    stack = []
    matching = {')': '(', ']': '[', '}': '{'}

    for char in value:
        if char in matching.values():
            stack.append(char)
        elif char in matching.keys():
            if stack == [] or matching[char] != stack.pop():
                raise ValueError(f"Unmatched parentheses in string: {value}")

    if stack:
        raise ValueError(f"Unmatched parentheses in string: {value}")

    return bool(re.match(r'^\s*[\{\[\(]', value))


def add_brackets(value: str) -> str | None:
    """
    If a string represents a list or a dict structure without brackets,
    add open/close brackets and return a modified str.
    If a string represents a list or a dict with brackets, no actions.
    If a string is not representing any of the above, no actions.
    If other types are passed, no actions.
    """
    if not isinstance(value, str):
        raise TypeError(f'Passed value {value} must be a string.')

    # check for unmatched brackets
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}
    for char in value:
        if char in matching.values():
            stack.append(char)
        elif char in matching.keys():
            if not stack or matching[char] != stack.pop():
                raise ValueError(f"Unmatched parentheses in string: {value}")
    if stack:
        raise ValueError(f"Unmatched parentheses in string: {value}")

    # check if the string is a list or dict without brackets
    if ',' in value and not re.match(r'^\s*[\{\[\(]', value):
        items = [item.strip() for item in value.split(',')]

        if ':' in items[0]:
            # handle comma-separated pairs of key-value items
            value = '{' + ', '.join(items) + '}'
        else:
            # handle comma-separated items
            value = '[' + ', '.join(items) + ']'

    # check if the string is a dict without brackets
    if ':' in value and not re.match(r'^\s*[\{\[\(]', value):
        items = [item.strip() for item in value.split(':')]
        value = '{' + ': '.join(items) + '}'

    return value


def add_quotes(value: str) -> str:
    """
    Converts all unquoted symbols into quoted symbols.

    """
    if not isinstance(value, str):
        raise TypeError(f'Passed value {value} must be a string.')

    # Split the string by commas and strip whitespace
    items = [
        item.strip()
        for item in re.split(r'(\s*[:,\[\]\{\}\(\)]\s*)', value)
    ]

    # Enclose each item in quotes if not already quoted and not a symbol
    quoted_items = []
    for item in items:
        if item and \
                not re.match(r'^\s*[:,\[\]\{\}\(\)]\s*$', item) and \
                not (item.startswith("'") and item.endswith("'")) and \
                not re.match(r'^-?\d+(\.\d+)?$', item):
            item = f"'{item}'"
        quoted_items.append(item)

    # Join the quoted items back into a single string
    result = ''.join(quoted_items)

    # Add spaces after commas and colons
    for item in [',', ':']:
        result = result.replace(f"{item}", item+' ')

    return result


def evaluate_bool(value: Any) -> Any:
    """
    parse a generic expression and find str representing bool (in bool_map dict)
    and convert them to bool
    """
    bool_map = {
        'true': True, 'True': True, 'TRUE': True,
        'false': False, 'False': False, 'FALSE': False,
    }

    if isinstance(value, str):
        return bool_map.get(value, value)
    elif isinstance(value, dict):
        return {k: evaluate_bool(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [evaluate_bool(item) for item in value]
    elif isinstance(value, Iterable):
        return type(value)(evaluate_bool(item) for item in value)
    else:
        return value


def process_str(value: Any) -> Any:

    # if value is not a string, return it as is
    if not isinstance(value, str):
        return value

    # add brackets in case value is a string representing list | dict without brackets
    value = add_brackets(value)

    # in case the string is a list | dict, add quotes to all items and evaluate it
    if str_to_be_evaluated(value):
        value = add_quotes(value)
        try:
            value = ast.literal_eval(value)
        except ValueError as e:
            raise ValueError(
                f"Malformed string cannot be evaluated: '{value}'") from e

    # in case there are str representing bool, convert to bool
    value = evaluate_bool(value)

    return value


def balanced_parentheses(parentheses_list: List[str]) -> bool:
    """
    Check if the parentheses in a list are balanced.
    """
    stack = []
    matching = {')': '('}

    for char in parentheses_list:
        if char in matching.values():
            stack.append(char)
        elif char in matching.keys():
            if not stack or matching[char] != stack.pop():
                return False

    return not stack


def extract_tokens_from_expression(
    expression: str,
    pattern: str = None,
    tokens_to_skip: Optional[List[str]] = [],
) -> List[str]:
    """
    Parses and extracts variable names from a symbolic expression, excluding
    any non-allowed tokens.
    This method uses regular expressions to identify potential variable names
    within the given expression and filters out any tokens that are designated
    as non-allowed, such as mathematical operators or reserved keywords.

    Parameters:
        expression (str): The symbolic expression from which to extract
            variable names.
        non_allowed_tokens (Optional[List[str]]): A list of tokens that should
            not be considered as variables. Default is an empty list.
        first_char_pattern (str): A regex pattern that defines the first
            character of a valid variable name.
        other_chars_pattern (str): A regex pattern that defines the subsequent
            characters of a valid variable name.
        tokens_to_skip (Optional[List[str]]): A list of tokens to skip when
            extracting variable names. Default is an empty list.
    Returns:
        List[str]: A list of valid variable names extracted from the expression.
    """
    if not isinstance(expression, str):
        raise TypeError(f'Passed expression {expression} must be a string.')

    if not isinstance(tokens_to_skip, list):
        raise TypeError(
            f'Passed tokens_to_skip {tokens_to_skip} must be a list.')

    tokens = []

    if isinstance(pattern, list):
        for pat in pattern:
            tokens += re.findall(pat, expression)
    elif isinstance(pattern, str):
        tokens = re.findall(pattern, expression)
    else:
        raise TypeError(
            f'Passed pattern {pattern} must be a string or a list of strings.')

    allowed_tokens = [token for token in tokens if token not in tokens_to_skip]

    return allowed_tokens
