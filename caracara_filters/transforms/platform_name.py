"""Caracara Filters: Platform Name Transform.

This file contains a function that converts a platform name to match Falcon.
Use this transform for filtering on a platform name where the API's FQL field
is case-sensitive but user input may vary in capitalisation (e.g. ``windows``).
"""

from typing import Union

from caracara_filters.common import PLATFORMS


def platform_name_transform(value: Union[str, list]) -> Union[str, list]:
    """Return the platform name expected by Falcon or the original value if unsupported."""
    if isinstance(value, str):
        for platform in PLATFORMS:
            if value.lower() == platform.lower():
                return platform
    return value
