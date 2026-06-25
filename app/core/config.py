from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Star Wars API"
    SWAPI_BASE_URL: str = "https://swapi.py4e.com/api"
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_MIN_POOL: int = 1
    DB_MAX_POOL: int = 5

    class Config:
        env_file = ".env"


settings = Settings()
