"""
Pydantic schemas for authentication.
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from app.models.user import KYCStatus, AccountType, AccountStatus


class UserRegister(BaseModel):
    """User registration request."""
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    full_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=100)


class UserLogin(BaseModel):
    """User login request."""
    username: str  # Can be email or username
    password: str


class TokenResponse(BaseModel):
    """Token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


class UserResponse(BaseModel):
    """User profile response."""
    id: str
    email: str
    username: str
    full_name: str
    kyc_status: KYCStatus
    account_type: AccountType
    account_status: AccountStatus
    created_at: datetime
    
    class Config:
        from_attributes = True
