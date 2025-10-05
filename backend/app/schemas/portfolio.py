from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PortfolioResponse(BaseModel):
    """Schema for portfolio response"""
    id: int
    user_id: int
    cash_balance: float
    buying_power: float
    portfolio_value: float
    long_market_value: float
    short_market_value: float
    total_pl: float
    total_pl_percent: float
    day_pl: float
    day_pl_percent: float
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
