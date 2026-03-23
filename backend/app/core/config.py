from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "ZapKart"
    DEBUG: bool = True
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str = "sqlite:///./zapkart.db"

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
    ]

    REDIS_URL: str = "redis://localhost:6379"
    DELIVERY_TIME_MINUTES: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
