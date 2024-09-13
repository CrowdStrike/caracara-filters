"""Prevention policy-specific filters."""

from caracara_filters import FQLGenerator


def test_prevention_policies_platform():
    """Test that the platform filter is properly inherited from the base filters."""
    fql_generator = FQLGenerator(dialect="prevention_policies")
    fql_generator.create_new_filter("OS", "Windows")
    fql = fql_generator.get_fql()
    assert fql == "platform_name: 'Windows'"
