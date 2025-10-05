from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.order import OrderSide, OrderType, OrderStatus


class OrderCreate(BaseModel):
    """Schema for creating an order"""
    symbol: str = Field(..., min_length=1, max_length=20)
    side: OrderSide
    order_type: OrderType
    quantity: float = Field(..., gt=0)
    limit_price: Optional[float] = Field(None, gt=0)
    stop_price: Optional[float] = Field(None, gt=0)


class OrderResponse(BaseModel):
    """Schema for order response"""
    id: int
    user_id: int
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    limit_price: Optional[float]
    stop_price: Optional[float]
    filled_price: Optional[float]
    filled_quantity: float
    status: OrderStatus
    external_order_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    filled_at: Optional[datetime]
    
    class Config:
        from_attributes = True
