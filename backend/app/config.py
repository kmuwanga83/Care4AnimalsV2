from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "CARE4ANIMALS API"
    database_url: str = "postgresql+psycopg://care4animals:care4animals@localhost:5432/care4animals"
    frontend_url: str = "http://localhost:5173"
    rapidpro_secret: str = "change-me"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
