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
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("OS", ["Windows", "Linux"])
    fql = fql_generator.get_fql()
    assert fql == "platform_name: ['Windows','Linux']"


def test_ip_fql():
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("localip", "192.168.1.1")
    fql = fql_generator.get_fql()
    assert fql == "local_ip: '192.168.1.1'"


def test_containment_pending_human_readable():
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("contained", "Containment Pending")
    fql = fql_generator.get_fql()
    assert fql == "status: 'containment_pending'"


def test_contained_machine_readable():
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("contained", "contained")
    fql = fql_generator.get_fql()
    assert fql == "status: 'contained'"


def test_multi_hostname_domain():
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("Hostname", "TestBox*")
    fql_generator.create_new_filter("domain", "ad.local")
    fql = fql_generator.get_fql()
    assert fql == "hostname: 'TestBox*'+machine_domain: 'ad.local'"


@freeze_time("2023-08-14 08:00:13", tz_offset=-7)
def test_relative_first_seen_with_tz_offset():
    # FreezeGun uses a UTC timestamp, so this proves the effectiveness of datetime.utcnow()
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("FirstSeen", "-30m", "LTE")
    fql = fql_generator.get_fql()
    assert fql == "first_seen: <='2023-08-14T07:30:13Z'"


@freeze_time("2022-12-13 13:14:15", tz_offset=-4)
def test_relative_last_seen_default_operator_tz_offset():
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("LastSeen", "-1h")
    fql = fql_generator.get_fql()
    # We default to GTE (>=) for this filter type
    assert fql == "last_seen: >='2022-12-13T12:14:15Z'"


def test_invalid_os_option():
    fql_generator = FQLGenerator()
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("OS", "Fakedows", "EQUAL")


def test_mixed_valid_invalid_os_option():
    fql_generator = FQLGenerator()
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("OS", ['Windows', 'Linux', 'Solaris'])


def test_role():
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("Role", "Server")
    fql = fql_generator.get_fql()
    assert fql == "product_type_desc: 'Server'"


def test_wrong_role():
    fql_generator = FQLGenerator(dialect='base')
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("OS", "Windows")


def test_base_in_hosts():
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("Name", "SomeNameOfSomething")
    fql = fql_generator.get_fql()
    assert fql == "name: 'SomeNameOfSomething'"


@freeze_time("2020-01-01 00:00:13")
def test_multi_kv_string():
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter_from_kv_string("OS", "Windows,Linux")
    fql_generator.create_new_filter_from_kv_string("LastSeen__GTE", "-29m")
    fql = fql_generator.get_fql()
    assert fql == "platform_name: ['Windows','Linux']+last_seen: >='2019-12-31T23:31:13Z'"


def test_non_multivariate_list_exception():
    fql_generator = FQLGenerator(dialect='hosts')
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("LastSeen", ['-30m', '-60h'])


def test_incorrect_list_type_exception():
    fql_generator = FQLGenerator(dialect='hosts')
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("hostname", [0, 'some host'])


def test_validation_failure():
    fql_generator = FQLGenerator(dialect='hosts')
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("LastSeen", '^123')


def test_incorrect_containment_option():
    fql_generator = FQLGenerator(dialect='hosts')
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("contained", "some containment option")


def test_incorrect_relative_timestamp_format():
    fql_generator = FQLGenerator(dialect='hosts')
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("firstseen", "-80x")


@freeze_time("2023-08-15 01:02:03")
def test_last_seen_day():
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("firstseen", "-2d")
    fql = fql_generator.get_fql()
    assert fql == "first_seen: >='2023-08-13T01:02:03Z'"


@freeze_time("2023-08-15 01:02:03")
def test_first_seen_add_time():
    # This is a ridiculous scenario, but we support it anyway.
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("firstseen", "+2d")
    fql = fql_generator.get_fql()
    assert fql == "first_seen: >='2023-08-17T01:02:03Z'"


@freeze_time("2023-08-15 01:02:03")
def test_last_seen_relative_seconds():
    fql_generator = FQLGenerator(dialect='hosts')
    fql_generator.create_new_filter("lastseen", "-63s")
    fql = fql_generator.get_fql()
    assert fql == "last_seen: >='2023-08-15T01:01:00Z'"
