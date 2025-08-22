
import pytest
import sqlite3
from config.settings import settings
from scripts.populate_db import create_tables, populate_users, remove_users
from adapters.db.sqlite_user_repository import SQLiteUserRepository
from adapters.web.schemas.user_schema import AvailableUserUpdateRequest
from core.use_cases.update_user import update_user


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    db_path = settings.DB_PATH
    connection = sqlite3.connect(db_path)
    create_tables(connection)
    remove_users(connection)
    populate_users(connection)


def test_update_one_user_success():
    """ Should be able to update user """
    repo = SQLiteUserRepository()
    user = repo.get_by_email("user@example.com")
    if user:
        payload = {"name": "Roberto Gomes"}
        result = update_user(
            repo,
            user_id=user.id,
            user_data=AvailableUserUpdateRequest(**payload))  # type: ignore
        if not result:
            assert False, "User update failed"
        assert result.name == "Roberto Gomes"
        assert user.updated_at != result.updated_at
        assert user.created_at == result.created_at


def test_update_one_user_not_found():
    """ Should return None if user is not found """
    repo = SQLiteUserRepository()
    try:
        update_user(
            repo,
            user_id="non_existent_user_id",
            user_data=AvailableUserUpdateRequest(name="Roberto Gomes")
        )
    except Exception as e:
        assert str(e) == "404: User not found"
