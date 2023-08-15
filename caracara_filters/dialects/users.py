"""Caracara Filters: Users Dialect.

This module contains filters that are specific to the User Management API.
"""
from typing import Any, Dict

from caracara_filters.dialects._base import default_filter
from caracara_filters.dialects._base import rebase_filters_on_default


users_assigned_cids_filter = {
    "fql": "assigned_cids",
    "help": "Filter by CID(s) assigned to a user.",
}

users_cid_filter = {
    "fql": "cid",
    "help": "Filter by users' home CID.",
}

users_first_name_filter = {
    "fql": "first_name",
    "help": "Filter by a user's first name.",
}

users_last_name_filter = {
    "fql": "last_name",
    "help": "Filter by a user's last name.",
}


USERS_FILTERS: Dict[str, Dict[str, Any]] = {
    "assignedcids": users_assigned_cids_filter,
    "assigned_cids": users_assigned_cids_filter,  # pythonic
    "cid": users_cid_filter,
    "firstname": users_first_name_filter,
    "first_name": users_first_name_filter,  # pythonic
    "lastname": users_last_name_filter,
    "last_name": users_last_name_filter,  # pythonic
}  

rebase_filters_on_default(default_filter, USERS_FILTERS)
