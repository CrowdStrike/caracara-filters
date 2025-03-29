"""Caracara Filters: Filter Templates.

This file can contain templates for filters that follow very common formats and accept the same
data types, such as relative timestamps.
"""

from caracara_filters.transforms.relative_timestamp import relative_timestamp_transform
from caracara_filters.validators.relative_timestamp import relative_timestamp_validator

RELATIVE_TIMESTAMP_FILTER_TEMPLATE = {
    "multivariate": False,
    "operator": "GTE",
    "valid_operators": [
        "EQUAL",
        "GT",
        "GTE",
        "LT",
        "LTE",
    ],
    "transform": relative_timestamp_transform,
    "validator": relative_timestamp_validator,
}
