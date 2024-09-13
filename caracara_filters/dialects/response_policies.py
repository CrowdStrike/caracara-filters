"""Caracara Filters: Response Policies Dialect.

This module contains filters that are specific to the Response Policies API.
This code may be merged into a more generic policies dialect, depending on the overlaps
in data structures.
"""

from caracara_filters.dialects._base import default_filter, rebase_filters_on_default

RESPONSE_POLICIES_FILTERS = {}
rebase_filters_on_default(default_filter, RESPONSE_POLICIES_FILTERS)
