"""Tests that can cover the way that the filtering logic works outside of individual dialects."""
import pytest

from caracara_filters import FQLGenerator


def test_non_existent_dialect():
    """Test an attempt to load a dialect that doesn't exist."""
    with pytest.raises(ValueError):
        FQLGenerator(dialect='not a module')


def test_filter_delete_real_id():
    """Test attempting to delete a filter from an FQLGenerator object."""
    fql_generator = FQLGenerator(dialect='base')
    filter_id = fql_generator.create_new_filter("name", "testtest")
    fql = fql_generator.get_fql()
    assert fql == "name: 'testtest'"
    assert filter_id is not None
    fql_generator.remove_filter(filter_id)
    assert not fql_generator.filters


def test_filter_delete_bad_id():
    """Test trying to delete a nonexistent filter."""
    fql_generator = FQLGenerator()
    with pytest.raises(KeyError):
        fql_generator.remove_filter("non-existent-filter-id")


def test_bad_data_type():
    """Test trying to load a base filter with a bad datatype."""
    fql_generator = FQLGenerator(dialect='base')
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("name", 123)


def test_nullable_filter():
    """Test that a nullable filter accepts None correctly."""
    # TODO: write a test here once we have a nullable filter defined
    # (and validation logic to handle this)


def test_bool_filter():
    """Test that a boolean filter properly validates and transforms."""
    # TODO: write a test once we have a boolean filter defined


def test_str_dunder():
    """Test that the __str__ function in the FQLGenerator class works."""
    fql_generator = FQLGenerator(dialect='base')
    fql_generator.create_new_filter("name", "testname")
    fql = fql_generator.get_fql()
    assert fql == str(fql_generator)
    assert fql == "name: 'testname'"
