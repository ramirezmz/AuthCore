import pytest

from core.use_cases.authenticate_user import (
    authenticate_user,
    AuthenticationError,
)
from adapters.db.sqlite_user_repository import SQLiteUserRepository

user_data = {"email": "admin1@example.com", "password": "123456"}


def test_authenticate_user_success():
    """Deve autenticar com sucesso e retornar um token"""

    repo = SQLiteUserRepository()
    token = authenticate_user(repo, user_data["email"], user_data["password"])
    user = repo.get_by_email(user_data["email"])
    if not user:
        raise Exception("User not found")

    assert len(token) > 80
    assert user.last_login is not None


def test_authenticate_user_invalid_password():
    """Deve lançar AuthenticationError se a senha for inválida"""

    repo = SQLiteUserRepository()

    with pytest.raises(AuthenticationError) as exc:
        authenticate_user(repo, user_data["email"], "wrong")

    assert "Invalid credentials" in str(exc.value)


def test_authenticate_user_user_not_found():
    """Deve lançar AuthenticationError se o usuário não for encontrado"""

    repo = SQLiteUserRepository()

    with pytest.raises(AuthenticationError):
        authenticate_user(repo, "notfound@example.com", "secret")
