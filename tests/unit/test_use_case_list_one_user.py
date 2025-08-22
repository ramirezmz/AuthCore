
from adapters.db.sqlite_user_repository import SQLiteUserRepository
from core.use_cases.list_one_user import get_user


def test_list_one_user_success():
    """ Should be able to return the user details """

    repo = SQLiteUserRepository()
    target_user = repo.get_by_email("guest1@example.com")
    if not target_user:
        raise Exception("User not found")

    user = get_user(repo, user_id=target_user.id)
    assert user is not None
    assert user.email == target_user.email
    assert user.name == target_user.name


def test_list_one_user_not_found():
    """ Should return user not found for a non-existing user """

    repo = SQLiteUserRepository()
    try:
        user = get_user(repo, user_id="non-existing-id")
        assert user is None
    except Exception as e:
        assert str(e) == "404: User not found"
