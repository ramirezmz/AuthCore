import pytest
import sqlite3
from adapters.db.sqlite_user_repository import SQLiteUserRepository
from config.settings import settings

from scripts.populate_db import create_tables, populate_users, remove_users


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    db_path = settings.DB_PATH
    connection = sqlite3.connect(db_path)
    create_tables(connection)
    remove_users(connection)
    populate_users(connection)


def test_delete_user_success():
    """Should be able to delete a user successfully"""
    repo = SQLiteUserRepository()
    user = repo.get_by_email("guest2@example.com")
    assert user is not None
    repo.delete_user(user.id)

    user = repo.get_by_email("guest2@example.com")
    assert user is None


def test_delete_user_not_found():
    """Should return 404 if user not found"""
    repo = SQLiteUserRepository()
    result = repo.delete_user("non_existing_id")
    assert not result
