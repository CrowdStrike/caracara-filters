"""Caracara Filters: Options Validator.

This code file contains a standard validator that ensures an input is one of a pre-set list
of allowable options.
"""
from typing import Any, List


def options_validator(options: List[Any], chosen_option: Any) -> bool:
    """Check if an option passed to the filter is within a pre-set list of options.

    If a list of choices is passed in, we bail out if any of those items are not in the list.
    If all items fail to result in a bail out, we return True.

    Technically, we should probably test whether this item is multivariate here. However, we
    perform that check in fql.py within the FQLGenerator function.
    """
    if isinstance(chosen_option, list):
        for chosen_option_item in chosen_option:
            if chosen_option_item not in options:
                return False
        return True

    return chosen_option in options
