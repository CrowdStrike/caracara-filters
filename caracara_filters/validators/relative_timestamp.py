"""Caracara Filters: Relative Timestamp Validator.

This file contains a regex validator to ensure that the input matches spec.
"""

from caracara_filters.common import ISO8601_TIMESTAMP_RE, RELATIVE_TIMESTAMP_RE


def relative_timestamp_validator(timestamp_input: str) -> bool:
    """Check if an input matches a relative timestamp structure."""
    if RELATIVE_TIMESTAMP_RE.match(timestamp_input) is not None:
        return True

    if ISO8601_TIMESTAMP_RE.match(timestamp_input) is not None:
        return True

    return False
