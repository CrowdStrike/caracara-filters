"""Caracara Filters: Hosts Dialect.

This module contains filters that are specific to the Hosts API.
"""
from functools import partial
from typing import Any, Dict

from caracara_filters.common import PLATFORMS
from caracara_filters.dialects._base import default_filter
from caracara_filters.dialects._base import rebase_filters_on_default
from caracara_filters.transforms import relative_timestamp_transform
from caracara_filters.validators import options_validator
from caracara_filters.validators import relative_timestamp_validator


_containment_value_map = {
    "Contained": "contained",
    "Containment Pending": "containment_pending",
    "Not Contained": "normal",
}

_role_map = {
    "DC": "Domain Controller",
    "Server": "Server",
    "Workstation": "Workstation",
}


def user_readable_string_transform(map_dict: Dict[str, str], input_str: str) -> str:
    """Map a human-readable string to a machine-readable one."""
    if input_str in map_dict.values():
        return input_str

    if input_str in map_dict:
        return map_dict[input_str]

    raise ValueError("An invalid filter input was provided.")


host_contained_filter = {
    "fql": "status",
    "help": "Filter by a host's network containment status.",
    "multivariate": False,
    "transform": partial(user_readable_string_transform, _containment_value_map),
    "validator": partial(options_validator, [
        *_containment_value_map.keys(),
        *_containment_value_map.values(),
    ]),
}

host_domain_filter = {
    "fql": "machine_domain",
    "help": (
        "This filter accepts an AD domain, e.g. GOODDOMAIN or gooddomain.company.com. You can "
        "also provide multiple domains as a Python list or comma delimited string"
    ),
}

host_group_id_filter = {
    "fql": "groups",
    "help": (
        "This filter accepts one or more Group IDs as either one string, or as a comma "
        "delimited list of strings. For example, 075e03f5e5c04d83b4831374e7dc01c3 would "
        "target hosts within the group with ID 075e03f5e5c04d83b4831374e7dc01c3 only, or "
        "abcdefg123,abcdefg321 would target hosts in either group."
    ),
}

host_hostname_filter = {
    "fql": "hostname",
    "help": (
        "Provide either a single hostname string, or a list of hostnames via a comma delimited "
        "string or Python list. For example, you can omit two specific hosts with "
        "Hostname__NOT=HOST1,HOST2."
    ),
}

host_last_seen_filter = {
    "fql": "last_seen",
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
        "minus thirty minutes, so is best combined with an operator such as GTE. A popular "
        "example is LastSeen__GTE=-30m, to stipulate all hosts that have been online in the "
        "past half hour (i.e. are likely to be online)."
    ),
}

host_first_seen_filter = {
    "fql": "first_seen",
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
        "minus thirty minutes, so is best combined with an operator such as GTE. One example is "
        "FirstSeen__GTE=-1d, to filter for all new hosts that have been added to Falcon within "
        "the past 1 day."
    ),
}

host_local_ip_address_filter = {
    "fql": "local_ip",
    "help": (
        "This filter accepts an IP address string associated with a network card, e.g. "
        "172.16.1.2 or 172.16.* to cover the /16 range. You can also comma delimit strings "
        "for multiple matches, e.g., 172.16.1.2,172.16.1.3 to target hosts with each of those "
        "IPs, or provide a Python list of IP strings."
    ),
}

host_os_filter = {
    "fql": "platform_name",
    "validator": partial(options_validator, PLATFORMS),
    "help": f"Filter by host operating system (options: {str(PLATFORMS)}).",
}

host_os_version_filter = {
    "fql": "os_version",
    "help": (
        "This filter accepts a name of an operating system version and can be supplied many "
        "times. For example, Windows 7, RHEL 7.9, Catalina (10.15), etc."
    ),
}

host_role_filter = {
    "fql": "product_type_desc",
    "transform": partial(user_readable_string_transform, _role_map),
    "validator": partial(options_validator, [*_role_map.keys(), *_role_map.values()]),
    "help": "Filter by system role (i.e., DC, Server, Workstation).",
}

host_site_filter = {
    "fql": "site_name",
    "help": (
        "This filter accepts one or more site names as either one string, or as a comma delimtied "
        "list of strings. For example, London,Manchster1,Manchester2 would target hosts within "
        "any of those three sites."
    ),
}

host_tag_filter = {
    "fql": "tags",
    "help": (
        "This filter accepts one or more sensor tags as either one string, or as a comma "
        "delimited list of strings. For example, SensorGroupingTags/Tag1,FalconGroupingTags/Tag2 "
        "to filter by hosts with one of those tags."
    ),
}

host_ou_filter = {
    "fql": "ou",
    "help": (
        "This filter accepts an Organisational Unit (OU) name as a string. You can also comma "
        "delimit OUs for multiple matches, e.g. UKServers,USServers to target hosts within any of "
        "those OUs. Programmatically, you can pass a Python list of OUs."
    ),
}

HOST_FILTERS: Dict[str, Dict[str, Any]] = {
    "contained": host_contained_filter,
    "domain": host_domain_filter,
    "groupid": host_group_id_filter,
    "hostname": host_hostname_filter,
    "lastseen": host_last_seen_filter,
    "firstseen": host_first_seen_filter,
    "localip": host_local_ip_address_filter,
    "os": host_os_filter,
    "osversion": host_os_version_filter,
    "role": host_role_filter,
    "site": host_site_filter,
    "tag": host_tag_filter,
}

rebase_filters_on_default(default_filter, HOST_FILTERS)
