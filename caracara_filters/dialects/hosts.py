"""Caracara Filters: Hosts Dialect.

This module contains filters that are specific to the Hosts API.
"""

from functools import partial
from typing import Any, Dict

from caracara_filters.common.templates import RELATIVE_TIMESTAMP_FILTER_TEMPLATE
from caracara_filters.dialects._base import default_filter, rebase_filters_on_default
from caracara_filters.validators import options_validator

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


hosts_contained_filter = {
    "fql": "status",
    "help": "Filter by a host's network containment status.",
    "transform": partial(user_readable_string_transform, _containment_value_map),
    "validator": partial(
        options_validator,
        [
            *_containment_value_map.keys(),
            *_containment_value_map.values(),
        ],
    ),
}

hosts_device_id_filter = {
    "fql": "device_id",
    "help": "Filter by device ID (AID).",
}

hosts_domain_filter = {
    "fql": "machine_domain",
    "help": (
        "This filter accepts an AD domain, e.g. GOODDOMAIN or gooddomain.company.com. You can "
        "also provide multiple domains as a Python list or comma delimited string"
    ),
}

hosts_external_ip_address_filter = {
    "fql": "external_ip",
    "help": (
        "This filter accepts an IP address string associated with a remote network, e.g. "
        "123.234.123.234, or 123.234.0.0/16 to cover the /16 range. You can also comma delimit "
        "strings for multiple matches, e.g., 123.234.123.234,100.200.100.200 to target hosts with "
        "each of those IP addresses, or provide a Python list of IP address strings."
    ),
}

hosts_first_seen_filter = {
    **RELATIVE_TIMESTAMP_FILTER_TEMPLATE,
    "fql": "first_seen",
    "help": (
        "This filter accepts two types of parameter: a fixed ISO 8601 timestamp (such as "
        "2020-01-01:01:00:00Z), or a relative timestamp such as -30m. -30m means time now, "
        "minus thirty minutes, so is best combined with an operator such as GTE. One example is "
        "FirstSeen__GTE=-1d, to filter for all new hosts that have been added to Falcon within "
        "the past 1 day."
    ),
}

hosts_group_id_filter = {
    "fql": "groups",
    "help": (
        "This filter accepts one or more Group IDs as either one string, or as a comma "
        "delimited list of strings. For example, 075e03f5e5c04d83b4831374e7dc01c3 would "
        "target hosts within the group with ID 075e03f5e5c04d83b4831374e7dc01c3 only, or "
        "abcdefg123,abcdefg321 would target hosts in either group."
    ),
}

hosts_hostname_filter = {
    "fql": "hostname",
    "nullable": True,
    "help": (
        "Provide either a single hostname string, or a list of hostnames via a comma delimited "
        "string or Python list. For example, you can omit two specific hosts with "
        "Hostname__NOT=HOST1,HOST2."
    ),
}

hosts_last_seen_filter = {
    **RELATIVE_TIMESTAMP_FILTER_TEMPLATE,
    "fql": "last_seen",
    "help": (
        "This filter accepts two types of parameter: a fixed ISO 8601 timestamp (such as "
        "2020-01-01:01:00:00Z), or a relative timestamp such as -30m. -30m means time now, "
        "minus thirty minutes, so is best combined with an operator such as GTE. A popular "
        "example is LastSeen__GTE=-30m, to stipulate all hosts that have been online in the "
        "past half hour (i.e. are likely to be online)."
    ),
}

hosts_local_ip_address_filter = {
    "fql": "local_ip",
    "help": (
        "This filter accepts an IP address string associated with a network card, e.g. "
        "172.16.1.2 or 172.16.0.0/16 to cover the /16 range. You can also comma delimit strings "
        "for multiple matches, e.g., 172.16.1.2,172.16.1.3 to target hosts with each of those "
        "IP addresses, or provide a Python list of IP address strings."
    ),
}

hosts_mac_address_filter = {
    "fql": "mac_address",
    "help": (
        "This filter accepts a MAC address string associated with a network interface, e.g., "
        "01-22-33-44-55-66"
    ),
}

hosts_os_version_filter = {
    "fql": "os_version",
    "help": (
        "This filter accepts a name of an operating system version and can be supplied many "
        "times. For example, Windows 7, RHEL 7.9, Catalina (10.15), etc."
    ),
}


hosts_role_filter = {
    "fql": "product_type_desc",
    "transform": partial(user_readable_string_transform, _role_map),
    "validator": partial(options_validator, [*_role_map.keys(), *_role_map.values()]),
    "help": "Filter by system role (i.e., DC, Server, Workstation).",
}

hosts_site_filter = {
    "fql": "site_name",
    "help": (
        "This filter accepts one or more site names as either one string, or as a comma delimtied "
        "list of strings. For example, London,Manchster1,Manchester2 would target hosts within "
        "any of those three sites."
    ),
}

hosts_tag_filter = {
    "fql": "tags",
    "help": (
        "This filter accepts one or more sensor tags as either one string, or as a comma "
        "delimited list of strings. For example, SensorGroupingTags/Tag1,FalconGroupingTags/Tag2 "
        "to filter by hosts with one of those tags."
    ),
}

hosts_ou_filter = {
    "fql": "ou",
    "help": (
        "This filter accepts an Organisational Unit (OU) name as a string. You can also comma "
        "delimit OUs for multiple matches, e.g. UKServers,USServers to target hosts within any of "
        "those OUs. Programmatically, you can pass a Python list of OUs."
    ),
}

HOSTS_FILTERS: Dict[str, Dict[str, Any]] = {
    "contained": hosts_contained_filter,
    "deviceid": hosts_device_id_filter,
    "device_id": hosts_device_id_filter,  # pythonic
    "domain": hosts_domain_filter,
    "externalip": hosts_external_ip_address_filter,
    "external_ip": hosts_external_ip_address_filter,  # pythonic
    "firstseen": hosts_first_seen_filter,
    "first_seen": hosts_first_seen_filter,  # pythonic
    "groupid": hosts_group_id_filter,
    "group_id": hosts_group_id_filter,  # pythonic
    "hostname": hosts_hostname_filter,
    "lastseen": hosts_last_seen_filter,
    "last_seen": hosts_last_seen_filter,  # pythonic
    "localip": hosts_local_ip_address_filter,
    "local_ip": hosts_local_ip_address_filter,  # pythonic
    "macaddress": hosts_mac_address_filter,
    "mac_address": hosts_mac_address_filter,  # pythonic
    "osversion": hosts_os_version_filter,
    "os_version": hosts_os_version_filter,  # pythonic
    "role": hosts_role_filter,
    "site": hosts_site_filter,
    "tag": hosts_tag_filter,
}

rebase_filters_on_default(default_filter, HOSTS_FILTERS)
