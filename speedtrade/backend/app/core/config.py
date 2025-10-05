from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache
from pydantic import field_validator


class Settings(BaseSettings):
    # App
    APP_NAME: str = "SpeedTrade"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "change-this-in-production"
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    @field_validator('ALLOWED_ORIGINS')
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    # Database
    DATABASE_URL: str = "postgresql://speedtrade:password@localhost:5432/speedtrade_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Alpaca
    ALPACA_API_KEY: str = "your_alpaca_api_key"
    ALPACA_SECRET_KEY: str = "your_alpaca_secret_key"
    ALPACA_BASE_URL: str = "https://paper-api.alpaca.markets"
    ALPACA_PAPER_TRADING: bool = True
    
    # Crypto Exchanges
    COINBASE_API_KEY: Optional[str] = None
    COINBASE_SECRET: Optional[str] = None
    COINBASE_PASSPHRASE: Optional[str] = None
    
    # Market Data
    POLYGON_API_KEY: Optional[str] = None
    COINGECKO_API_KEY: Optional[str] = None
    
    # JWT
    JWT_SECRET_KEY: str = "jwt-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # KYC
    PLAID_CLIENT_ID: Optional[str] = None
    PLAID_SECRET: Optional[str] = None
    PLAID_ENV: str = "sandbox"
    
    # Email
    SENDGRID_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@speedtrade.com"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
