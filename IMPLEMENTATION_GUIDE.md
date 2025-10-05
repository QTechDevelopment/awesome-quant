# SpeedTrade MVP - Implementation Guide
## Step-by-Step Development Roadmap

This guide provides practical, actionable steps to build your trading platform MVP using tools from the awesome-quant repository.

---

## 🎯 Phase 1: Project Setup (Week 1)

### Day 1: Environment Setup

#### 1. Install Required Tools
```bash
# Install Python 3.11+
python --version  # Should be 3.11+

# Install Node.js 18+
node --version  # For frontend

# Install Docker
docker --version

# Install PostgreSQL
# On Ubuntu/Debian:
sudo apt install postgresql postgresql-contrib

# Install Redis
sudo apt install redis-server
```

#### 2. Create Project Structure
```bash
mkdir speedtrade
cd speedtrade

# Backend structure
mkdir -p backend/{app,tests,alembic}
mkdir -p backend/app/{api,core,models,services,adapters}
mkdir -p backend/app/api/{v1,websocket}

# Frontend structure
mkdir -p frontend/{src,public}
mkdir -p frontend/src/{components,pages,services,hooks,store}

# Shared
mkdir -p infrastructure/{docker,k8s,scripts}
mkdir -p docs

# Create files
touch backend/requirements.txt
touch backend/Dockerfile
touch docker-compose.yml
touch README.md
```

#### 3. Initialize Git Repository
```bash
git init
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.env

# Node
node_modules/
npm-debug.log*
build/
dist/

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Secrets
*.pem
*.key
secrets/
EOF

git add .
git commit -m "Initial project structure"
```

### Day 2: Backend Foundation

#### 1. Create `backend/requirements.txt`
```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9

# Async & Caching
aioredis==2.0.1
redis==5.0.1
celery==5.3.4

# Trading Libraries (from awesome-quant)
alpaca-trade-api==3.0.2
ccxt==4.1.54
yfinance==0.2.32
pandas==2.1.3
numpy==1.26.2
ta-lib==0.4.28  # Technical Analysis

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
bcrypt==4.1.1

# Monitoring & Logging
loguru==0.7.2
sentry-sdk==1.38.0
prometheus-client==0.19.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
faker==20.1.0

# Utilities
python-dotenv==1.0.0
httpx==0.25.2
websockets==12.0
```

#### 2. Create `backend/.env.example`
```bash
# Application
APP_NAME=SpeedTrade
APP_ENV=development
DEBUG=True
SECRET_KEY=your-super-secret-key-change-in-production
API_V1_PREFIX=/api/v1

# Database
DATABASE_URL=postgresql://speedtrade:password@localhost:5432/speedtrade_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=0

# Redis
REDIS_URL=redis://localhost:6379/0

# Alpaca (Trading)
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
ALPACA_BASE_URL=https://paper-api.alpaca.markets  # Paper trading for testing

# Market Data
POLYGON_API_KEY=your_polygon_api_key
COINGECKO_API_KEY=optional_coingecko_api_key

# Security
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# KYC/Compliance
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_secret
PLAID_ENV=sandbox  # sandbox, development, production

# Email
SENDGRID_API_KEY=your_sendgrid_api_key
FROM_EMAIL=noreply@speedtrade.com

# Monitoring
SENTRY_DSN=your_sentry_dsn
```

#### 3. Create `docker-compose.yml`
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: speedtrade_postgres
    environment:
      POSTGRES_USER: speedtrade
      POSTGRES_PASSWORD: password
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
      timeout: 5s
      retries: 5

  timescaledb:
    image: timescale/timescaledb:latest-pg15
    container_name: speedtrade_timescale
    environment:
      POSTGRES_USER: speedtrade
      POSTGRES_PASSWORD: password
      POSTGRES_DB: market_data
    ports:
      - "5433:5432"
    volumes:
      - timescale_data:/var/lib/postgresql/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: speedtrade_backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://speedtrade:password@postgres:5432/speedtrade_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    env_file:
      - ./backend/.env

  nginx:
    image: nginx:alpine
    container_name: speedtrade_nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./infrastructure/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/build:/usr/share/nginx/html
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
  timescale_data:
```

### Day 3-4: Core Backend Development

#### 1. Create `backend/app/main.py`
```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import time

from app.core.config import settings
from app.api.v1 import router as api_v1_router
from app.api.websocket import router as websocket_router

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="High-speed trading platform for stocks and crypto under $100",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.method} {request.url.path} - {process_time:.3f}s")
    return response

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "detail": str(exc)},
    )

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.APP_ENV
    }

# Include routers
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)
app.include_router(websocket_router)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME}")
    # Initialize connections (database, redis, etc.)
    
@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")
    # Close connections

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

#### 2. Create `backend/app/core/config.py`
```python
from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "SpeedTrade"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0
    
    # Redis
    REDIS_URL: str
    
    # Alpaca
    ALPACA_API_KEY: str
    ALPACA_SECRET_KEY: str
    ALPACA_BASE_URL: str
    
    # Market Data
    POLYGON_API_KEY: Optional[str] = None
    COINGECKO_API_KEY: Optional[str] = None
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # KYC
    PLAID_CLIENT_ID: Optional[str] = None
    PLAID_SECRET: Optional[str] = None
    PLAID_ENV: str = "sandbox"
    
    # Email
    SENDGRID_API_KEY: Optional[str] = None
    FROM_EMAIL: str = "noreply@speedtrade.com"
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

#### 3. Create Database Models `backend/app/models/user.py`
```python
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base

class KYCStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class AccountType(str, enum.Enum):
    CASH = "cash"
    MARGIN = "margin"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    
    # KYC
    kyc_status = Column(Enum(KYCStatus), default=KYCStatus.PENDING)
    kyc_level = Column(Integer, default=0)
    
    # Account
    account_type = Column(Enum(AccountType), default=AccountType.CASH)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    two_factor_enabled = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<User {self.username}>"

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Balances
    total_value = Column(Numeric(20, 2), default=0)
    cash_balance = Column(Numeric(20, 2), default=0)
    buying_power = Column(Numeric(20, 2), default=0)
    equity = Column(Numeric(20, 2), default=0)
    
    # P&L
    daily_pnl = Column(Numeric(20, 2), default=0)
    total_pnl = Column(Numeric(20, 2), default=0)
    
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Portfolio {self.user_id}>"
```

#### 4. Create `backend/app/models/trading.py`
```python
from sqlalchemy import Column, String, DateTime, Enum, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base

class OrderSide(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(str, enum.Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    PARTIAL = "partial"
    CANCELLED = "cancelled"
    REJECTED = "rejected"

class TimeInForce(str, enum.Enum):
    DAY = "day"
    GTC = "gtc"  # Good till cancelled
    IOC = "ioc"  # Immediate or cancel
    FOK = "fok"  # Fill or kill

class AssetType(str, enum.Enum):
    STOCK = "stock"
    CRYPTO = "crypto"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Order details
    symbol = Column(String, nullable=False, index=True)
    asset_type = Column(Enum(AssetType), nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    type = Column(Enum(OrderType), nullable=False)
    
    # Quantities & Prices
    quantity = Column(Numeric(20, 8), nullable=False)
    filled_quantity = Column(Numeric(20, 8), default=0)
    price = Column(Numeric(20, 8), nullable=True)
    stop_price = Column(Numeric(20, 8), nullable=True)
    avg_fill_price = Column(Numeric(20, 8), nullable=True)
    
    # Status
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    time_in_force = Column(Enum(TimeInForce), default=TimeInForce.DAY)
    
    # External IDs
    broker_order_id = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    filled_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Order {self.symbol} {self.side} {self.quantity}>"

class Position(Base):
    __tablename__ = "positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    symbol = Column(String, nullable=False, index=True)
    asset_type = Column(Enum(AssetType), nullable=False)
    
    quantity = Column(Numeric(20, 8), nullable=False)
    avg_entry_price = Column(Numeric(20, 8), nullable=False)
    current_price = Column(Numeric(20, 8), default=0)
    
    unrealized_pnl = Column(Numeric(20, 2), default=0)
    realized_pnl = Column(Numeric(20, 2), default=0)
    
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Position {self.symbol} {self.quantity}>"
```

### Day 5: Trading Service Implementation

#### Create `backend/app/services/trading_service.py`
```python
from typing import Optional, Dict, Any
from decimal import Decimal
import alpaca_trade_api as tradeapi
from loguru import logger

from app.core.config import settings
from app.models.trading import Order, OrderSide, OrderType, OrderStatus

class TradingService:
    """Core trading service using Alpaca API"""
    
    def __init__(self):
        self.api = tradeapi.REST(
            key_id=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
            base_url=settings.ALPACA_BASE_URL
        )
    
    async def validate_order(
        self,
        symbol: str,
        quantity: Decimal,
        side: OrderSide,
        order_type: OrderType,
        price: Optional[Decimal] = None
    ) -> Dict[str, Any]:
        """Validate order before submission"""
        errors = []
        
        # Check if market is open
        clock = self.api.get_clock()
        if not clock.is_open:
            errors.append("Market is closed")
        
        # Check if asset exists and is tradable
        try:
            asset = self.api.get_asset(symbol)
            if not asset.tradable:
                errors.append(f"{symbol} is not tradable")
            if asset.status != 'active':
                errors.append(f"{symbol} is not active")
        except Exception as e:
            errors.append(f"Invalid symbol: {symbol}")
            logger.error(f"Asset validation error: {e}")
        
        # Check quantity
        if quantity <= 0:
            errors.append("Quantity must be positive")
        
        # Check price for limit orders
        if order_type == OrderType.LIMIT and price is None:
            errors.append("Limit orders require a price")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    async def place_order(
        self,
        user_id: str,
        symbol: str,
        quantity: Decimal,
        side: OrderSide,
        order_type: OrderType,
        price: Optional[Decimal] = None,
        stop_price: Optional[Decimal] = None,
        time_in_force: str = 'day'
    ) -> Dict[str, Any]:
        """Place an order with Alpaca"""
        
        # Validate first
        validation = await self.validate_order(
            symbol, quantity, side, order_type, price
        )
        if not validation["valid"]:
            return {
                "success": False,
                "errors": validation["errors"]
            }
        
        try:
            # Map our order type to Alpaca's
            alpaca_order_type = {
                OrderType.MARKET: 'market',
                OrderType.LIMIT: 'limit',
                OrderType.STOP: 'stop',
                OrderType.STOP_LIMIT: 'stop_limit'
            }[order_type]
            
            # Submit order to Alpaca
            alpaca_order = self.api.submit_order(
                symbol=symbol,
                qty=float(quantity),
                side=side.value,
                type=alpaca_order_type,
                time_in_force=time_in_force,
                limit_price=float(price) if price else None,
                stop_price=float(stop_price) if stop_price else None
            )
            
            logger.info(f"Order placed: {alpaca_order.id} for {symbol}")
            
            return {
                "success": True,
                "order_id": alpaca_order.id,
                "status": alpaca_order.status,
                "submitted_at": alpaca_order.submitted_at
            }
            
        except Exception as e:
            logger.error(f"Order placement failed: {e}")
            return {
                "success": False,
                "errors": [str(e)]
            }
    
    async def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an order"""
        try:
            self.api.cancel_order(order_id)
            logger.info(f"Order cancelled: {order_id}")
            return {"success": True}
        except Exception as e:
            logger.error(f"Order cancellation failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_order_status(self, order_id: str) -> Dict[str, Any]:
        """Get order status from broker"""
        try:
            order = self.api.get_order(order_id)
            return {
                "order_id": order.id,
                "status": order.status,
                "filled_qty": order.filled_qty,
                "filled_avg_price": order.filled_avg_price
            }
        except Exception as e:
            logger.error(f"Failed to get order status: {e}")
            return None
    
    async def get_account_info(self) -> Dict[str, Any]:
        """Get account information"""
        try:
            account = self.api.get_account()
            return {
                "cash": float(account.cash),
                "portfolio_value": float(account.portfolio_value),
                "buying_power": float(account.buying_power),
                "equity": float(account.equity)
            }
        except Exception as e:
            logger.error(f"Failed to get account info: {e}")
            return None

# Singleton instance
trading_service = TradingService()
```

---

## 🚀 Quick Start Commands

### Start Development Environment
```bash
# Clone and setup
git clone <your-repo>
cd speedtrade

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Start services with Docker
cd ..
docker-compose up -d postgres redis timescaledb

# Run migrations
cd backend
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload

# Visit: http://localhost:8000/api/docs
```

### Test Trading API
```bash
# Get Alpaca paper trading keys from:
# https://app.alpaca.markets/paper/dashboard/overview

# Test order placement
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "symbol": "AAPL",
    "quantity": 1,
    "side": "buy",
    "type": "market"
  }'
```

---

## 📚 Next Documents to Create

1. **API_DOCUMENTATION.md** - All API endpoints
2. **DEPLOYMENT_GUIDE.md** - Production deployment
3. **TESTING_STRATEGY.md** - Unit, integration tests
4. **SECURITY_CHECKLIST.md** - Security best practices
5. **FRONTEND_GUIDE.md** - React app development

This implementation guide provides the foundation to start building immediately!
