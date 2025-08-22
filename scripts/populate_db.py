import sys
import sqlite3
from datetime import datetime
import uuid

from config.settings import settings
from core.utils.password_utils import encrypt_password


def remove_users(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users;")
    conn.commit()


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


def populate_users(conn):
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()
    password = encrypt_password("123456")

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
    # Create admin users
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
    if len(sys.argv) < 2:
        print("Usage: python populate_db.py [add|remove|both]")
        sys.exit(1)

    action = sys.argv[1].lower()
    db_path = settings.DB_PATH
    conn = sqlite3.connect(db_path)
    create_tables(conn)

    if action == "remove":
        remove_users(conn)
        print("✅ All users removed from the database!")
    elif action == "add":
        populate_users(conn)
        print("✅ Database populated successfully!")
    elif action == "both":
        remove_users(conn)
        populate_users(conn)
        print("✅ Database cleaned and populated successfully!")
    else:
        print("Invalid argument. Use 'add', 'remove', or 'both'.")
        sys.exit(1)
    conn.close()
