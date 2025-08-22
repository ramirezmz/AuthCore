import sqlite3
import pytest
from adapters.db.sqlite_user_repository import SQLiteUserRepository
from core.use_cases.list_users import get_all_users
from core.utils.validate_query import UserQuery
from config.settings import settings

from scripts.populate_db import create_tables, populate_users, remove_users


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    db_path = settings.DB_PATH
    connection = sqlite3.connect(db_path)
    create_tables(connection)
    remove_users(connection)
    populate_users(connection)


def test_list_all_users_success():
    """Should be able to return first 10 users with details"""
    repo = SQLiteUserRepository()

    result = get_all_users(repo, UserQuery(
        page=1, limit=10, role=None, q=None, order=1))

    assert result is not None
    assert len(result.users) == 10


def test_list_all_users_admin_only():
    """Should return all users admin only by query"""
    repo = SQLiteUserRepository()

    result = get_all_users(repo, UserQuery(
        page=1, limit=10, role="admin", q=None, order=1))

    assert result is not None
    assert len(result.users) == 10
    assert all(user.role == "admin" for user in result.users)


def test_list_all_users_query_q():
    """Should return all users matching query"""
    repo = SQLiteUserRepository()

    result = get_all_users(repo, UserQuery(
        page=1, limit=10, role=None, q="Peter", order=1))

    assert result is not None
    assert len(result.users) == 1
    assert result.users[0].name == "Peter Parker"
