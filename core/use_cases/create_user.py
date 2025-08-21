from core.utils.password_utils import encrypt_password
from core.entities.user import User
from core.ports.user_repository import UserRepository
from core.entities.user import UserRole
from adapters.web.schemas.user_schema import UserCreateRequest


def create_user(
    user_repository: UserRepository,
    body: UserCreateRequest,
) -> User:
    hashed_password = encrypt_password(body.password)
    role_enum = UserRole.validate(body.role.value)

    user = User(
        email=body.email,
        name=body.name,
        password=hashed_password,
        role=role_enum.value,
    )

    return user_repository.save(user)
