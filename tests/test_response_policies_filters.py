"""Test response policy-specific filters."""
from caracara_filters import FQLGenerator


def test_response_policies_platform():
    """Ensure the response policies dialect properly inherits the base filters."""
    fql_generator = FQLGenerator(dialect='response_policies')
    fql_generator.create_new_filter("platform_name", "Linux")
    fql = fql_generator.get_fql()
    assert fql == "platform_name: 'Linux'"
