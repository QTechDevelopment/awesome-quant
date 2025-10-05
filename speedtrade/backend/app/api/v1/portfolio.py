"""
Portfolio and position management API endpoints.
"""
from typing import List, Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.user import Portfolio
from app.models.trading import Position, AssetType
from app.schemas.portfolio import (
    PortfolioResponse,
    PositionResponse,
    PositionListResponse
)


router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("", response_model=PortfolioResponse)
async def get_portfolio(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get user's portfolio summary.
    
    Returns:
    - Cash balance
    - Crypto balance
    - Total equity value
    - Unrealized P&L
    - Realized P&L
    """
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == user_id).first()
    
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portfolio not found"
        )
    
    # Get all positions
    positions = db.query(Position).filter(
        and_(Position.user_id == user_id, Position.quantity > 0)
    ).all()
    
    # Calculate total position value
    # In production, you'd get real-time prices here
    position_value = sum(
        pos.quantity * pos.average_entry_price for pos in positions
    )
    
    # Calculate total equity
    total_equity = portfolio.cash_balance + portfolio.crypto_balance + position_value
    
    return PortfolioResponse(
        user_id=portfolio.user_id,
        cash_balance=portfolio.cash_balance,
        crypto_balance=portfolio.crypto_balance,
        position_value=position_value,
        total_equity=total_equity,
        unrealized_pnl=portfolio.unrealized_pnl,
        realized_pnl=portfolio.realized_pnl,
        total_pnl=portfolio.unrealized_pnl + portfolio.realized_pnl,
        updated_at=portfolio.updated_at
    )


@router.get("/positions", response_model=PositionListResponse)
async def get_positions(
    asset_type: Optional[AssetType] = None,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get user's open positions.
    
    Can filter by asset type (stock/crypto).
    """
    query = db.query(Position).filter(
        and_(Position.user_id == user_id, Position.quantity > 0)
    )
    
    if asset_type:
        query = query.filter(Position.asset_type == asset_type)
    
    positions = query.all()
    
    # In production, you'd get real-time prices and calculate current values
    position_responses = []
    for pos in positions:
        current_price = pos.average_entry_price  # TODO: Get real-time price
        current_value = pos.quantity * current_price
        unrealized_pnl = current_value - (pos.quantity * pos.average_entry_price)
        unrealized_pnl_pct = (unrealized_pnl / (pos.quantity * pos.average_entry_price)) * 100
        
        position_responses.append(
            PositionResponse(
                id=pos.id,
                symbol=pos.symbol,
                asset_type=pos.asset_type,
                quantity=pos.quantity,
                average_entry_price=pos.average_entry_price,
                current_price=current_price,
                current_value=current_value,
                cost_basis=pos.quantity * pos.average_entry_price,
                unrealized_pnl=unrealized_pnl,
                unrealized_pnl_pct=unrealized_pnl_pct,
                realized_pnl=pos.realized_pnl,
                opened_at=pos.opened_at,
                updated_at=pos.updated_at
            )
        )
    
    return PositionListResponse(
        positions=position_responses,
        total=len(position_responses)
    )


@router.get("/positions/{symbol}", response_model=PositionResponse)
async def get_position(
    symbol: str,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific position.
    """
    position = db.query(Position).filter(
        and_(
            Position.user_id == user_id,
            Position.symbol == symbol,
            Position.quantity > 0
        )
    ).first()
    
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No open position found for {symbol}"
        )
    
    # Calculate current values
    current_price = position.average_entry_price  # TODO: Get real-time price
    current_value = position.quantity * current_price
    unrealized_pnl = current_value - (position.quantity * position.average_entry_price)
    unrealized_pnl_pct = (unrealized_pnl / (position.quantity * position.average_entry_price)) * 100
    
    return PositionResponse(
        id=position.id,
        symbol=position.symbol,
        asset_type=position.asset_type,
        quantity=position.quantity,
        average_entry_price=position.average_entry_price,
        current_price=current_price,
        current_value=current_value,
        cost_basis=position.quantity * position.average_entry_price,
        unrealized_pnl=unrealized_pnl,
        unrealized_pnl_pct=unrealized_pnl_pct,
        realized_pnl=position.realized_pnl,
        opened_at=position.opened_at,
        updated_at=position.updated_at
    )
