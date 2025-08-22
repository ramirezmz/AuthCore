from core.ports.user_repository import UserRepository
from core.utils.validate_query import UserQuery
from adapters.web.schemas.user_schema import UserListAllResponse


def get_all_users(
    user_repository: UserRepository,
    query: UserQuery
) -> UserListAllResponse:
    users = user_repository.get_all_users(query)

    return users
