from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.order import Order, OrderStatus
from app.schemas.order import OrderCreate, OrderResponse
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new order"""
    
    # Validate limit and stop prices based on order type
    if order_data.order_type.value == "limit" and not order_data.limit_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit price required for limit orders"
        )
    
    if order_data.order_type.value in ["stop", "stop_limit"] and not order_data.stop_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stop price required for stop orders"
        )
    
    # Create order in database
    new_order = Order(
        user_id=current_user.id,
        symbol=order_data.symbol.upper(),
        side=order_data.side,
        order_type=order_data.order_type,
        quantity=order_data.quantity,
        limit_price=order_data.limit_price,
        stop_price=order_data.stop_price,
        status=OrderStatus.PENDING
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    # TODO: Submit order to Alpaca/CCXT
    # For now, we just create it in our database
    
    return new_order


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: str = None,
    symbol: str = None
):
    """List user's orders with optional filters"""
    
    query = db.query(Order).filter(Order.user_id == current_user.id)
    
    if status:
        try:
            order_status = OrderStatus[status.upper()]
            query = query.filter(Order.status == order_status)
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {status}"
            )
    
    if symbol:
        query = query.filter(Order.symbol == symbol.upper())
    
    orders = query.order_by(Order.created_at.desc()).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get order details by ID"""
    
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel an order"""
    
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if order can be cancelled
    if order.status in [OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel order with status: {order.status.value}"
        )
    
    # Update order status
    order.status = OrderStatus.CANCELLED
    db.commit()
    
    # TODO: Cancel order in Alpaca/CCXT
    
    return None
