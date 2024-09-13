"""Caracara Filters: Identity Transform.

This file contains a function that merely returns its input; it's intended to be the
default transform for data inputs that do not need to be massaged.
"""

from typing import Any


def identity_transform(value: Any) -> Any:
    """Return back the same value, as no transform is required."""
    return value
