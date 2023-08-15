"""Caracara Filters: Dialects.

FQL's dialect varies based on the API in use. For example, Spotlight and Hosts show similar
data but with different property names and paths. Each dialect is defined here, and matched to
a dictionary of filters by string mapping.
"""

__all__ = [
    'DIALECTS',
    'HOSTS_FILTERS',
    'PREVENTION_POLICIES_FILTERS',
    'RTR_FILTERS',
    'USERS_FILTERS',
    'default_filter',
    'rebase_filters_on_default',
]

from caracara_filters.dialects._base import BASE_FILTERS
from caracara_filters.dialects._base import default_filter
from caracara_filters.dialects._merge import rebase_filters_on_default
from caracara_filters.dialects.hosts import HOSTS_FILTERS
from caracara_filters.dialects.prevention_policies import PREVENTION_POLICIES_FILTERS
from caracara_filters.dialects.rtr import RTR_FILTERS
from caracara_filters.dialects.users import USERS_FILTERS

DIALECTS = {
    "base": BASE_FILTERS,
    "hosts": HOSTS_FILTERS,
    "prevention_policies": PREVENTION_POLICIES_FILTERS,
    "rtr": RTR_FILTERS,
    "users": USERS_FILTERS,
}
