# 🏗️ SpeedTrade - MVP Technical Architecture

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Frontend Architecture](#frontend-architecture)
4. [Backend Architecture](#backend-architecture)
5. [Database Design](#database-design)
6. [API Design](#api-design)
7. [Real-Time Communication](#real-time-communication)
8. [Security Architecture](#security-architecture)
9. [Scalability & Performance](#scalability--performance)
10. [Deployment Architecture](#deployment-architecture)

---

## System Overview

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                               │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐     │
│  │  Web Browser   │  │  Mobile App    │  │  Desktop App   │     │
│  │  (React)       │  │  (React Native)│  │  (Electron)    │     │
│  └────────┬───────┘  └────────┬───────┘  └────────┬───────┘     │
└───────────┼─────────────────────┼─────────────────────┼──────────┘
            │                     │                     │
            └──────────────┬──────┴─────────────────────┘
                           │ HTTPS/WSS
┌──────────────────────────▼───────────────────────────────────────┐
│                      API GATEWAY                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Nginx     │  │ Rate Limiter│  │     SSL     │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└──────────────────────────┬───────────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────────┐
│                   APPLICATION LAYER                               │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │              FastAPI Backend (Python)                     │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│    │
│  │  │   Auth   │  │  Trading │  │ Portfolio│  │Real-Time ││    │
│  │  │  Service │  │  Service │  │  Service │  │  Service ││    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘│    │
│  └──────────────────────────────────────────────────────────┘    │
└──────────┬────────────────────────┬──────────────────────────────┘
           │                        │
     ┌─────▼──────┐           ┌─────▼──────────────────┐
     │            │           │                        │
┌────▼────────┐  │      ┌────▼──────────┐  ┌─────────▼────────┐
│ PostgreSQL  │  │      │ Alpaca API    │  │ CCXT (Crypto)    │
│  Database   │  │      │ (Stock Trade) │  │ (Crypto Trade)   │
└─────────────┘  │      └───────────────┘  └──────────────────┘
                 │
           ┌─────▼──────┐         ┌───────────────┐
           │   Redis    │         │  Polygon.io   │
           │   Cache    │         │  (Market Data)│
           └────────────┘         └───────────────┘
```

---

## Architecture Diagram

### Component Interaction Flow

```
User Action: Place Order
│
├─> Frontend (React)
│   ├─> Validate input
│   ├─> Display loading state
│   └─> Send POST /api/v1/orders
│
├─> API Gateway (Nginx)
│   ├─> SSL termination
│   ├─> Rate limiting (100 req/min)
│   └─> Route to Backend
│
├─> Backend (FastAPI)
│   ├─> Authenticate JWT
│   ├─> Validate order params
│   ├─> Check buying power
│   ├─> Risk management
│   └─> Execute order
│       │
│       ├─> Stock? → Alpaca API
│       └─> Crypto? → CCXT (Binance/Coinbase)
│
├─> Database (PostgreSQL)
│   ├─> Insert order record
│   ├─> Update portfolio
│   └─> Log transaction
│
├─> Cache (Redis)
│   ├─> Invalidate portfolio cache
│   └─> Update real-time position
│
└─> WebSocket
    └─> Broadcast order update to client
```

---

## Frontend Architecture

### Technology Stack

```typescript
// Core
React 18.2+ (UI framework)
TypeScript 5.0+ (Type safety)
Vite 4.0+ (Build tool)

// State Management
Redux Toolkit (Global state)
React Query (Server state)
Zustand (Light local state)

// UI Components
Material-UI v5 / Tailwind CSS
TradingView Lightweight Charts
Recharts (simple charts)

// Real-Time
Socket.io-client (WebSocket)
SWR (Data fetching)

// Forms & Validation
React Hook Form
Zod (Schema validation)

// Routing
React Router v6

// Utils
Axios (HTTP client)
date-fns (Date manipulation)
numeral (Number formatting)
```

### Folder Structure

```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── common/           # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── Loader.tsx
│   │   ├── trading/          # Trading-specific components
│   │   │   ├── OrderForm.tsx
│   │   │   ├── OrderBook.tsx
│   │   │   ├── PriceChart.tsx
│   │   │   └── TickerList.tsx
│   │   └── portfolio/        # Portfolio components
│   │       ├── PositionCard.tsx
│   │       ├── PerformanceChart.tsx
│   │       └── AssetAllocation.tsx
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Trade.tsx
│   │   └── Portfolio.tsx
│   ├── store/
│   │   ├── index.ts          # Redux store
│   │   ├── slices/
│   │   │   ├── authSlice.ts
│   │   │   ├── portfolioSlice.ts
│   │   │   └── tradingSlice.ts
│   ├── services/
│   │   ├── api.ts            # Axios instance
│   │   ├── authService.ts
│   │   ├── tradingService.ts
│   │   └── websocket.ts      # WebSocket client
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useWebSocket.ts
│   │   └── useRealTimePrice.ts
│   ├── utils/
│   │   ├── formatters.ts     # Price, date formatting
│   │   ├── validators.ts
│   │   └── constants.ts
│   ├── types/
│   │   ├── user.ts
│   │   ├── order.ts
│   │   └── portfolio.ts
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
└── vite.config.ts
```

### Key Frontend Features

#### 1. Real-Time Price Updates
```typescript
// hooks/useRealTimePrice.ts
import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

export const useRealTimePrice = (symbol: string) => {
  const [price, setPrice] = useState<number | null>(null);
  
  useEffect(() => {
    const socket = io(process.env.VITE_WS_URL);
    
    socket.emit('subscribe', symbol);
    socket.on('price_update', (data) => {
      if (data.symbol === symbol) {
        setPrice(data.price);
      }
    });
    
    return () => {
      socket.emit('unsubscribe', symbol);
      socket.disconnect();
    };
  }, [symbol]);
  
  return price;
};
```

#### 2. Order Form Component
```typescript
// components/trading/OrderForm.tsx
interface OrderFormProps {
  symbol: string;
  currentPrice: number;
}

export const OrderForm: React.FC<OrderFormProps> = ({ symbol, currentPrice }) => {
  const [orderType, setOrderType] = useState<'market' | 'limit'>('market');
  const [side, setSide] = useState<'buy' | 'sell'>('buy');
  const [quantity, setQuantity] = useState<number>(1);
  const [limitPrice, setLimitPrice] = useState<number>(currentPrice);
  
  const handleSubmit = async () => {
    const order = {
      symbol,
      side,
      type: orderType,
      qty: quantity,
      ...(orderType === 'limit' && { limit_price: limitPrice })
    };
    
    await api.post('/api/v1/orders', order);
  };
  
  return (
    // Form JSX...
  );
};
```

---

## Backend Architecture

### Technology Stack

```python
# Core
FastAPI 0.104+ (Web framework)
Python 3.10+ (Language)
Pydantic v2 (Data validation)
SQLAlchemy 2.0+ (ORM)

# Database
PostgreSQL 15+ (Primary DB)
Redis 7+ (Cache & real-time)

# Trading
alpaca-trade-api (Stock trading)
ccxt (Crypto trading)
yfinance (Market data)
polygon (Real-time data)

# Auth & Security
python-jose (JWT)
passlib (Password hashing)
python-multipart (File uploads)

# Real-Time
python-socketio (WebSocket)
aioredis (Async Redis)

# Background Tasks
celery (Task queue)
redis (Broker)

# Testing
pytest (Unit tests)
httpx (Async HTTP client)
```

### Folder Structure

```
backend/
├── app/
│   ├── main.py               # FastAPI app entry
│   ├── config.py             # Configuration
│   ├── database.py           # DB connection
│   ├── models/               # SQLAlchemy models
│   │   ├── user.py
│   │   ├── order.py
│   │   ├── portfolio.py
│   │   └── position.py
│   ├── schemas/              # Pydantic schemas
│   │   ├── user.py
│   │   ├── order.py
│   │   └── portfolio.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── orders.py
│   │   │   │   ├── portfolio.py
│   │   │   │   └── market_data.py
│   │   │   └── router.py
│   ├── services/             # Business logic
│   │   ├── auth_service.py
│   │   ├── trading_service.py
│   │   ├── portfolio_service.py
│   │   └── market_data_service.py
│   ├── core/
│   │   ├── security.py       # JWT, hashing
│   │   ├── dependencies.py   # FastAPI dependencies
│   │   └── exceptions.py     # Custom exceptions
│   ├── integrations/
│   │   ├── alpaca.py         # Alpaca API wrapper
│   │   ├── ccxt_client.py    # CCXT wrapper
│   │   └── polygon.py        # Polygon API wrapper
│   ├── websocket/
│   │   ├── manager.py        # WebSocket connection manager
│   │   └── handlers.py       # WS event handlers
│   └── tests/
│       ├── test_auth.py
│       ├── test_orders.py
│       └── test_portfolio.py
├── alembic/                  # Database migrations
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

### Core Backend Services

#### 1. Authentication Service
```python
# app/services/auth_service.py
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = "HS256"
        self.access_token_expire = 30  # minutes
    
    def create_access_token(self, user_id: int) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire)
        payload = {
            "sub": str(user_id),
            "exp": expire
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
```

#### 2. Trading Service
```python
# app/services/trading_service.py
from alpaca_trade_api import REST as AlpacaClient
import ccxt

class TradingService:
    def __init__(self):
        self.alpaca = AlpacaClient(
            key_id=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
            base_url=settings.ALPACA_BASE_URL
        )
        self.binance = ccxt.binance({
            'apiKey': settings.BINANCE_API_KEY,
            'secret': settings.BINANCE_SECRET_KEY
        })
    
    async def place_order(
        self,
        user_id: int,
        symbol: str,
        side: str,
        order_type: str,
        qty: float,
        limit_price: float = None
    ):
        # Determine if stock or crypto
        if self._is_crypto(symbol):
            return await self._place_crypto_order(symbol, side, order_type, qty, limit_price)
        else:
            return await self._place_stock_order(symbol, side, order_type, qty, limit_price)
    
    async def _place_stock_order(self, symbol, side, order_type, qty, limit_price):
        order = self.alpaca.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force='gtc',
            limit_price=limit_price
        )
        return order
    
    async def _place_crypto_order(self, symbol, side, order_type, qty, limit_price):
        # CCXT uses different format: BTC/USDT
        market_symbol = self._convert_to_ccxt_symbol(symbol)
        
        if order_type == 'market':
            if side == 'buy':
                order = self.binance.create_market_buy_order(market_symbol, qty)
            else:
                order = self.binance.create_market_sell_order(market_symbol, qty)
        else:
            if side == 'buy':
                order = self.binance.create_limit_buy_order(market_symbol, qty, limit_price)
            else:
                order = self.binance.create_limit_sell_order(market_symbol, qty, limit_price)
        
        return order
```

#### 3. Market Data Service
```python
# app/services/market_data_service.py
import yfinance as yf
from polygon import RESTClient
import ccxt

class MarketDataService:
    def __init__(self):
        self.polygon = RESTClient(settings.POLYGON_API_KEY)
        self.binance = ccxt.binance()
    
    async def get_quote(self, symbol: str):
        if self._is_crypto(symbol):
            return await self._get_crypto_quote(symbol)
        else:
            return await self._get_stock_quote(symbol)
    
    async def get_under_100(self, asset_type: str = 'all'):
        """Get all stocks/crypto under $100"""
        if asset_type in ['all', 'stocks']:
            stocks = await self._get_stocks_under_100()
        
        if asset_type in ['all', 'crypto']:
            crypto = await self._get_crypto_under_100()
        
        return {
            'stocks': stocks if asset_type in ['all', 'stocks'] else [],
            'crypto': crypto if asset_type in ['all', 'crypto'] else []
        }
    
    async def _get_stocks_under_100(self):
        # Use Polygon or yfinance to filter stocks
        # This is a simplified example
        tickers = yf.Tickers('^GSPC')  # Get S&P 500
        under_100 = []
        
        for ticker in tickers.tickers:
            price = ticker.info.get('regularMarketPrice', 0)
            if 0 < price < 100:
                under_100.append({
                    'symbol': ticker.ticker,
                    'price': price,
                    'name': ticker.info.get('shortName')
                })
        
        return under_100
```

---

## Database Design

### PostgreSQL Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_premium BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Accounts table (brokerage accounts)
CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    account_type VARCHAR(50) NOT NULL,  -- 'alpaca', 'binance', etc.
    account_number VARCHAR(255),
    api_key_encrypted VARCHAR(500),
    api_secret_encrypted VARCHAR(500),
    is_paper BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    account_id INTEGER REFERENCES accounts(id),
    symbol VARCHAR(20) NOT NULL,
    asset_type VARCHAR(20) NOT NULL,  -- 'stock', 'crypto'
    side VARCHAR(10) NOT NULL,        -- 'buy', 'sell'
    order_type VARCHAR(20) NOT NULL,  -- 'market', 'limit', 'stop'
    qty DECIMAL(20, 8) NOT NULL,
    filled_qty DECIMAL(20, 8) DEFAULT 0,
    limit_price DECIMAL(20, 2),
    stop_price DECIMAL(20, 2),
    status VARCHAR(20) NOT NULL,      -- 'pending', 'filled', 'cancelled'
    filled_avg_price DECIMAL(20, 2),
    external_order_id VARCHAR(255),   -- Alpaca/CCXT order ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    filled_at TIMESTAMP
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_symbol ON orders(symbol);
CREATE INDEX idx_orders_status ON orders(status);

-- Positions table (current holdings)
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    account_id INTEGER REFERENCES accounts(id),
    symbol VARCHAR(20) NOT NULL,
    asset_type VARCHAR(20) NOT NULL,
    qty DECIMAL(20, 8) NOT NULL,
    avg_entry_price DECIMAL(20, 2) NOT NULL,
    current_price DECIMAL(20, 2),
    market_value DECIMAL(20, 2),
    unrealized_pl DECIMAL(20, 2),
    unrealized_plpc DECIMAL(10, 4),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, account_id, symbol)
);

CREATE INDEX idx_positions_user_id ON positions(user_id);

-- Portfolio history (daily snapshots)
CREATE TABLE portfolio_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    account_id INTEGER REFERENCES accounts(id),
    date DATE NOT NULL,
    equity DECIMAL(20, 2) NOT NULL,
    cash DECIMAL(20, 2) NOT NULL,
    profit_loss DECIMAL(20, 2),
    profit_loss_pct DECIMAL(10, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, account_id, date)
);

CREATE INDEX idx_portfolio_history_user_date ON portfolio_history(user_id, date);

-- Watchlist table
CREATE TABLE watchlists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Watchlist items
CREATE TABLE watchlist_items (
    id SERIAL PRIMARY KEY,
    watchlist_id INTEGER REFERENCES watchlists(id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL,
    asset_type VARCHAR(20) NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(watchlist_id, symbol)
);

-- Price alerts
CREATE TABLE price_alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    symbol VARCHAR(20) NOT NULL,
    condition VARCHAR(10) NOT NULL,  -- 'above', 'below'
    target_price DECIMAL(20, 2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    triggered_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Redis Cache Schema

```
# User session
user:session:{user_id} → {access_token, refresh_token, expires_at}

# Portfolio cache (5 min TTL)
portfolio:{user_id} → {JSON of positions, equity, cash}

# Real-time prices (10 sec TTL)
price:{symbol} → {price, timestamp}

# Rate limiting
rate_limit:{user_id}:{endpoint} → request count (1 min TTL)

# WebSocket connections
ws:connections → Set of user_ids
ws:subscriptions:{symbol} → Set of user_ids
```

---

## API Design

### REST API Endpoints

#### Authentication
```
POST   /api/v1/auth/register          # Register new user
POST   /api/v1/auth/login             # Login (get JWT)
POST   /api/v1/auth/refresh           # Refresh token
POST   /api/v1/auth/logout            # Logout
GET    /api/v1/auth/me                # Get current user
```

#### Trading
```
POST   /api/v1/orders                 # Place order
GET    /api/v1/orders                 # List orders
GET    /api/v1/orders/{order_id}      # Get order details
DELETE /api/v1/orders/{order_id}      # Cancel order
```

#### Portfolio
```
GET    /api/v1/portfolio              # Get portfolio summary
GET    /api/v1/positions              # List positions
GET    /api/v1/positions/{symbol}     # Get position details
GET    /api/v1/portfolio/history      # Portfolio performance history
```

#### Market Data
```
GET    /api/v1/market/quote/{symbol}  # Get quote
GET    /api/v1/market/under-100       # Get assets under $100
GET    /api/v1/market/search          # Search symbols
GET    /api/v1/market/chart/{symbol}  # Historical chart data
```

#### Watchlist
```
GET    /api/v1/watchlists             # List watchlists
POST   /api/v1/watchlists             # Create watchlist
POST   /api/v1/watchlists/{id}/items  # Add to watchlist
DELETE /api/v1/watchlists/{id}/items/{symbol}  # Remove from watchlist
```

### WebSocket Events

#### Client → Server
```javascript
// Subscribe to price updates
socket.emit('subscribe', { symbols: ['AAPL', 'BTC/USD'] });

// Unsubscribe
socket.emit('unsubscribe', { symbols: ['AAPL'] });

// Subscribe to order updates
socket.emit('subscribe_orders');
```

#### Server → Client
```javascript
// Price update
socket.on('price_update', {
  symbol: 'AAPL',
  price: 178.52,
  change: 1.23,
  change_pct: 0.69,
  timestamp: 1234567890
});

// Order update
socket.on('order_update', {
  order_id: '123',
  status: 'filled',
  filled_qty: 10,
  filled_avg_price: 178.50
});

// Position update
socket.on('position_update', {
  symbol: 'AAPL',
  qty: 10,
  unrealized_pl: 123.45
});
```

---

## Real-Time Communication

### WebSocket Architecture

```python
# app/websocket/manager.py
from fastapi import WebSocket
import asyncio
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
        self.subscriptions: dict[str, set[int]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Remove from all subscriptions
        for symbol in self.subscriptions:
            self.subscriptions[symbol].discard(user_id)
    
    def subscribe(self, user_id: int, symbol: str):
        if symbol not in self.subscriptions:
            self.subscriptions[symbol] = set()
        self.subscriptions[symbol].add(user_id)
    
    def unsubscribe(self, user_id: int, symbol: str):
        if symbol in self.subscriptions:
            self.subscriptions[symbol].discard(user_id)
    
    async def broadcast_price_update(self, symbol: str, data: dict):
        if symbol not in self.subscriptions:
            return
        
        for user_id in self.subscriptions[symbol]:
            if user_id in self.active_connections:
                websocket = self.active_connections[user_id]
                try:
                    await websocket.send_json({
                        'event': 'price_update',
                        'data': data
                    })
                except:
                    await self.disconnect(user_id)

manager = ConnectionManager()
```

---

## Security Architecture

### Authentication Flow

```
1. User Registration/Login
   ├─> Client sends credentials
   ├─> Server validates
   ├─> Server hashes password (bcrypt)
   ├─> Server generates JWT
   └─> Client stores JWT (httpOnly cookie or localStorage)

2. Authenticated Request
   ├─> Client sends JWT in Authorization header
   ├─> Server validates JWT signature
   ├─> Server checks expiration
   ├─> Server extracts user_id
   └─> Request proceeds with user context

3. Token Refresh
   ├─> Access token expires (30 min)
   ├─> Client uses refresh token
   ├─> Server issues new access token
   └─> Client updates stored token
```

### Security Measures

1. **Password Security**
   - Bcrypt hashing (cost factor 12)
   - Minimum 8 characters
   - Required: uppercase, lowercase, number, special char

2. **API Security**
   - JWT with HS256 signing
   - 30-minute access token expiry
   - 7-day refresh token expiry
   - Rate limiting (100 req/min per user)
   - CORS configuration

3. **Database Security**
   - SQL injection prevention (SQLAlchemy ORM)
   - Parameterized queries
   - API keys encrypted at rest (AES-256)
   - No plain text secrets

4. **Transport Security**
   - HTTPS only (TLS 1.3)
   - WSS for WebSocket
   - HSTS headers
   - Certificate pinning (mobile apps)

5. **Data Security**
   - PII encryption
   - Audit logging
   - Regular backups
   - GDPR compliance

---

## Scalability & Performance

### Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Order Execution | < 100ms | P95 latency |
| API Response | < 200ms | P95 latency |
| Page Load | < 2s | Lighthouse score |
| WebSocket Latency | < 50ms | Round-trip time |
| Database Query | < 50ms | P95 latency |

### Scaling Strategy

#### Horizontal Scaling (MVP → 10K users)
```
┌─────────────┐
│ Load Balancer│
│   (Nginx)    │
└──────┬───────┘
       │
   ┌───┴───┬───────┬───────┐
   │       │       │       │
┌──▼───┐ ┌─▼────┐ ┌─▼────┐ ┌─▼────┐
│App 1 │ │App 2 │ │App 3 │ │App N │
└──────┘ └──────┘ └──────┘ └──────┘
       │       │
   ┌───▼───────▼───┐
   │  PostgreSQL   │
   │  (Primary)    │
   └───────┬───────┘
           │
   ┌───────▼───────┐
   │  PostgreSQL   │
   │   (Replica)   │
   └───────────────┘
```

#### Caching Strategy
1. **Redis L1 Cache**
   - User sessions (30 min TTL)
   - Portfolio data (5 min TTL)
   - Real-time prices (10 sec TTL)

2. **CDN (Cloudflare)**
   - Static assets (HTML, CSS, JS)
   - Market data (1 min TTL)

3. **Database Query Cache**
   - SQLAlchemy query cache
   - Materialized views for complex queries

#### Database Optimization
1. **Indexing Strategy**
   - B-tree indexes on foreign keys
   - Composite indexes on (user_id, created_at)
   - Partial indexes on active records

2. **Partitioning**
   - Orders table partitioned by month
   - Portfolio history partitioned by year

3. **Connection Pooling**
   - Max 100 connections
   - Min 10 idle connections
   - 30s connection timeout

---

## Deployment Architecture

### Development Environment
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/speedtrade
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:8000
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=speedtrade
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Production Architecture (AWS/DigitalOcean)
```
┌─────────────────────────────────────────────┐
│          Cloudflare CDN (Global)            │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         AWS/DigitalOcean Region             │
│  ┌──────────────────────────────────────┐   │
│  │  Load Balancer (ALB/HAProxy)         │   │
│  └────────┬────────────┬─────────────────┘   │
│           │            │                     │
│  ┌────────▼───────┐  ┌─▼─────────────────┐  │
│  │  App Server 1  │  │  App Server 2     │  │
│  │  (FastAPI)     │  │  (FastAPI)        │  │
│  └────────┬───────┘  └─┬─────────────────┘  │
│           │            │                     │
│  ┌────────▼────────────▼─────────────────┐  │
│  │  PostgreSQL (RDS/Managed)             │  │
│  │  Primary + Read Replica               │  │
│  └───────────────────────────────────────┘  │
│           │                                  │
│  ┌────────▼────────────────────────────┐   │
│  │  Redis (ElastiCache/Managed)        │   │
│  └─────────────────────────────────────┘   │
│           │                                  │
│  ┌────────▼────────────────────────────┐   │
│  │  S3 (Backups & Logs)                │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### Monitoring Stack
```
- Prometheus (Metrics collection)
- Grafana (Visualization)
- Loki (Log aggregation)
- Jaeger (Distributed tracing)
- Sentry (Error tracking)
```

---

## Technology Alternatives

If you want to change technologies:

| Component | Primary Choice | Alternative |
|-----------|---------------|-------------|
| Frontend | React | Vue.js, Svelte, Angular |
| Backend | FastAPI (Python) | Node.js (Express), Go (Gin), C# (ASP.NET) |
| Database | PostgreSQL | MySQL, MongoDB, CockroachDB |
| Cache | Redis | Memcached, DragonflyDB |
| Stock API | Alpaca | Interactive Brokers, TD Ameritrade |
| Crypto API | CCXT | Direct exchange APIs |
| Charts | TradingView | Chart.js, D3.js, Highcharts |
| Deployment | Docker | VMs, Serverless (Lambda) |

---

## Next Steps

1. ✅ **Understand architecture** (this document)
2. ✅ **Start coding** → See IMPLEMENTATION_GUIDE.md
3. ✅ **Follow roadmap** → See PROJECT_ROADMAP.md
4. ✅ **Set up project structure** → See PROJECT_STRUCTURE.md

---

**Previous:** [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)  
**Next:** [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
