from sqlalchemy import Column, String, Boolean, DateTime, Enum, Numeric, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class KYCStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class AccountType(str, enum.Enum):
    CASH = "cash"
    MARGIN = "margin"


class AccountStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    
    # KYC
    kyc_status = Column(Enum(KYCStatus), default=KYCStatus.PENDING)
    kyc_level = Column(Integer, default=0)
    
    # Account
    account_type = Column(Enum(AccountType), default=AccountType.CASH)
    account_status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=False)
    
    # Privacy settings (stored as JSON in production, simplified here)
    show_real_name = Column(Boolean, default=True)
    allow_location_history = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User {self.username}>"


class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Balances
    total_value = Column(Numeric(20, 2), default=0)
    cash_balance = Column(Numeric(20, 2), default=0)
    buying_power = Column(Numeric(20, 2), default=0)
    equity = Column(Numeric(20, 2), default=0)
    
    # P&L
    daily_pnl = Column(Numeric(20, 2), default=0)
    daily_pnl_percent = Column(Numeric(10, 4), default=0)
    total_pnl = Column(Numeric(20, 2), default=0)
    total_pnl_percent = Column(Numeric(10, 4), default=0)
    
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Portfolio {self.user_id}>"
