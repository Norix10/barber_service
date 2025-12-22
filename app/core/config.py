from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRES_MINUTES: int = 15 * 24 * 60

    SECRET_KEY: str
    DATABASE_URL: str 
    ECHO: bool = False

    class Config:
        env_file = str(ENV_PATH)
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()