"""Tests for the sensor_download FQL dialect.

Filter values are drawn from real API responses observed during live testing against the
CrowdStrike Sensor Download API.  Platforms confirmed: android, linux, mac, vmware, windows.
"""

from datetime import datetime

import pytest
import time_machine

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from caracara_filters import FQLGenerator


# ---------------------------------------------------------------------------
# architectures
# ---------------------------------------------------------------------------


def test_architectures_x86_64():
    """Filter by x86_64 architecture (most common Linux/Windows build)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("architectures", "x86_64")
    assert fql_generator.get_fql() == "architectures: 'x86_64'"


def test_architectures_arm64():
    """Filter by arm64 architecture (Apple Silicon, AWS Graviton, RHEL arm64)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("architectures", "arm64")
    assert fql_generator.get_fql() == "architectures: 'arm64'"


def test_architectures_s390x():
    """Filter by s390x (IBM zLinux) architecture."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("architectures", "s390x")
    assert fql_generator.get_fql() == "architectures: 's390x'"


def test_architectures_multivariate():
    """Filter by multiple architectures using a list."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("architectures", ["x86_64", "arm64"])
    assert fql_generator.get_fql() == "architectures: ['x86_64','arm64']"


# ---------------------------------------------------------------------------
# is_lts — boolean filter; accepts bool or string
# ---------------------------------------------------------------------------


def test_is_lts_true_bool():
    """Python True produces unquoted FQL true."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("is_lts", True)
    assert fql_generator.get_fql() == "is_lts: true"


def test_is_lts_false_bool():
    """Python False produces unquoted FQL false."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("is_lts", False)
    assert fql_generator.get_fql() == "is_lts: false"


def test_is_lts_string_true():
    """String 'true' is coerced to boolean true."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("is_lts", "true")
    assert fql_generator.get_fql() == "is_lts: true"


def test_is_lts_string_false():
    """String 'false' is coerced to boolean false."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("is_lts", "false")
    assert fql_generator.get_fql() == "is_lts: false"


def test_is_lts_string_true_mixed_case():
    """String 'True' (title case) is accepted and coerced to boolean true."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("is_lts", "True")
    assert fql_generator.get_fql() == "is_lts: true"


def test_is_lts_string_false_mixed_case():
    """String 'False' (title case) is accepted and coerced to boolean false."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("is_lts", "False")
    assert fql_generator.get_fql() == "is_lts: false"


def test_is_lts_string_yes():
    """String 'yes' is treated as true (human-friendly alias)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("is_lts", "yes")
    assert fql_generator.get_fql() == "is_lts: true"


def test_is_lts_string_no():
    """String 'no' is treated as false (human-friendly alias)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("is_lts", "no")
    assert fql_generator.get_fql() == "is_lts: false"


def test_is_lts_alias_islts():
    """islts is a valid alias for is_lts."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("islts", True)
    assert fql_generator.get_fql() == "is_lts: true"


def test_is_lts_alias_lts():
    """lts is a valid shorthand alias for is_lts."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("lts", True)
    assert fql_generator.get_fql() == "is_lts: true"


def test_is_lts_invalid_value():
    """An unrecognised string raises ValueError."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("is_lts", "maybe")


def test_is_lts_invalid_type():
    """An integer raises TypeError (is_lts only accepts str or bool)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("is_lts", 1)


# ---------------------------------------------------------------------------
# os — free-form string matching the OS field returned by the API
# ---------------------------------------------------------------------------


def test_os_rhel():
    """Filter by RHEL (most common Linux OS in this tenant)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os", "RHEL")
    assert fql_generator.get_fql() == "os: 'RHEL'"


def test_os_ubuntu():
    """Filter by Ubuntu."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os", "Ubuntu")
    assert fql_generator.get_fql() == "os: 'Ubuntu'"


def test_os_debian():
    """Filter by Debian."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os", "Debian")
    assert fql_generator.get_fql() == "os: 'Debian'"


def test_os_windows():
    """Filter by Windows (standard desktop/server sensor)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os", "Windows")
    assert fql_generator.get_fql() == "os: 'Windows'"


def test_os_macos():
    """Filter by macOS (value as returned by the API)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os", "macOS")
    assert fql_generator.get_fql() == "os: 'macOS'"


def test_os_asset_inventory():
    """Filter by Asset Inventory (the VMware OVA appliance OS label)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os", "Asset Inventory")
    assert fql_generator.get_fql() == "os: 'Asset Inventory'"


def test_os_android():
    """Filter by Android."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os", "Android")
    assert fql_generator.get_fql() == "os: 'Android'"


def test_os_photon_os():
    """Filter by PhotonOS (used for VMware vSphere guest sensors)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os", "PhotonOS")
    assert fql_generator.get_fql() == "os: 'PhotonOS'"


def test_os_compound_name():
    """Filter by compound OS names such as RHEL/CentOS/Oracle (as returned by the API)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os", "RHEL/CentOS/Oracle")
    assert fql_generator.get_fql() == "os: 'RHEL/CentOS/Oracle'"


# ---------------------------------------------------------------------------
# os_version — version string as returned by the API; accepts complex forms
# ---------------------------------------------------------------------------


def test_os_version_simple():
    """Filter by a simple numeric OS version (e.g. RHEL 8)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os_version", "8")
    assert fql_generator.get_fql() == "os_version: '8'"


def test_os_version_semver():
    """Filter by a dotted OS version string (e.g. Ubuntu 20.04)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os_version", "20.04")
    assert fql_generator.get_fql() == "os_version: '20.04'"


def test_os_version_with_arch_suffix():
    """Filter by OS version that includes an architecture qualifier (e.g. SLES 15 - arm64)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os_version", "15 - arm64")
    assert fql_generator.get_fql() == "os_version: '15 - arm64'"


def test_os_version_with_ibm_zlinux_suffix():
    """Filter by OS version including the IBM zLinux qualifier, as seen in API responses."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os_version", "7 - IBM zLinux")
    assert fql_generator.get_fql() == "os_version: '7 - IBM zLinux'"


def test_os_version_multi_release_string():
    """Filter by a multi-release version string (e.g. Debian 9/10/11/12/13)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("os_version", "9/10/11/12/13")
    assert fql_generator.get_fql() == "os_version: '9/10/11/12/13'"


def test_os_version_alias_osversion():
    """osversion is a valid camelCase alias for os_version."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("osversion", "8")
    assert fql_generator.get_fql() == "os_version: '8'"


# ---------------------------------------------------------------------------
# platform — case-insensitive enum; transforms to lowercase for the API
# ---------------------------------------------------------------------------


def test_platform_linux_lowercase():
    """Lowercase 'linux' is accepted and passed through as-is."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "linux")
    assert fql_generator.get_fql() == "platform: 'linux'"


def test_platform_linux_titlecase():
    """'Linux' (title case) is normalised to lowercase."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "Linux")
    assert fql_generator.get_fql() == "platform: 'linux'"


def test_platform_linux_uppercase():
    """'LINUX' (all caps) is normalised to lowercase."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "LINUX")
    assert fql_generator.get_fql() == "platform: 'linux'"


def test_platform_windows_lowercase():
    """Lowercase 'windows' is accepted."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "windows")
    assert fql_generator.get_fql() == "platform: 'windows'"


def test_platform_windows_titlecase():
    """'Windows' (title case) is normalised to lowercase."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "Windows")
    assert fql_generator.get_fql() == "platform: 'windows'"


def test_platform_mac_lowercase():
    """Lowercase 'mac' is accepted."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "mac")
    assert fql_generator.get_fql() == "platform: 'mac'"


def test_platform_mac_titlecase():
    """'Mac' (title case) is normalised to lowercase."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "Mac")
    assert fql_generator.get_fql() == "platform: 'mac'"


def test_platform_vmware_lowercase():
    """Lowercase 'vmware' is accepted (targets OVA asset inventory appliance)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "vmware")
    assert fql_generator.get_fql() == "platform: 'vmware'"


def test_platform_vmware_mixed_case():
    """'VMware' (mixed case) is normalised to lowercase."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "VMware")
    assert fql_generator.get_fql() == "platform: 'vmware'"


def test_platform_android_lowercase():
    """Lowercase 'android' is accepted."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "android")
    assert fql_generator.get_fql() == "platform: 'android'"


def test_platform_android_titlecase():
    """'Android' (title case) is normalised to lowercase."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "Android")
    assert fql_generator.get_fql() == "platform: 'android'"


def test_platform_multivariate():
    """Multiple platforms can be requested together using a list."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", ["linux", "windows"])
    assert fql_generator.get_fql() == "platform: ['linux','windows']"


def test_platform_invalid_value():
    """An unsupported platform name raises ValueError."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("platform", "ios")


def test_platform_invalid_type():
    """A non-string value raises TypeError."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("platform", 42)


# ---------------------------------------------------------------------------
# release_date — relative and absolute timestamps; default operator is GTE
# ---------------------------------------------------------------------------


@time_machine.travel(datetime(2024, 6, 15, 12, 0, 0, tzinfo=ZoneInfo("UTC")))
def test_release_date_relative_gte_default_operator():
    """Relative timestamp with default GTE operator subtracts days from UTC now."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("release_date", "-30d")
    assert fql_generator.get_fql() == "release_date: >='2024-05-16T12:00:00Z'"


@time_machine.travel(datetime(2024, 6, 15, 12, 0, 0, tzinfo=ZoneInfo("UTC")))
def test_release_date_relative_lte():
    """Relative timestamp with explicit LTE operator."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("release_date", "-90d", "LTE")
    assert fql_generator.get_fql() == "release_date: <='2024-03-17T12:00:00Z'"


@time_machine.travel(datetime(2024, 6, 15, 12, 0, 0, tzinfo=ZoneInfo("UTC")))
def test_release_date_relative_greater():
    """Relative timestamp with GREATER (strict greater-than) operator."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("release_date", "-7d", "GREATER")
    assert fql_generator.get_fql() == "release_date: >'2024-06-08T12:00:00Z'"


@time_machine.travel(datetime(2024, 6, 15, 12, 0, 0, tzinfo=ZoneInfo("UTC")))
def test_release_date_relative_less():
    """Relative timestamp with LESS (strict less-than) operator."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("release_date", "+1d", "LESS")
    assert fql_generator.get_fql() == "release_date: <'2024-06-16T12:00:00Z'"


@time_machine.travel(datetime(2024, 6, 15, 8, 0, 0, tzinfo=ZoneInfo("America/New_York")))
def test_release_date_relative_with_tz_offset():
    """Relative timestamp is always converted to UTC regardless of local timezone."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("release_date", "-30d", "GTE")
    # America/New_York is UTC-4 in summer; local 08:00 = UTC 12:00; minus 30d = 2024-05-16T12:00:00Z
    assert fql_generator.get_fql() == "release_date: >='2024-05-16T12:00:00Z'"


def test_release_date_absolute_iso8601_gte():
    """An ISO 8601 absolute timestamp is passed through unchanged."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("release_date", "2024-01-01T00:00:00Z", "GTE")
    assert fql_generator.get_fql() == "release_date: >='2024-01-01T00:00:00Z'"


def test_release_date_absolute_iso8601_equal():
    """EQUAL operator with an absolute timestamp (no operator symbol in output)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("release_date", "2024-06-15T12:00:00Z", "EQUAL")
    assert fql_generator.get_fql() == "release_date: '2024-06-15T12:00:00Z'"


def test_release_date_alias_releasedate():
    """releasedate is a valid camelCase alias for release_date."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("releasedate", "2024-01-01T00:00:00Z", "GTE")
    assert fql_generator.get_fql() == "release_date: >='2024-01-01T00:00:00Z'"


def test_release_date_invalid_timestamp():
    """A non-timestamp string raises ValueError."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("release_date", "not-a-date")


def test_release_date_invalid_operator():
    """An operator not in the allowed set raises ValueError."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("release_date", "2024-01-01T00:00:00Z", "NOT")


# ---------------------------------------------------------------------------
# version — supports EQUAL, NOT, GREATER, GTE, LESS, LTE
# ---------------------------------------------------------------------------


def test_version_equal():
    """Exact version match (default EQUAL operator, no symbol in FQL)."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("version", "7.36.18909")
    assert fql_generator.get_fql() == "version: '7.36.18909'"


def test_version_gte():
    """Version greater-than-or-equal (>=) comparison."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("version", "7.14.0", "GTE")
    assert fql_generator.get_fql() == "version: >='7.14.0'"


def test_version_lte():
    """Version less-than-or-equal (<=) comparison."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("version", "7.32.18513", "LTE")
    assert fql_generator.get_fql() == "version: <='7.32.18513'"


def test_version_greater():
    """Version strict greater-than (>) comparison using GREATER operator."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("version", "7.0", "GREATER")
    assert fql_generator.get_fql() == "version: >'7.0'"


def test_version_less():
    """Version strict less-than (<) comparison using LESS operator."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("version", "7.36.0", "LESS")
    assert fql_generator.get_fql() == "version: <'7.36.0'"


def test_version_not():
    """Version NOT (!=) excludes a specific version."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("version", "7.19.18913", "NOT")
    assert fql_generator.get_fql() == "version: !'7.19.18913'"


def test_version_android_date_style():
    """Android version strings (date-style prefix) are accepted as plain strings."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("version", "2025.05.4150001 (4.15.0)")
    assert fql_generator.get_fql() == "version: '2025.05.4150001 (4.15.0)'"


def test_version_invalid_operator():
    """An operator not in the allowed set raises ValueError."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("version", "7.0", "CONTAINS")


# ---------------------------------------------------------------------------
# Multi-filter combinations
# ---------------------------------------------------------------------------


def test_combined_platform_and_os():
    """Combining platform and os filters produces a joined FQL string."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "Linux")
    fql_generator.create_new_filter("os", "RHEL")
    assert fql_generator.get_fql() == "platform: 'linux'+os: 'RHEL'"


def test_combined_platform_and_is_lts():
    """Combining platform and is_lts produces the correct mixed-type FQL."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "Windows")
    fql_generator.create_new_filter("is_lts", True)
    assert fql_generator.get_fql() == "platform: 'windows'+is_lts: true"


def test_combined_vmware_asset_inventory():
    """Combining vmware platform with Asset Inventory OS targets OVA appliances."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "vmware")
    fql_generator.create_new_filter("os", "Asset Inventory")
    assert fql_generator.get_fql() == "platform: 'vmware'+os: 'Asset Inventory'"


def test_combined_platform_os_version_gte():
    """Three-filter combination: platform, os, and version with GTE operator."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("platform", "Linux")
    fql_generator.create_new_filter("os", "RHEL")
    fql_generator.create_new_filter("version", "7.14.0", "GTE")
    assert fql_generator.get_fql() == "platform: 'linux'+os: 'RHEL'+version: >='7.14.0'"


def test_combined_architectures_and_is_lts():
    """Architectures and is_lts can be combined to target LTS arm64 builds."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter("architectures", "arm64")
    fql_generator.create_new_filter("is_lts", False)
    assert fql_generator.get_fql() == "architectures: 'arm64'+is_lts: false"


# ---------------------------------------------------------------------------
# kv-string interface (create_new_filter_from_kv_string)
# ---------------------------------------------------------------------------


def test_kv_string_platform():
    """Platform filter created via kv-string interface."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter_from_kv_string("platform", "Linux")
    assert fql_generator.get_fql() == "platform: 'linux'"


def test_kv_string_version_gte():
    """Version GTE filter created via kv-string interface with operator suffix."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter_from_kv_string("version__GTE", "7.14.0")
    assert fql_generator.get_fql() == "version: >='7.14.0'"


def test_kv_string_is_lts_bool_string():
    """is_lts filter created via kv-string with a 'True' string value."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter_from_kv_string("is_lts", "True")
    assert fql_generator.get_fql() == "is_lts: true"


@time_machine.travel(datetime(2024, 6, 15, 12, 0, 0, tzinfo=ZoneInfo("UTC")))
def test_kv_string_release_date_gte():
    """release_date GTE filter created via kv-string with a relative timestamp."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter_from_kv_string("release_date__GTE", "-90d")
    assert fql_generator.get_fql() == "release_date: >='2024-03-17T12:00:00Z'"


def test_kv_string_os_version_alias():
    """os_version filter created via the osversion camelCase alias."""
    fql_generator = FQLGenerator(dialect="sensor_download")
    fql_generator.create_new_filter_from_kv_string("osversion", "8")
    assert fql_generator.get_fql() == "os_version: '8'"
