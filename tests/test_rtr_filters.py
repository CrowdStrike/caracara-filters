"""Test RTR-specific filters."""

import pytest

from caracara_filters import FQLGenerator


def test_base_command_fql():
    """Test that the base_command filter accepts a valid RTR command."""
    fql_generator = FQLGenerator(dialect="rtr")
    fql_generator.create_new_filter("command", "put")
    fql = fql_generator.get_fql()
    assert fql == "base_command: 'put'"


def test_mixed_case_base_command_fql():
    """Test that a mixed case base comand validates and transforms as expected."""
    fql_generator = FQLGenerator(dialect="rtr")
    fql_generator.create_new_filter("command", "GeT")
    fql = fql_generator.get_fql()
    assert fql == "base_command: 'GeT'"


def test_invalid_operator_base_command():
    """Test that an invalid filter type will properly error."""
    fql_generator = FQLGenerator(dialect="rtr")
    with pytest.raises(ValueError):
        fql_generator.create_new_filter("command", "ls", "GTE")
