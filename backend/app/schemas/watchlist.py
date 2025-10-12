from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class WatchlistItemCreate(BaseModel):
    """Schema for creating a watchlist item"""
    symbol: str = Field(..., min_length=1, max_length=20)
    asset_type: str = Field(..., pattern="^(stock|crypto)$")


class WatchlistItemResponse(BaseModel):
    """Schema for watchlist item response"""
    id: int
    watchlist_id: int
    symbol: str
    asset_type: str
    added_at: datetime
    
    class Config:
        from_attributes = True


class WatchlistCreate(BaseModel):
    """Schema for creating a watchlist"""
    name: str = Field(..., min_length=1, max_length=100)


class WatchlistResponse(BaseModel):
    """Schema for watchlist response"""
    id: int
    user_id: int
    name: str
    created_at: datetime
    items: Optional[List[WatchlistItemResponse]] = []
    
    class Config:
        from_attributes = True
