"""
Pydantic schemas for market data.
"""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class QuoteResponse(BaseModel):
    """Real-time quote response."""
    symbol: str
    bid_price: Decimal
    ask_price: Decimal
    last_price: Decimal
    last_volume: int
    high: Decimal
    low: Decimal
    open: Decimal
    previous_close: Decimal
    change: Decimal
    change_percent: Decimal
    volume: int
    timestamp: datetime


class SearchResult(BaseModel):
    """Symbol search result."""
    symbol: str
    name: str
    asset_type: str
    exchange: Optional[str] = None


class SearchResponse(BaseModel):
    """Search results response."""
    results: List[SearchResult]
    total: int


class ChartData(BaseModel):
    """Single chart data point."""
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


class ChartResponse(BaseModel):
    """Chart data response."""
    symbol: str
    interval: str
    period: str
    data: List[ChartData]
