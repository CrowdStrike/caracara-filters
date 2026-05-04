"""Caracara Filters: Lowercase Transform.

This file contains a function that converts a string value to lowercase.  Use this
transform for filters where the API's FQL field is case-insensitive and a canonical
lowercase representation is required (e.g. ``platform``).
"""

from typing import Union


def lowercase_transform(value: Union[str, list]) -> Union[str, list]:
    """Return the value lowercased; non-string values are returned unchanged."""
    if isinstance(value, str):
        return value.lower()
    return value
