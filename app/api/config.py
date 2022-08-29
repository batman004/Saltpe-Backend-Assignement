from pickle import FALSE
from pydantic import BaseSettings
from dotenv import dotenv_values

config = dotenv_values(".env")


class CommonSettings(BaseSettings):
    APP_NAME: str = "salt-task"
    DEBUG_MODE: bool = FALSE


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL_PROD: str = config["DB_URL_PROD"]



class JwtTokenSettings(BaseSettings):
    JWT_SECRET_KEY: str = config["JWT_SECRET_KEY"]
    JWT_REFRESH_SECRET_KEY: str = config["JWT_REFRESH_SECRET_KEY"]
    ALGORITHM: str = "HS256"


class Settings(CommonSettings, JwtTokenSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
