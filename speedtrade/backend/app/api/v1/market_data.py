"""
Market data API endpoints.
"""
from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Query
from loguru import logger

from app.core.security import get_current_user_id
from app.services.market_data_service import get_market_data_service
from app.schemas.market_data import (
    QuoteResponse,
    SearchResult,
    SearchResponse,
    ChartData,
    ChartResponse
)


router = APIRouter(prefix="/market", tags=["Market Data"])


@router.get("/quote/{symbol}", response_model=QuoteResponse)
async def get_quote(
    symbol: str,
    user_id: int = Depends(get_current_user_id)
):
    """
    Get real-time quote for a symbol.
    
    Returns:
    - Current bid/ask prices
    - Last trade price and volume
    - Daily high/low
    - Previous close
    """
    market_service = get_market_data_service()
    
    try:
        quote = await market_service.get_quote(symbol)
        return quote
    except Exception as e:
        logger.error(f"Failed to get quote for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch quote for {symbol}"
        )


@router.get("/search", response_model=SearchResponse)
async def search_symbols(
    query: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=50, description="Number of results"),
    user_id: int = Depends(get_current_user_id)
):
    """
    Search for stocks and crypto by symbol or name.
    
    Returns matching symbols with names and asset types.
    """
    market_service = get_market_data_service()
    
    try:
        results = await market_service.search_symbols(query, limit)
        return SearchResponse(results=results, total=len(results))
    except Exception as e:
        logger.error(f"Failed to search symbols: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search symbols"
        )


@router.get("/chart/{symbol}", response_model=ChartResponse)
async def get_chart_data(
    symbol: str,
    interval: str = Query("1D", description="Time interval (1m, 5m, 15m, 1h, 1D)"),
    period: str = Query("1D", description="Time period (1D, 5D, 1M, 3M, 1Y)"),
    user_id: int = Depends(get_current_user_id)
):
    """
    Get historical chart data for a symbol.
    
    Intervals:
    - 1m, 5m, 15m, 30m: Intraday (1 minute to 30 minutes)
    - 1h, 4h: Hourly
    - 1D: Daily
    
    Periods:
    - 1D: One day
    - 5D: Five days
    - 1M: One month
    - 3M: Three months
    - 6M: Six months
    - 1Y: One year
    """
    market_service = get_market_data_service()
    
    try:
        chart_data = await market_service.get_chart_data(symbol, interval, period)
        return ChartResponse(
            symbol=symbol,
            interval=interval,
            period=period,
            data=chart_data
        )
    except Exception as e:
        logger.error(f"Failed to get chart data for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch chart data for {symbol}"
        )


@router.get("/movers/gainers", response_model=List[QuoteResponse])
async def get_top_gainers(
    limit: int = Query(10, ge=1, le=50),
    user_id: int = Depends(get_current_user_id)
):
    """Get top gaining stocks of the day."""
    market_service = get_market_data_service()
    
    try:
        gainers = await market_service.get_top_gainers(limit)
        return gainers
    except Exception as e:
        logger.error(f"Failed to get top gainers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch top gainers"
        )


@router.get("/movers/losers", response_model=List[QuoteResponse])
async def get_top_losers(
    limit: int = Query(10, ge=1, le=50),
    user_id: int = Depends(get_current_user_id)
):
    """Get top losing stocks of the day."""
    market_service = get_market_data_service()
    
    try:
        losers = await market_service.get_top_losers(limit)
        return losers
    except Exception as e:
        logger.error(f"Failed to get top losers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch top losers"
        )
