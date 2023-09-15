"""Test hosts dialect filters."""
import pytest

from freezegun import freeze_time

from caracara_filters import FQLGenerator


def test_os_windows_fql():
    """Test filtering for just Windows systems."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("OS", "Windows")
    fql = fql_generator.get_fql()
    assert fql == "platform_name: 'Windows'"


def test_os_windows_linux_fql():
    """Test filtering for Windows and Linux systems."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("OS", ["Windows", "Linux"])
    fql = fql_generator.get_fql()
    assert fql == "platform_name: ['Windows','Linux']"


def test_ip_fql():
    """Test filtering by local IP address."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("localip", "192.168.1.1")
    fql = fql_generator.get_fql()
    assert fql == "local_ip: '192.168.1.1'"


def test_containment_pending_human_readable():
    """Test a filter for systems pending containment, with the input in upper case."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("contained", "Containment Pending")
    fql = fql_generator.get_fql()
    assert fql == "status: 'containment_pending'"


def test_contained_machine_readable():
    """Test a filter for contained systems with the input in lower case."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("contained", "contained")
    fql = fql_generator.get_fql()
    assert fql == "status: 'contained'"


def test_contained_and_pending_containment():
    """Test filtering for contained systems, and those with containment pending, in mixed case."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("contained", ["contained", "Containment Pending"])
    fql = fql_generator.get_fql()
    assert fql == "status: ['contained','containment_pending']"


def test_multi_hostname_domain():
    """Test a filter for systems by hostname AND domain."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("Hostname", "TestBox*")
    fql_generator.create_new_filter("domain", "ad.local")
    fql = fql_generator.get_fql()
    assert fql == "hostname: 'TestBox*'+machine_domain: 'ad.local'"


def test_multi_role():
    """Test a filter for systems that are both DCs AND Servers."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("Role", ["DC", "Server"])
    fql = fql_generator.get_fql()
    assert fql == "product_type_desc: ['Domain Controller','Server']"


def test_null_hostname():
    """Test that a null hostname is properly transformed to null."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("Hostname", None)
    fql = fql_generator.get_fql()
    assert fql == "hostname: null"


@freeze_time("2023-08-14 08:00:13", tz_offset=-7)
def test_relative_first_seen_with_tz_offset():
    """Test filtering for systems that have been online only before half an hour ago."""
    # FreezeGun uses a UTC timestamp, so this proves the effectiveness of datetime.utcnow()
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("FirstSeen", "-30m", "LTE")
    fql = fql_generator.get_fql()
    assert fql == "first_seen: <='2023-08-14T07:30:13Z'"


@freeze_time("2022-12-13 13:14:15", tz_offset=-4)
def test_relative_last_seen_default_operator_tz_offset():
    """Test filtering by systems last seen within the past hour."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("LastSeen", "-1h")
    fql = fql_generator.get_fql()
    # We default to GTE (>=) for this filter type
    assert fql == "last_seen: >='2022-12-13T12:14:15Z'"


def test_invalid_os_option():
    """Test filtering with an invalid platform name."""
    fql_generator = FQLGenerator()
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("OS", "Fakedows", "EQUAL")


def test_mixed_valid_invalid_os_option():
    """Test filtering with a list of platforms, where one is incorrect."""
    fql_generator = FQLGenerator()
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("OS", ['Windows', 'Linux', 'Solaris'])


def test_role():
    """Test filtering for a single OS role."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("Role", "Server")
    fql = fql_generator.get_fql()
    assert fql == "product_type_desc: 'Server'"


def test_wrong_dialect():
    """Test a hosts filter that does not exist in the base dialect."""
    fql_generator = FQLGenerator(dialect='base')
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("LastSeen", "-30m")


def test_base_in_hosts():
    """Test that a base filter exists in the hosts dialect."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("Name", "SomeNameOfSomething")
    fql = fql_generator.get_fql()
    assert fql == "name: 'SomeNameOfSomething'"


@freeze_time("2020-01-01 00:00:13")
def test_multi_kv_string():
    """Test a comma-delimited KV multivariate combined with a Last Seen relative timestamp."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter_from_kv_string("OS", "Windows,Linux")
    fql_generator.create_new_filter_from_kv_string("LastSeen__GTE", "-29m")
    fql = fql_generator.get_fql()
    assert fql == "platform_name: ['Windows','Linux']+last_seen: >='2019-12-31T23:31:13Z'"


def test_non_multivariate_list_exception():
    """Test passing multiple options into a non-multivariate filter."""
    fql_generator = FQLGenerator(dialect='hosts')
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("LastSeen", ['-30m', '-60h'])


def test_incorrect_list_type_exception():
    """Test passing an incorrect datatype into a list."""
    fql_generator = FQLGenerator(dialect='hosts')
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("hostname", [0, 'some host'])


def test_validation_failure():
    """Test a failed validation."""
    fql_generator = FQLGenerator(dialect='hosts')
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("LastSeen", '^123')


def test_incorrect_containment_option():
    """Test filtering by an incorrect containment status."""
    fql_generator = FQLGenerator(dialect='hosts')
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("contained", "some containment option")


def test_incorrect_relative_timestamp_format():
    """Test filtering by a relative timestamp in an incorrect format."""
    fql_generator = FQLGenerator(dialect='hosts')
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("firstseen", "-80x")


@freeze_time("2023-08-15 01:02:03")
def test_last_seen_day():
    """Test relative timestamp filtering that spans multiple days."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("firstseen", "-2d")
    fql = fql_generator.get_fql()
    assert fql == "first_seen: >='2023-08-13T01:02:03Z'"


@freeze_time("2023-08-15 01:02:03")
def test_first_seen_add_time():
    """Test adding time to a relative timestamp."""
    # This is a ridiculous scenario, but we support it anyway.
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("firstseen", "+2d")
    fql = fql_generator.get_fql()
    assert fql == "first_seen: >='2023-08-17T01:02:03Z'"


@freeze_time("2023-08-15 01:02:03")
def test_last_seen_relative_seconds():
    """Test filtering by a relative timestamp in the order of seconds."""
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("lastseen", "-63s")
    fql = fql_generator.get_fql()
    assert fql == "last_seen: >='2023-08-15T01:01:00Z'"
