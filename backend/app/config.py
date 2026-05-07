from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "CARE4ANIMALS API"
    
    # Database Configuration
    database_url: str = "postgresql+psycopg://care4animals:care4animals@localhost:5432/care4animals"
    
    # Frontend/CORS Configuration
    frontend_url: str = "http://localhost:5173"
    
    # Africa's Talking SMS configuration
    at_username: str = "sandbox"
    at_api_key: str = "change-me"
    at_sender_id: str | None = None
    at_webhook_token: str | None = None
    # Comma-separated IPs/CIDRs allowed to hit inbound SMS (empty = skip IP check). Prefer token + reverse-proxy truthfulness.
    at_webhook_allowed_ips: str = ""
    sms_max_retries: int = 3
    sms_retry_backoff_seconds: float = 0.5

    # Email configuration (SMTP)
    email_provider: str = "smtp"
    smtp_host: str = "localhost"
    smtp_port: int = 25
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = False
    email_from: str = "no-reply@care4animals.local"
    
    # Other Integrations
    rapidpro_secret: str = "change-me"
    
    # Pydantic configuration to load from .env
    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore",
        env_file_encoding='utf-8'
    )

settings = Settings()