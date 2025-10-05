"""
Pydantic schemas for orders.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.trading import (
    OrderSide,
    OrderType,
    OrderStatus,
    TimeInForce,
    AssetType
)


class OrderRequest(BaseModel):
    """Order placement request."""
    symbol: str = Field(..., description="Trading symbol (e.g., AAPL, BTC/USD)")
    side: OrderSide = Field(..., description="Buy or sell")
    order_type: OrderType = Field(..., description="Market, limit, stop, or stop_limit")
    quantity: Decimal = Field(..., gt=0, description="Order quantity")
    asset_type: AssetType = Field(..., description="Stock or crypto")
    limit_price: Optional[Decimal] = Field(None, gt=0, description="Limit price for limit orders")
    stop_price: Optional[Decimal] = Field(None, gt=0, description="Stop price for stop orders")
    time_in_force: TimeInForce = Field(default=TimeInForce.DAY, description="Order duration")
    
    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "side": "buy",
                "order_type": "limit",
                "quantity": "10",
                "asset_type": "stock",
                "limit_price": "150.00",
                "time_in_force": "day"
            }
        }


class OrderResponse(BaseModel):
    """Order response."""
    id: int
    user_id: int
    symbol: str
    side: OrderSide
    type: OrderType
    quantity: Decimal
    filled_quantity: Decimal
    limit_price: Optional[Decimal]
    stop_price: Optional[Decimal]
    filled_avg_price: Optional[Decimal]
    time_in_force: TimeInForce
    status: OrderStatus
    asset_type: AssetType
    broker_order_id: Optional[str]
    rejection_reason: Optional[str]
    created_at: datetime
    submitted_at: Optional[datetime]
    filled_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """List of orders response."""
    orders: List[OrderResponse]
    total: int


class CancelOrderResponse(BaseModel):
    """Order cancellation response."""
    order_id: int
    status: OrderStatus
    message: str
