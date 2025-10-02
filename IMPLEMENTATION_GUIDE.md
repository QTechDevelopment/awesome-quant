# 🛠️ SpeedTrade - Implementation Guide

## Table of Contents
1. [Development Environment Setup](#development-environment-setup)
2. [Backend Implementation](#backend-implementation)
3. [Frontend Implementation](#frontend-implementation)
4. [Trading Integration](#trading-integration)
5. [Database Setup](#database-setup)
6. [Real-Time Features](#real-time-features)
7. [Testing Strategy](#testing-strategy)
8. [Deployment Guide](#deployment-guide)

---

## Development Environment Setup

### Prerequisites

```bash
# Required Software
- Python 3.10+ (Backend)
- Node.js 18+ (Frontend)
- Docker & Docker Compose (Containerization)
- Git (Version control)
- PostgreSQL 15+ (Database)
- Redis 7+ (Cache)

# Optional but Recommended
- VS Code with extensions:
  - Python
  - ESLint
  - Prettier
  - Docker
  - Thunder Client (API testing)
```

### Initial Setup

#### 1. Clone and Initialize Project

```bash
# Create project directory
mkdir speedtrade && cd speedtrade

# Initialize Git
git init

# Create directory structure
mkdir -p backend frontend docker

# Initialize frontend
cd frontend
npm create vite@latest . -- --template react-ts
npm install

# Initialize backend
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib python-multipart

# Go back to root
cd ..
```

#### 2. Docker Compose Setup

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: speedtrade_postgres
    environment:
      POSTGRES_USER: speedtrade
      POSTGRES_PASSWORD: dev_password_change_in_prod
      POSTGRES_DB: speedtrade_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U speedtrade"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: speedtrade_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: speedtrade_backend
    environment:
      - DATABASE_URL=postgresql://speedtrade:dev_password_change_in_prod@postgres:5432/speedtrade_db
      - REDIS_URL=redis://redis:6379
      - SECRET_KEY=your-secret-key-change-in-prod
      - ALPACA_API_KEY=${ALPACA_API_KEY}
      - ALPACA_SECRET_KEY=${ALPACA_SECRET_KEY}
      - ALPACA_BASE_URL=https://paper-api.alpaca.markets  # Paper trading
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: speedtrade_frontend
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_WS_URL=ws://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host

volumes:
  postgres_data:
  redis_data:
```

#### 3. Environment Variables

Create `.env` file in project root:

```bash
# Database
DATABASE_URL=postgresql://speedtrade:dev_password_change_in_prod@localhost:5432/speedtrade_db

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-256-bit-secret-key-generate-with-openssl
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Alpaca (Paper Trading)
ALPACA_API_KEY=your_alpaca_paper_api_key
ALPACA_SECRET_KEY=your_alpaca_paper_secret_key
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Binance (Testnet)
BINANCE_API_KEY=your_binance_testnet_api_key
BINANCE_SECRET_KEY=your_binance_testnet_secret_key

# Polygon (Optional - for market data)
POLYGON_API_KEY=your_polygon_api_key

# Frontend
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

#### 4. Get API Keys

```bash
# 1. Alpaca (Free Paper Trading)
# Visit: https://alpaca.markets
# Sign up → Generate API keys (Paper trading)

# 2. Binance Testnet (Optional for crypto)
# Visit: https://testnet.binance.vision
# Create account → Generate API keys

# 3. Polygon.io (Optional - free tier available)
# Visit: https://polygon.io
# Sign up → Get API key
```

---

## Backend Implementation

### Project Structure

```bash
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration
│   ├── database.py             # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── order.py
│   │   ├── portfolio.py
│   │   └── position.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── order.py
│   │   └── token.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py
│   │           ├── orders.py
│   │           ├── portfolio.py
│   │           └── market_data.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── trading_service.py
│   │   └── market_data_service.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py
│   │   └── dependencies.py
│   └── integrations/
│       ├── __init__.py
│       ├── alpaca_client.py
│       └── ccxt_client.py
├── tests/
├── alembic/
├── requirements.txt
├── Dockerfile
└── .env
```

### 1. Backend Core Files

#### `app/config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Alpaca
    ALPACA_API_KEY: str
    ALPACA_SECRET_KEY: str
    ALPACA_BASE_URL: str
    
    # Binance (optional)
    BINANCE_API_KEY: str = ""
    BINANCE_SECRET_KEY: str = ""
    
    # Polygon (optional)
    POLYGON_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
```

#### `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### `app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.database import engine
from app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SpeedTrade API",
    description="High-speed trading API for stocks and crypto under $100",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "SpeedTrade API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 2. Models

#### `app/models/user.py`

```python
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    positions = relationship("Position", back_populates="user")
```

#### `app/models/order.py`

```python
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    symbol = Column(String(20), nullable=False, index=True)
    asset_type = Column(String(20), nullable=False)  # 'stock' or 'crypto'
    side = Column(String(10), nullable=False)  # 'buy' or 'sell'
    order_type = Column(String(20), nullable=False)  # 'market', 'limit', 'stop'
    qty = Column(Numeric(20, 8), nullable=False)
    filled_qty = Column(Numeric(20, 8), default=0)
    limit_price = Column(Numeric(20, 2))
    stop_price = Column(Numeric(20, 2))
    status = Column(String(20), nullable=False, index=True)  # 'pending', 'filled', 'cancelled'
    filled_avg_price = Column(Numeric(20, 2))
    external_order_id = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    filled_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="orders")
```

### 3. Schemas (Pydantic)

#### `app/schemas/user.py`

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_premium: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None
```

#### `app/schemas/order.py`

```python
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from typing import Optional

class OrderCreate(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    asset_type: str = Field(..., pattern="^(stock|crypto)$")
    side: str = Field(..., pattern="^(buy|sell)$")
    order_type: str = Field(..., pattern="^(market|limit|stop)$")
    qty: Decimal = Field(..., gt=0)
    limit_price: Optional[Decimal] = None
    stop_price: Optional[Decimal] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    symbol: str
    asset_type: str
    side: str
    order_type: str
    qty: Decimal
    filled_qty: Decimal
    limit_price: Optional[Decimal]
    status: str
    filled_avg_price: Optional[Decimal]
    created_at: datetime
    filled_at: Optional[datetime]
    
    class Config:
        from_attributes = True
```

### 4. Authentication Endpoint

#### `app/api/v1/endpoints/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.config import settings

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create user
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Find user by username
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
```

### 5. Trading Integration

#### `app/integrations/alpaca_client.py`

```python
from alpaca_trade_api import REST
from app.config import settings

class AlpacaClient:
    def __init__(self):
        self.client = REST(
            key_id=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
            base_url=settings.ALPACA_BASE_URL
        )
    
    def get_account(self):
        return self.client.get_account()
    
    def place_order(self, symbol: str, qty: float, side: str, order_type: str, limit_price: float = None):
        return self.client.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force='gtc',
            limit_price=limit_price
        )
    
    def get_order(self, order_id: str):
        return self.client.get_order(order_id)
    
    def cancel_order(self, order_id: str):
        return self.client.cancel_order(order_id)
    
    def get_positions(self):
        return self.client.list_positions()
    
    def get_quote(self, symbol: str):
        return self.client.get_latest_quote(symbol)

alpaca_client = AlpacaClient()
```

### 6. Orders Endpoint

#### `app/api/v1/endpoints/orders.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderResponse
from app.api.v1.endpoints.auth import get_current_user
from app.integrations.alpaca_client import alpaca_client

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=201)
async def place_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Place order with Alpaca
        alpaca_order = alpaca_client.place_order(
            symbol=order_data.symbol,
            qty=float(order_data.qty),
            side=order_data.side,
            order_type=order_data.order_type,
            limit_price=float(order_data.limit_price) if order_data.limit_price else None
        )
        
        # Create order record
        order = Order(
            user_id=current_user.id,
            symbol=order_data.symbol,
            asset_type=order_data.asset_type,
            side=order_data.side,
            order_type=order_data.order_type,
            qty=order_data.qty,
            limit_price=order_data.limit_price,
            status="pending",
            external_order_id=alpaca_order.id
        )
        
        db.add(order)
        db.commit()
        db.refresh(order)
        
        return order
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@router.delete("/{order_id}")
async def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Can only cancel pending orders")
    
    try:
        alpaca_client.cancel_order(order.external_order_id)
        order.status = "cancelled"
        db.commit()
        return {"message": "Order cancelled successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### 7. Requirements.txt

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
pydantic-settings==2.1.0
alpaca-trade-api==3.0.2
ccxt==4.1.64
yfinance==0.2.32
redis==5.0.1
python-socketio==5.10.0
```

---

## Frontend Implementation

### 1. Install Dependencies

```bash
cd frontend

# Core dependencies
npm install axios @reduxjs/toolkit react-redux react-router-dom

# UI libraries
npm install @mui/material @emotion/react @emotion/styled
npm install lightweight-charts

# Forms and validation
npm install react-hook-form zod @hookform/resolvers

# Real-time
npm install socket.io-client

# Utils
npm install date-fns numeral

# Dev dependencies
npm install -D @types/numeral
```

### 2. Frontend Structure

```typescript
// src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

```typescript
// src/services/authService.ts
import api from './api';

export const authService = {
  async login(username: string, password: string) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await api.post('/api/v1/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    
    localStorage.setItem('access_token', response.data.access_token);
    return response.data;
  },
  
  async register(email: string, username: string, password: string) {
    const response = await api.post('/api/v1/auth/register', {
      email,
      username,
      password,
    });
    return response.data;
  },
  
  logout() {
    localStorage.removeItem('access_token');
  },
  
  async getCurrentUser() {
    const response = await api.get('/api/v1/auth/me');
    return response.data;
  },
};
```

```typescript
// src/services/tradingService.ts
import api from './api';

export interface OrderData {
  symbol: string;
  asset_type: 'stock' | 'crypto';
  side: 'buy' | 'sell';
  order_type: 'market' | 'limit';
  qty: number;
  limit_price?: number;
}

export const tradingService = {
  async placeOrder(orderData: OrderData) {
    const response = await api.post('/api/v1/orders', orderData);
    return response.data;
  },
  
  async getOrders() {
    const response = await api.get('/api/v1/orders');
    return response.data;
  },
  
  async cancelOrder(orderId: number) {
    const response = await api.delete(`/api/v1/orders/${orderId}`);
    return response.data;
  },
};
```

### 3. React Components

```typescript
// src/components/trading/OrderForm.tsx
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Button, TextField, Select, MenuItem } from '@mui/material';
import { tradingService, OrderData } from '../../services/tradingService';

export const OrderForm: React.FC<{ symbol: string; currentPrice: number }> = ({
  symbol,
  currentPrice,
}) => {
  const { register, handleSubmit, watch } = useForm<OrderData>();
  const [loading, setLoading] = useState(false);
  
  const orderType = watch('order_type', 'market');
  
  const onSubmit = async (data: OrderData) => {
    setLoading(true);
    try {
      await tradingService.placeOrder({
        ...data,
        symbol,
        asset_type: 'stock',
      });
      alert('Order placed successfully!');
    } catch (error) {
      alert('Error placing order');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Select {...register('side')} defaultValue="buy">
        <MenuItem value="buy">Buy</MenuItem>
        <MenuItem value="sell">Sell</MenuItem>
      </Select>
      
      <Select {...register('order_type')} defaultValue="market">
        <MenuItem value="market">Market</MenuItem>
        <MenuItem value="limit">Limit</MenuItem>
      </Select>
      
      <TextField
        {...register('qty')}
        label="Quantity"
        type="number"
        required
      />
      
      {orderType === 'limit' && (
        <TextField
          {...register('limit_price')}
          label="Limit Price"
          type="number"
          defaultValue={currentPrice}
        />
      )}
      
      <Button type="submit" disabled={loading}>
        Place Order
      </Button>
    </form>
  );
};
```

---

## Testing Strategy

### Backend Tests

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123"
        }
    )
    assert response.status_code == 201
    assert "id" in response.json()

def test_login():
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Frontend Tests

```typescript
// src/components/__tests__/OrderForm.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { OrderForm } from '../trading/OrderForm';

describe('OrderForm', () => {
  it('renders order form', () => {
    render(<OrderForm symbol="AAPL" currentPrice={150} />);
    expect(screen.getByText('Place Order')).toBeInTheDocument();
  });
  
  it('shows limit price field for limit orders', () => {
    render(<OrderForm symbol="AAPL" currentPrice={150} />);
    fireEvent.change(screen.getByLabelText('Order Type'), {
      target: { value: 'limit' }
    });
    expect(screen.getByLabelText('Limit Price')).toBeInTheDocument();
  });
});
```

---

## Deployment Guide

### 1. Docker Build

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f backend
```

### 2. Database Migration

```bash
# Install Alembic
pip install alembic

# Initialize
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Run migration
alembic upgrade head
```

### 3. Production Deployment

```bash
# Build for production
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# SSL Certificate
certbot --nginx -d yourdomain.com
```

---

## Quick Start Commands

```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Run backend tests
cd backend && pytest

# Run frontend tests
cd frontend && npm test

# Access services
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

**Previous:** [MVP_ARCHITECTURE.md](MVP_ARCHITECTURE.md)  
**Next:** [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)
