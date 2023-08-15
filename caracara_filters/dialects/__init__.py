__all__ = [
    'default_filter',
    'rebase_filters_on_default',
    'DIALECTS',
    'HOST_FILTERS',
]

from caracara_filters.dialects._base import default_filter
from caracara_filters.dialects._merge import rebase_filters_on_default
from caracara_filters.dialects._base import BASE_FILTERS
from caracara_filters.dialects.hosts import HOST_FILTERS

DIALECTS = {
    "base": BASE_FILTERS,
    "hosts": HOST_FILTERS,
}
