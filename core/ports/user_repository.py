from abc import ABC, abstractmethod
from core.entities.user import User


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
