from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI SQLite Service"
    database_url: str = "sqlite:///./app.db"
    api_key: str = "changeme"

    class Config:
        env_file = ".env"


settings = Settings()
