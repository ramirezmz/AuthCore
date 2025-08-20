import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    DB_PATH: str = os.getenv("DB_PATH", str(BASE_DIR / "authcore.db"))
    DATABASE_URL: str = f"sqlite:///{DB_PATH}"
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXP_HOURS: int = int(os.getenv("JWT_EXP_HOURS", "24"))


settings = Settings()
