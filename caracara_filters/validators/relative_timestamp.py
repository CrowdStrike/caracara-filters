"""Caracara Filters: Relative Timestamp Validator.

This file contains a regex validator to ensure that the input matches spec.
"""

from caracara_filters.common import RELATIVE_TIMESTAMP_RE


def relative_timestamp_validator(timestamp_input: str) -> bool:
    """Check if an input matches a relative timestamp structure."""
    return RELATIVE_TIMESTAMP_RE.match(timestamp_input) is not None
