import pytest

from caracara_filters import FQLGenerator


def test_non_existent_dialect():
    with pytest.raises(ValueError):
        FQLGenerator(dialect='not a module')


def test_filter_delete_real_id():
    fql_generator = FQLGenerator(dialect='base')
    filter_id = fql_generator.create_new_filter("name", "testtest")
    fql = fql_generator.get_fql()
    assert fql == "name: 'testtest'"
    assert filter_id is not None
    fql_generator.remove_filter(filter_id)
    assert fql_generator.filters == {}


def test_filter_delete_bad_id():
    fql_generator = FQLGenerator()
    with pytest.raises(KeyError):
        fql_generator.remove_filter("non-existent-filter-id")


def test_bad_data_type():
    fql_generator = FQLGenerator(dialect='base')
    with pytest.raises(TypeError):
        fql_generator.create_new_filter("name", 123)


def test_nullable_filter():
    # TODO: write a test here once we have a nullable filter defined
    # (and validation logic to handle this)
    pass


def test_bool_filter():
    # TODO: write a test once we have a boolean filter defined
    pass


def test_str_dunder():
    fql_generator = FQLGenerator(dialect='base')
    fql_generator.create_new_filter("name", "testname")
    fql = fql_generator.get_fql()
    assert fql == str(fql_generator)
    assert fql == "name: 'testname'"
