"""
Pydantic schemas for portfolio and positions.
"""
from datetime import datetime
from decimal import Decimal
from typing import List
from pydantic import BaseModel

from app.models.trading import AssetType


class PortfolioResponse(BaseModel):
    """Portfolio summary response."""
    user_id: int
    cash_balance: Decimal
    crypto_balance: Decimal
    position_value: Decimal
    total_equity: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
    total_pnl: Decimal
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PositionResponse(BaseModel):
    """Position details response."""
    id: int
    symbol: str
    asset_type: AssetType
    quantity: Decimal
    average_entry_price: Decimal
    current_price: Decimal
    current_value: Decimal
    cost_basis: Decimal
    unrealized_pnl: Decimal
    unrealized_pnl_pct: Decimal
    realized_pnl: Decimal
    opened_at: datetime
    updated_at: datetime


class PositionListResponse(BaseModel):
    """List of positions response."""
    positions: List[PositionResponse]
    total: int
