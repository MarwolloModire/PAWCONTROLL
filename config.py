from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/postgres"

    class Config:
        env_file = ".env"


settings = Settings()
