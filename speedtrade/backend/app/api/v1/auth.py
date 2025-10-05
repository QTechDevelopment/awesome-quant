"""
Authentication API endpoints.
"""
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from loguru import logger

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
    get_current_user_id
)
from app.models.user import User, Portfolio, KYCStatus, AccountType, AccountStatus
from app.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    UserResponse,
    RefreshTokenRequest
)


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    - Creates user account
    - Initializes portfolio with $0 balance
    - Sets KYC status to PENDING
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Create user
    user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        password_hash=get_password_hash(user_data.password),
        kyc_status=KYCStatus.PENDING,
        account_type=AccountType.CASH,
        account_status=AccountStatus.ACTIVE
    )
    db.add(user)
    db.flush()
    
    # Create portfolio
    portfolio = Portfolio(
        user_id=user.id,
        cash_balance=0
    )
    db.add(portfolio)
    db.commit()
    db.refresh(user)
    
    logger.info(f"New user registered: {user.email}")
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        kyc_status=user.kyc_status,
        account_type=user.account_type,
        account_status=user.account_status,
        created_at=user.created_at
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    """
    Login with email/username and password.
    
    Returns access token and refresh token.
    """
    # Find user by email or username
    user = db.query(User).filter(
        (User.email == form_data.username) | (User.username == form_data.username)
    ).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    if user.account_status != AccountStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account is {user.account_status.value}"
        )
    
    # Create tokens
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    logger.info(f"User logged in: {user.email}")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    """
    try:
        payload = decode_token(request.refresh_token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Verify user exists and is active
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.account_status != AccountStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new tokens
    access_token = create_access_token({"sub": str(user_id)})
    new_refresh_token = create_refresh_token({"sub": str(user_id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user's profile.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        kyc_status=user.kyc_status,
        account_type=user.account_type,
        account_status=user.account_status,
        created_at=user.created_at
    )


@router.post("/logout")
async def logout(
    user_id: str = Depends(get_current_user_id)
):
    """
    Logout current user.
    
    Note: With JWT, actual logout is handled client-side by removing tokens.
    This endpoint is for logging purposes.
    """
    logger.info(f"User logged out: {user_id}")
    return {"message": "Successfully logged out"}
