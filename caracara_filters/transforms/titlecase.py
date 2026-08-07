"""Caracara Filters: Titlecase Transform.

This file contains a function that converts a string value to titlecase.  Use this
transform for filters where the API's FQL field is case-sensitive but user input
may vary in capitalisation (e.g. ``platform_name``).
"""

from typing import Union


def titlecase_transform(value: Union[str, list]) -> Union[str, list]:
    """Return the value titlecased; non-string values are returned unchanged."""
    if isinstance(value, str):
        return value.title()
    return value
