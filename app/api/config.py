from fastapi import APIRouter
from pydantic import BaseSettings
from dotenv import dotenv_values

config = dotenv_values(".env")


class CommonSettings(BaseSettings):
    APP_NAME: str = "salt-task"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str = config["DB_URL"]
    DB_NAME: str = config["DB_NAME"]


class JwtTokenSettings(BaseSettings):
    JWT_SECRET_KEY: str = config["JWT_SECRET_KEY"]
    JWT_REFRESH_SECRET_KEY: str = config["JWT_REFRESH_SECRET_KEY"]
    ALGORITHM: str = "HS256"


class Settings(CommonSettings, JwtTokenSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
