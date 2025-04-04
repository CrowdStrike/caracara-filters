"""Caracara Filters: Boolean validator.

This file contains a validator to ensure that the input is or represents a boolean value.
"""

from typing import Union


def boolean_validator(boolean_input: Union[bool, str], accept_yes_no=False):
    """Validate if a filter value is a boolean."""
    # If the object is a Python boolean, this is always true
    if boolean_input in [True, False]:
        return True

    # If the input is a string but evaluates to true or false, we can treat it as a boolean
    # since it'll be represented as a string when converted to FQL
    if isinstance(boolean_input, str):
        if boolean_input.lower() in ["true", "false"]:
            return True

        # Some filters accept "yes" or "no" as valid boolean inputs (such as RFM)
        if accept_yes_no and boolean_input.lower() in ["yes", "no"]:
            return True

    return False
