from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.watchlist import Watchlist, WatchlistItem
from app.schemas.watchlist import (
    WatchlistCreate,
    WatchlistResponse,
    WatchlistItemCreate,
    WatchlistItemResponse
)
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=WatchlistResponse, status_code=status.HTTP_201_CREATED)
async def create_watchlist(
    watchlist_data: WatchlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new watchlist"""
    
    new_watchlist = Watchlist(
        user_id=current_user.id,
        name=watchlist_data.name
    )
    
    db.add(new_watchlist)
    db.commit()
    db.refresh(new_watchlist)
    
    return new_watchlist


@router.get("/", response_model=List[WatchlistResponse])
async def list_watchlists(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List user's watchlists"""
    
    watchlists = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id
    ).all()
    
    return watchlists


@router.get("/{watchlist_id}", response_model=WatchlistResponse)
async def get_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get watchlist details by ID"""
    
    watchlist = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == current_user.id
    ).first()
    
    if not watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist not found"
        )
    
    return watchlist


@router.delete("/{watchlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a watchlist"""
    
    watchlist = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == current_user.id
    ).first()
    
    if not watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist not found"
        )
    
    db.delete(watchlist)
    db.commit()
    
    return None


@router.post("/{watchlist_id}/items", response_model=WatchlistItemResponse, status_code=status.HTTP_201_CREATED)
async def add_item_to_watchlist(
    watchlist_id: int,
    item_data: WatchlistItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a stock/crypto to watchlist"""
    
    # Verify watchlist exists and belongs to user
    watchlist = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == current_user.id
    ).first()
    
    if not watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist not found"
        )
    
    # Check if item already exists
    existing_item = db.query(WatchlistItem).filter(
        WatchlistItem.watchlist_id == watchlist_id,
        WatchlistItem.symbol == item_data.symbol.upper()
    ).first()
    
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Symbol {item_data.symbol.upper()} already exists in watchlist"
        )
    
    # Create new item
    new_item = WatchlistItem(
        watchlist_id=watchlist_id,
        symbol=item_data.symbol.upper(),
        asset_type=item_data.asset_type
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return new_item


@router.delete("/{watchlist_id}/items/{symbol}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item_from_watchlist(
    watchlist_id: int,
    symbol: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a stock/crypto from watchlist"""
    
    # Verify watchlist exists and belongs to user
    watchlist = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == current_user.id
    ).first()
    
    if not watchlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist not found"
        )
    
    # Find and delete item
    item = db.query(WatchlistItem).filter(
        WatchlistItem.watchlist_id == watchlist_id,
        WatchlistItem.symbol == symbol.upper()
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in watchlist"
        )
    
    db.delete(item)
    db.commit()
    
    return None
