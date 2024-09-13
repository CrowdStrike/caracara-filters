"""Caracara Filters: Filter Builder.

This code file will merge the filter dictionaries using mergedeep
so that a resultant filter can exist.
"""

from typing import Any, Dict


def rebase_filters_on_default(
    default_filter: Dict[str, Any], filters: Dict[str, Dict[str, Any]]
) -> None:
    """Rebase every filter on a default base filter.

    This function originally used the mergedeep library, but that faced issues pickling the strange
    data types in use here. Instead, this rebase function will only work down to one single level of
    dictionary. It is not a recursive function, and does not need to be, so long as we do not need
    to go to the level of nested dictionaries.
    """
    for filter_name, filter_dict in filters.items():
        for default_filter_prop_k, default_filter_prop_v in default_filter.items():
            if default_filter_prop_k not in filter_dict:
                filters[filter_name][default_filter_prop_k] = default_filter_prop_v
