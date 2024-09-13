"""Caracara Filters: Prevention Policies Dialect.

This module contains filters that are specific to the Prevention Policies API.
This code may be merged into a more generic policies dialect, depending on the overlaps
in data structures.
"""
from caracara_filters.dialects._base import default_filter
from caracara_filters.dialects._base import rebase_filters_on_default

PREVENTION_POLICIES_FILTERS = {}
rebase_filters_on_default(default_filter, PREVENTION_POLICIES_FILTERS)
