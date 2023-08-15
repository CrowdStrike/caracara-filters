from caracara_filters import FQLGenerator


def test_users_assigned_cids():
    fql_generator = FQLGenerator(dialect='users')
    fql_generator.create_new_filter("assignedcids", ["abcdefg", "123456"])
    fql = fql_generator.get_fql()
    assert fql == "assigned_cids: ['abcdefg','123456']"


def test_users_home_cid():
    fql_generator = FQLGenerator(dialect='users')
    fql_generator.create_new_filter("cid", ["abcdefg", "123456"])
    fql = fql_generator.get_fql()
    assert fql == "cid: ['abcdefg','123456']"


def test_users_first_name():
    fql_generator = FQLGenerator(dialect='users')
    fql_generator.create_new_filter("firstname", "test")
    fql = fql_generator.get_fql()
    assert fql == "first_name: 'test'"


def test_users_last_name():
    fql_generator = FQLGenerator(dialect='users')
    fql_generator.create_new_filter("last_name", "Smith")
    fql = fql_generator.get_fql()
    assert fql == "last_name: 'Smith'"


def test_users_name():
    fql_generator = FQLGenerator(dialect='users')
    fql_generator.create_new_filter("name", "John Smith")
    fql = fql_generator.get_fql()
    assert fql == "name: 'John Smith'"
