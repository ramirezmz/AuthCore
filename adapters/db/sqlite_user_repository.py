import sqlite3
from core.entities.user import User
from core.utils.validate_query import UserQuery
from core.ports.user_repository import UserRepository
from config.settings import settings
from adapters.web.schemas.user_schema import UserListAllResponse, UserResponse


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

    def get_all_users(
        self,
        query: UserQuery
    ) -> UserListAllResponse:
        cursor = self.connection.cursor()
        base_sql = "FROM users WHERE 1=1"
        params = []

        if query.role:
            base_sql += " AND role = ?"
            params.append(query.role)
        if query.q:
            base_sql += " AND (email LIKE ? OR name LIKE ?)"
            params.extend([f"%{query.q}%", f"%{query.q}%"])

        count_sql = f"SELECT COUNT(*) as total {base_sql}"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()["total"]

        order_by = "ASC" if query.order == 1 else "DESC"
        sql = (
            "SELECT id, email, name, role, last_login, created_at, updated_at "
            f"{base_sql} ORDER BY created_at {order_by} LIMIT ? OFFSET ?"
        )

        params.extend([query.limit, (query.page - 1) * query.limit])

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        users = [
            UserResponse(
                id=row["id"],
                email=row["email"],
                name=row["name"],
                role=row["role"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
            for row in rows
        ]
        return UserListAllResponse(
            total=total,
            users=users
        )

    def update_one_user(self, user_id: str, user: User) -> UserResponse | None:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                (
                    "UPDATE users SET email = ?, name = ?, "
                    "role = ?, last_login = ?, created_at = ?, updated_at = ? "
                    "WHERE id = ?"
                ),
                (
                    user.email,
                    user.name,
                    user.role,
                    user.last_login,
                    user.created_at,
                    user.updated_at,
                    user_id,
                ),
            )
            self.connection.commit()
            # Fetch the updated user
            cursor.execute(
                (
                    "SELECT id, email, name, role, last_login, "
                    "created_at, updated_at "
                    "FROM users WHERE id = ?"
                ),
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return UserResponse(
                    id=row["id"],
                    email=row["email"],
                    name=row["name"],
                    role=row["role"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
            return None
        except Exception as error:
            self.connection.rollback()
            raise error
        finally:
            cursor.close()

    def delete_user(self, user_id: str) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.connection.commit()
            return cursor.rowcount > 0
        except Exception as error:
            self.connection.rollback()
            raise error
        finally:
            cursor.close()

    def update(self, user_id: str, user: User):
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                (
                    "UPDATE users SET email = ?, name = ?, "
                    "role = ?, last_login = ?, created_at = ?, updated_at = ? "
                    "WHERE id = ?"
                ),
                (
                    user.email,
                    user.name,
                    user.role,
                    user.last_login,
                    user.created_at,
                    user.updated_at,
                    user_id,
                ),
            )
            self.connection.commit()
        except Exception as error:
            self.connection.rollback()
            raise error
        finally:
            cursor.close()
