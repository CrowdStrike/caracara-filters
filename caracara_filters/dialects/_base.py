"""Caracara Filters: Base Dialect.

This file contains a base set of 'common' FQL parameters that may be used across multiple
dialects.
"""
from typing import Any, Dict

from caracara_filters.dialects._merge import rebase_filters_on_default
from caracara_filters.transforms import identity_transform
from caracara_filters.validators import identity_validator

default_filter = {
    "data_type": str,
    "operator": "EQUAL",
    "multivariate": True,
    "transform": identity_transform,
    "validator": identity_validator,
    "valid_operators": ['EQUAL'],
}

name_filter = {
    "fql": "name",
    "help": (
        "This filter accepts any string to be passed as a 'name' attribute. Examples of named "
        "objects in FQL include response and prevention policies."
    ),
}

BASE_FILTERS: Dict[str, Dict[str, Any]] = {
    "name": name_filter,
}

rebase_filters_on_default(default_filter, BASE_FILTERS)
