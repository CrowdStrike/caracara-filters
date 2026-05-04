"""Caracara Filters: Sensor Download Dialect.

This module contains filters specific to the Sensor Download API, enabling
structured searches across the sensor installer versions available for download.
"""

from functools import partial
from typing import Any, Dict

from caracara_filters.common.templates import RELATIVE_TIMESTAMP_FILTER_TEMPLATE
from caracara_filters.dialects._base import default_filter, rebase_filters_on_default
from caracara_filters.transforms import bool_transform, lowercase_transform
from caracara_filters.validators import boolean_validator, options_validator

# Sensor installer platform values as returned by the API (lowercase).
_INSTALLER_PLATFORMS = ["android", "linux", "mac", "vmware", "windows"]

installer_architectures_filter = {
    "fql": "architectures",
    "help": (
        "Filter by processor architecture supported by the installer "
        "(e.g. 'x86_64', 'arm64'). This field is available on V2 and V3 installer metadata."
    ),
}

installer_is_lts_filter = {
    "fql": "is_lts",
    "data_types": [str, bool],
    "transform": bool_transform,
    "validator": partial(boolean_validator, accept_yes_no=True),
    "help": (
        "Filter by whether the installer is a Long Term Support (LTS) release. "
        "Accepts True/False or 'yes'/'no'. This field is available on V3 installer metadata only."
    ),
}

installer_os_filter = {
    "fql": "os",
    "help": (
        "Filter by operating system name as reported in the installer metadata. "
        "Examples include 'RHEL', 'Ubuntu', 'Debian', 'Windows'."
    ),
}

installer_os_version_filter = {
    "fql": "os_version",
    "help": (
        "Filter by operating system version string associated with the installer. "
        "For example, '8' for RHEL 8 or '20.04' for Ubuntu 20.04."
    ),
}

installer_platform_filter = {
    "fql": "platform",
    "transform": lowercase_transform,
    "validator": partial(options_validator, _INSTALLER_PLATFORMS, case_sensitive=False),
    "help": (
        f"Filter by sensor installer platform (options: {_INSTALLER_PLATFORMS}). "
        "Case-insensitive: 'Windows', 'windows', and 'WINDOWS' are all accepted. "
        "This maps to the platform property in the installer metadata, which is distinct "
        "from the os and os_version fields."
    ),
}

installer_release_date_filter = {
    **RELATIVE_TIMESTAMP_FILTER_TEMPLATE,
    "fql": "release_date",
    "help": (
        "Filter by installer release date. Accepts a fixed ISO 8601 timestamp "
        "(e.g. 2024-01-01T00:00:00Z) or a relative timestamp such as -30d. "
        "For example, ReleaseDate__GTE=-90d returns installers released within the last 90 days."
    ),
}

installer_version_filter = {
    "fql": "version",
    "valid_operators": ["EQUAL", "NOT", "GREATER", "GTE", "LESS", "LTE"],
    "help": (
        "Filter by sensor version string. Comparison operators are supported, e.g. "
        "Version__GTE='7.0' to find all versions from 7.0 upwards. "
        "Note that FQL uses lexicographic comparison, so version ordering may be unexpected "
        "for version strings with varying digit counts (e.g., '7.9' vs '7.10')."
    ),
}

SENSOR_DOWNLOAD_FILTERS: Dict[str, Dict[str, Any]] = {
    "architectures": installer_architectures_filter,
    "islts": installer_is_lts_filter,
    "is_lts": installer_is_lts_filter,  # pythonic
    "lts": installer_is_lts_filter,  # common shorthand
    "os": installer_os_filter,  # overrides base 'os' which maps to platform_name
    "osversion": installer_os_version_filter,
    "os_version": installer_os_version_filter,  # pythonic
    "platform": installer_platform_filter,
    "releasedate": installer_release_date_filter,
    "release_date": installer_release_date_filter,  # pythonic
    "version": installer_version_filter,
}

rebase_filters_on_default(default_filter, SENSOR_DOWNLOAD_FILTERS)
