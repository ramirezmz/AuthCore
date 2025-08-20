from core.ports.user_repository import UserRepository
from core.utils.password_utils import verify_password
from adapters.auth.jwt_auth_service import generate_token


class AuthenticationError(Exception):
    pass


def authenticate_user(
    user_repository: UserRepository,
    email: str,
    password: str,
) -> str:
    user = user_repository.get_by_email(email)
    if not user or not verify_password(password, user.password):
        raise AuthenticationError("Invalid credentials")
    token = generate_token(user)
    return token
