"""Caracara Filters: Identity Validator.

This is a simple validator that always returns True.
"""
from typing import Any


def identity_validator(_: Any) -> bool:
    """Return True if no input validation (aside from type) is required."""
    return True
