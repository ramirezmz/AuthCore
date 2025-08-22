import sqlite3
import bcrypt
from datetime import datetime
import uuid

from config.settings import settings


def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            last_login TIMESTAMP NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        );
        """
    )
    conn.commit()


def hash_password(password: str) -> str:
    """Gera hash usando bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def populate_users(conn):
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()
    password = hash_password("123456")

    users = []

    admin_names = [
        "Tony Stark", "Nick Fury", "Pepper Potts", "Maria Hill",
        "Phil Coulson", "Happy Hogan", "Wong", "Okoye", "Shuri", "Heimdall"
    ]
    user_names = [
        "Peter Parker", "Steve Rogers", "Natasha Romanoff",
        "Bruce Banner", "Clint Barton"
    ]
    invited_names = [
        "Groot", "Rocket Raccoon"
    ]

    # Create 10 admin users
    for i, name in enumerate(admin_names, 1):
        users.append(
            (
                str(uuid.uuid4()),
                f"admin{i}@example.com",
                name,
                password,
                "admin",
                None,
                now,
                now,
            )
        )

    # Create 5 normal users
    for i, name in enumerate(user_names, 1):
        users.append(
            (
                str(uuid.uuid4()),
                f"user{i}@example.com",
                name,
                password,
                "user",
                None,
                now,
                now,
            )
        )

    # Create 2 invited users
    for i, name in enumerate(invited_names, 1):
        users.append(
            (
                str(uuid.uuid4()),
                f"guest{i}@example.com",
                name,
                password,
                "invited",
                None,
                now,
                now,
            )
        )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO users
        (id, email, name, password, role, last_login, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        users,
    )
    conn.commit()


if __name__ == "__main__":
    db_path = settings.DB_PATH
    conn = sqlite3.connect(db_path)
    create_tables(conn)
    populate_users(conn)
    conn.close()
    print("✅ Database populated successfully!")
