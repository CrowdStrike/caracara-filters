"""Test the base filters that are inherited by every dialect."""
from caracara_filters import FQLGenerator


def test_name_fql():
    """Test a name attribute from the base dialect with a static string value."""
    fql_generator = FQLGenerator(dialect='base')
    fql_generator.create_new_filter("name", "testname")
    fql = fql_generator.get_fql()
    assert fql == "name: 'testname'"
