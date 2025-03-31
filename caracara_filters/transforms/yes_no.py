"""Caracara Filters: Yes/No Transform.

This file contains a function that will convert a boolean input to either "yes" or "no" for filters
that expect this type of input (such as RFM).
"""

from typing import Union


def yes_no_transform(value: Union[str, bool]) -> str:
    """Return either "yes" or "no"."""
    if isinstance(value, bool):
        if value is True:
            return "yes"
        return "no"

    if isinstance(value, str):
        if value.lower() in ["true", "yes"]:
            return "yes"
        return "no"

    raise ValueError(f"{str(value)} is not a boolean or a string")
