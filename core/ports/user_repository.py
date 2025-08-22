from abc import ABC, abstractmethod
from core.entities.user import User
from core.utils.validate_query import UserQuery
from adapters.web.schemas.user_schema import (
    UserListAllResponse,
    UserResponse,
)


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User | None:
        pass

    @abstractmethod
    def get_all_users(self, query: UserQuery) -> UserListAllResponse:
        pass

    @abstractmethod
    def update_one_user(
        self,
        user_id: str,
        user: User
    ) -> UserResponse | None:
        pass
