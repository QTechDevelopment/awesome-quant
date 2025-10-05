from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.position import Position
from app.schemas.position import PositionResponse
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[PositionResponse])
async def list_positions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List user's current positions"""
    
    positions = db.query(Position).filter(
        Position.user_id == current_user.id,
        Position.quantity > 0  # Only active positions
    ).all()
    
    # TODO: Update current prices from Alpaca/CCXT
    
    return positions


@router.get("/{symbol}", response_model=PositionResponse)
async def get_position(
    symbol: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get position details for a specific symbol"""
    
    position = db.query(Position).filter(
        Position.user_id == current_user.id,
        Position.symbol == symbol.upper()
    ).first()
    
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No position found for symbol: {symbol}"
        )
    
    # TODO: Update current price from Alpaca/CCXT
    
    return position
