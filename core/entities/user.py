import re
import uuid
from datetime import datetime
from enum import Enum


class UserRole(Enum):
    """
    Enum representing the possible roles a user can have in the system.
    """

    ADMIN = "admin"
    USER = "user"
    INVITED = "invited"


class User:

    def __init__(
        self,
        email: str,
        name: str,
        password: str,
        role: UserRole = UserRole.USER,
        last_login: datetime | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        id: str | None = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.email = self._validate_email(email)
        self.name = name
        self.password = password
        self.role = role
        self.last_login = last_login
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def _validate_email(self, email: str) -> str:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return email

    def update_last_login(self) -> None:
        self.last_login = datetime.utcnow()

    def change_password(self, new_password: str) -> None:
        self.password = new_password
        self._touch()

    def _touch(self) -> None:
        self.updated_at = datetime.utcnow()
