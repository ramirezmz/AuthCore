from core.utils.password_utils import encrypt_password
from core.entities.user import User
from core.ports.user_repository import UserRepository
from core.entities.user import UserRole


def create_user(
    user_repository: UserRepository,
    email: str,
    name: str,
    password: str,
    role: str = "user",
) -> User:
    hashed_password = encrypt_password(password)
    valid_role = UserRole(role)
    user = User(
        email=email,
        name=name,
        password=hashed_password,
        role=valid_role,
    )

    return user_repository.save(user)
