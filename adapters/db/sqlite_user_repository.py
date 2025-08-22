import sqlite3
from core.entities.user import User
from core.ports.user_repository import UserRepository
from config.settings import settings


class SQLiteUserRepository(UserRepository):
    def __init__(self):
        self.connection = sqlite3.connect(
            settings.DB_PATH, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row

    def save(self, user: User) -> User:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                (
                    "INSERT INTO users (id, email, name, password, role, "
                    "last_login, created_at, updated_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                ),
                (
                    user.id,
                    user.email,
                    user.name,
                    user.password,
                    user.role,
                    user.last_login,
                    user.created_at,
                    user.updated_at,
                ),
            )
            self.connection.commit()
            return user
        except Exception as error:
            self.connection.rollback()
            raise error
        finally:
            cursor.close()

    def get_by_email(self, email: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return User(
                id=row["id"],
                email=row["email"],
                name=row["name"],
                password=row["password"],
                role=row["role"],
                last_login=row["last_login"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
        return None

    def get_user_by_id(self, user_id: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return User(
                id=row["id"],
                email=row["email"],
                name=row["name"],
                password=row["password"],
                role=row["role"],
                last_login=row["last_login"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
        return None
