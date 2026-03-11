from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI SQLite Service"
    database_url: str = "sqlite:///./app.db"
    api_key: str = "changeme"

    model_config = ConfigDict(env_file=".env")


settings = Settings()
