"""Caracara Filters: Boolean validator.

This file contains a validator to ensure that the input is or represents a boolean value.
"""
from typing import Union

def boolean_validator(boolean_input: Union[bool, str]):
    if isinstance(boolean_input, bool):
        return True
    elif isinstance(boolean_input, str):
        return boolean_input.lower() in ["true", "false"]
    return False