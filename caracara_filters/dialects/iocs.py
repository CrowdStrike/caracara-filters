"""Caracara Filters: IOC dialect.

This module contains filters that are specific to the IOC API.
"""
from functools import partial
from typing import Any, Dict, Union

from caracara_filters.common import PLATFORMS
from caracara_filters.dialects._base import default_filter
from caracara_filters.dialects._base import rebase_filters_on_default
from caracara_filters.transforms import relative_timestamp_transform
from caracara_filters.validators import boolean_validator, options_validator, relative_timestamp_validator


IOCS_ACTIONS = [
    "no_action",
    "allow",
    "prevent",
    "detect",
    "prevent_no_ui",
]

iocs_action_filter = {
    "fql": "action",
    "validator": partial(options_validator, IOCS_ACTIONS, case_sensitive=False),
    "transform": lambda action: action.lower(),
    "help": "Filter by IOC action."
}

iocs_created_by_filter = {
    "fql": "created_by",
    "help": "Filter by IOC author."
}

iocs_expiration_filter = {
    "fql": "expiration",
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
    "help": (
        "This filter accepts two types of parameter: a fixed ISO 8601 timestamp (such as "
        "2020-01-01:01:00:00Z), or a relative timestamp such as -30m. -30m means time now, "
        "minus thirty minutes. An example is expiration__LTE=+30d combined with expired=False, "
        "to stipulate all IOCs that are expiring within the next 30 days."
    ),
}

iocs_expired_filter = {
    "fql": "expired",
    "data_type": Union[bool, str],
    "validator": boolean_validator,
    "help": "Filter by expiration status of IOCs."
}

iocs_platform_filter = {
    "fql": "platforms",
    "validator": partial(options_validator, PLATFORMS, case_sensitive=False),
    "transform": lambda platform: platform.lower(),  # The IOC API only matches platform names in lower case.
    "help": "Filter by the platforms this IOC applies to."
}

IOCS_SEVERITIES = [
    "critical",
    "high",
    "medium",
    "low",
    "informational"
]

iocs_severity_filter = {
    "fql": "severity",
    "validator": partial(options_validator, IOCS_SEVERITIES, case_sensitive=False),
    "help": "Filter by IOC severity.",
}

iocs_tags_filter = {
    "fql": "tags",
    "help": "Filter by IOC tags."
}

IOCS_TYPES = [
    "all_subdomains",
    "domain",
    "ipv4",
    "ipv6",
    "md5",
    "sha256",
]

iocs_type_filter = {
    "fql": "type",
    "validator": partial(options_validator, IOCS_TYPES, case_sensitive=False),
    "transform": lambda type: type.lower(),  # The IOC API only matches types in lower case.
    "help": "Filter by IOC type.",
}

iocs_value_filter = {
    "fql": "value",
    "help": "Filter by IOC value (e.g. domain, hash or IP address)"
}

IOCS_FILTERS: Dict[str, Dict[str, Any]] = {
    "action": iocs_action_filter,
    "created_by": iocs_created_by_filter,
    "createdby": iocs_created_by_filter,
    "expiration": iocs_expiration_filter,
    "expired": iocs_expired_filter,
    "platform": iocs_platform_filter,
    "severity": iocs_severity_filter,
    "tags": iocs_tags_filter,
    "type": iocs_type_filter,
    "value": iocs_value_filter,
}
rebase_filters_on_default(default_filter, IOCS_FILTERS)
