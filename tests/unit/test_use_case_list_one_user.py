
from adapters.db.sqlite_user_repository import SQLiteUserRepository
from core.use_cases.list_one_user import get_user


def test_list_one_user_success():
    """ Should be able to return the user details """

    repo = SQLiteUserRepository()
    user = get_user(repo, user_id="9e36d083-3a30-4a81-b5c7-536c39e134cc")
    assert user is not None
    assert user.email == "admin@example.com"
    assert user.name == "Admin User"


def test_list_one_user_not_found():
    """ Should return user not found for a non-existing user """

    repo = SQLiteUserRepository()
    try:
        user = get_user(repo, user_id="non-existing-id")
        assert user is None
    except Exception as e:
        assert str(e) == "404: User not found"
