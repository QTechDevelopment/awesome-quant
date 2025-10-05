"""
Order management API endpoints.
"""
from typing import List, Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from loguru import logger

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.services.trading_service import get_trading_service
from app.models.trading import OrderStatus
from app.schemas.orders import (
    OrderRequest,
    OrderResponse,
    OrderListResponse,
    CancelOrderResponse
)


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(
    order_data: OrderRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Place a new trading order.
    
    - Validates order parameters
    - Checks buying power and positions
    - Submits to broker (Alpaca or CCXT)
    - Returns order confirmation
    """
    trading_service = get_trading_service()
    
    try:
        order = await trading_service.place_order(
            db=db,
            user_id=user_id,
            symbol=order_data.symbol,
            side=order_data.side,
            order_type=order_data.order_type,
            quantity=order_data.quantity,
            asset_type=order_data.asset_type,
            limit_price=order_data.limit_price,
            stop_price=order_data.stop_price,
            time_in_force=order_data.time_in_force
        )
        
        return OrderResponse.from_orm(order)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to place order: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to place order"
        )


@router.get("", response_model=OrderListResponse)
async def get_orders(
    status: Optional[OrderStatus] = Query(None, description="Filter by order status"),
    limit: int = Query(50, ge=1, le=200, description="Number of orders to return"),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get user's order history.
    
    - Returns list of orders
    - Can filter by status
    - Sorted by creation time (newest first)
    """
    trading_service = get_trading_service()
    
    orders = trading_service.get_orders(
        db=db,
        user_id=user_id,
        status=status,
        limit=limit
    )
    
    return OrderListResponse(
        orders=[OrderResponse.from_orm(order) for order in orders],
        total=len(orders)
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get details of a specific order.
    """
    from app.models.trading import Order
    from sqlalchemy import and_
    
    order = db.query(Order).filter(
        and_(Order.id == order_id, Order.user_id == user_id)
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Sync order status with broker
    trading_service = get_trading_service()
    await trading_service.sync_order_status(db, order_id)
    
    db.refresh(order)
    return OrderResponse.from_orm(order)


@router.delete("/{order_id}", response_model=CancelOrderResponse)
async def cancel_order(
    order_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Cancel a pending order.
    
    - Can only cancel orders in PENDING or SUBMITTED status
    - Sends cancellation request to broker
    """
    trading_service = get_trading_service()
    
    try:
        order = await trading_service.cancel_order(
            db=db,
            order_id=order_id,
            user_id=user_id
        )
        
        return CancelOrderResponse(
            order_id=order.id,
            status=order.status,
            message="Order cancelled successfully"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to cancel order {order_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel order"
        )
