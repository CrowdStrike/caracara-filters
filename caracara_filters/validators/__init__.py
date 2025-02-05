"""Caracara Filters: Validators.

A validator is applied to an input before the transform is executed, so that it can decide whether
to accept the user/developer's input before proceeding.
This ensure that, after optional transformation, the filter will be able to return a reasonable
string that will be valid FQL, and in turn recognised by the Falcon API.
"""
__all__ = [
    'boolean_validator',
    'identity_validator',
    'options_validator',
    'relative_timestamp_validator',
]

from caracara_filters.validators.boolean import boolean_validator
from caracara_filters.validators.identity import identity_validator
from caracara_filters.validators.options import options_validator
from caracara_filters.validators.relative_timestamp import relative_timestamp_validator
