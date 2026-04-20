from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "CARE4ANIMALS API"
    # Defaulting to localhost for Git Bash development
    database_url: str = "postgresql+psycopg://care4animals:care4animals@localhost:5432/care4animals"
    frontend_url: str = "http://localhost:5173"
    rapidpro_secret: str = "change-me"
    
    # This tells Pydantic to look for a .env file, but we will ensure it's correct
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()