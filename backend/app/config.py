from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/blink_customers"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Microsoft Graph API (SharePoint)
    MICROSOFT_TENANT_ID: Optional[str] = None
    MICROSOFT_CLIENT_ID: Optional[str] = None
    MICROSOFT_CLIENT_SECRET: Optional[str] = None
    SHAREPOINT_SITE_ID: Optional[str] = None
    SHAREPOINT_DRIVE_ID: Optional[str] = None
    
    # Google Calendar API
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[str] = "http://localhost:8000/auth/google/callback"
    GOOGLE_CALENDAR_ID: Optional[str] = "primary"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://frontend:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
