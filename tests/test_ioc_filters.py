"""IOC-specific filters."""

from datetime import datetime

import pytest
import time_machine

from caracara_filters import FQLGenerator

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo


# Action
def test_valid_action():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("action", "no_action")
    fql = fql_generator.get_fql()
    assert fql == "action: 'no_action'"


def test_invalid_action():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("action", "invalid_action")


# Applied Globally
def test_applied_globally():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("applied_globally", "true")
    fql = fql_generator.get_fql()
    assert fql == "applied_globally: true"


# Created By
def test_created_by():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("created_by", "fake.name@crowdstrike.com")
    fql = fql_generator.get_fql()
    assert fql == "created_by: 'fake.name@crowdstrike.com'"


# Created On
@time_machine.travel(datetime(2024, 12, 31, 23, 50, 0, tzinfo=ZoneInfo("America/New_York")))
def test_created_on_relative_time_gte():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("created_on", "-2h", "GTE")
    fql = fql_generator.get_fql()
    assert fql == "created_on: >='2025-01-01T02:50:00Z'"


def test_created_on_static_time_gte():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("created_on", "2021-02-01T01:00:00Z", "GTE")
    fql = fql_generator.get_fql()
    assert fql == "created_on: >='2021-02-01T01:00:00Z'"


# Expiration
@time_machine.travel(datetime(2025, 3, 28, 12, 15, 0, tzinfo=ZoneInfo("UTC")))
def test_relative_ioc_expiration_relative_time_gte():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("expiration", "-30m", "GTE")
    fql = fql_generator.get_fql()
    assert fql == "expiration: >='2025-03-28T11:45:00Z'"


def test_relative_ioc_expiration_static_time_gte():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("expiration", "2020-01-01T01:00:00Z", "GTE")
    fql = fql_generator.get_fql()
    assert fql == "expiration: >='2020-01-01T01:00:00Z'"


def test_relative_ioc_expiration_static_time_equal():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("expiration", "2020-01-01T01:00:00Z", "EQUAL")
    fql = fql_generator.get_fql()
    assert fql == "expiration: '2020-01-01T01:00:00Z'"


# Expired
def test_expired_bool_false():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("expired", "false")
    fql = fql_generator.get_fql()
    assert fql == "expired: false"


def test_expired_str_true():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("expired", "true")
    fql = fql_generator.get_fql()
    assert fql == "expired: true"


def test_expired_str_invalid():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("expired", "neither")


def test_expired_none():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("expired", None)


# From Parent
def test_from_parent_bool_true():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("from_parent", "true")
    fql = fql_generator.get_fql()
    assert fql == "from_parent: true"


# ID
def test_iocs_id():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("id", "test")
    fql = fql_generator.get_fql()
    assert fql == "id: 'test'"


# Mobile Action
def test_mobile_action_valid():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("mobile_action", "prevent")
    fql = fql_generator.get_fql()
    assert fql == "mobile_action: 'prevent'"


def test_mobile_action_str_invalid():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("mobile_action", "invalid_mobile_action")


def test_mobile_action_type_invalid():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("mobile_action", 13)


# Modified On
@time_machine.travel(datetime(2024, 12, 31, 23, 50, 0, tzinfo=ZoneInfo("America/New_York")))
def test_modified_on_relative_time_gte():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("modified_on", "-2h", "GTE")
    fql = fql_generator.get_fql()
    assert fql == "modified_on: >='2025-01-01T02:50:00Z'"


def test_modified_on_static_time_gte():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("modified_on", "2021-02-01T01:00:00Z", "GTE")
    fql = fql_generator.get_fql()
    assert fql == "modified_on: >='2021-02-01T01:00:00Z'"


def test_modified_on_str_bad_timestamp():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("modified_on", "2025-01-12t00:00:00z")


def test_modified_on_type_invalid():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("modified_on", 13)


def test_modified_on_type_none():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("modified_on", None)


# Modified By
def test_modified_by():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("modified_by", "fake.name2@crowdstrike.com")
    fql = fql_generator.get_fql()
    assert fql == "modified_by: 'fake.name2@crowdstrike.com'"


# Platform
def test_platform_valid_capital_first():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("platform", "Linux")
    fql = fql_generator.get_fql()
    assert fql == "platforms: 'linux'"


def test_platform_invalid():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("platform", "notwindows")


def test_platform_invalid_type():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("platform", 13)

    with pytest.raises(TypeError):
        fql_generator.create_new_filter("platform", None)


# Severity
def test_severity_high():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("severity", "high")
    fql = fql_generator.get_fql()
    assert fql == "severity: 'high'"


def test_severity_str_invalid():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("severity", "middle")


# Tags
def test_ioc_tags():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("tags", "an-ioc-tag")
    fql = fql_generator.get_fql()
    assert fql == "tags: 'an-ioc-tag'"


def test_ioc_tags_multi():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("tags", ["a-tag", "another-tag"])
    fql = fql_generator.get_fql()
    assert fql == "tags: ['a-tag','another-tag']"


def test_ioc_tags_invalid_type():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("tags", 13)


# Type
def test_ioc_type_valid():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("type", "sha256")
    fql = fql_generator.get_fql()
    assert fql == "type: 'sha256'"


def test_ioc_type_valid_multi():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("type", ["all_subdomains", "ipv6"])
    fql = fql_generator.get_fql()
    assert fql == "type: ['all_subdomains','ipv6']"


def test_ioc_type_partly_valid_multi():
    fql_generator = FQLGenerator(dialect="iocs")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("type", ["domain", "invalid-ioc-type"])


# Value
def test_ioc_value():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("value", "1.2.3.4")
    fql = fql_generator.get_fql()
    assert fql == "value: '1.2.3.4'"


# Combination of Filters
@time_machine.travel(datetime(2025, 1, 1, 0, 30, 13, tzinfo=ZoneInfo("Europe/Berlin")))
def test_ioc_multi_1():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("action", ["allow", "no_action"])
    fql_generator.create_new_filter("applied_globally", "true")
    fql_generator.create_new_filter("created_by", "first.last@customer.com")
    fql_generator.create_new_filter("modified_on", "-1h", "GTE")
    fql_generator.create_new_filter("type", ["domain", "md5"])
    fql = fql_generator.get_fql()
    assert fql == (
        "action: ['allow','no_action']+"
        "applied_globally: true+"
        "created_by: 'first.last@customer.com'+"
        "modified_on: >='2024-12-31T22:30:13Z'+"
        "type: ['domain','md5']"
    )


def test_ioc_multi_2():
    fql_generator = FQLGenerator(dialect="iocs")
    fql_generator.create_new_filter("action", "prevent")
    fql_generator.create_new_filter("platform", ["WINDOWS", "Mac"])
    fql = fql_generator.get_fql()
    assert fql == "action: 'prevent'+platforms: ['windows','mac']"
