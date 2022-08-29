from pickle import FALSE
from pydantic import BaseSettings

import os



class CommonSettings(BaseSettings):
    APP_NAME: str = "salt-task"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL_PROD: str = os.getenv("DB_URL_PROD")



class JwtTokenSettings(BaseSettings):
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    ALGORITHM: str = "HS256"


class Settings(CommonSettings, JwtTokenSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
