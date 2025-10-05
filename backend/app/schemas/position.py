from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PositionResponse(BaseModel):
    """Schema for position response"""
    id: int
    user_id: int
    symbol: str
    quantity: float
    average_entry_price: float
    current_price: Optional[float]
    market_value: Optional[float]
    cost_basis: float
    unrealized_pl: float
    unrealized_pl_percent: float
    asset_type: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
