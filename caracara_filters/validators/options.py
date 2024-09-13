"""Caracara Filters: Options Validator.

This code file contains a standard validator that ensures an input is one of a pre-set list
of allowable options.
"""
from typing import Any, List


def options_validator(options: List[Any], chosen_option: Any, case_sensitive: bool = True) -> bool:
    """Check if an option passed to the filter is within a pre-set list of options."""
    if isinstance(chosen_option, str) and not case_sensitive:
        lower_options = [x.lower() for x in options]
        return chosen_option.lower() in lower_options

    return chosen_option in options
