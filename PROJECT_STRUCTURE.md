# 📁 SpeedTrade - Complete Project Structure

## Overview

This document provides the complete file and folder organization for the SpeedTrade project.

**Use this as a reference when:**
- Setting up your project
- Understanding code organization
- Finding specific files
- Onboarding new team members

---

## Root Directory Structure

```
speedtrade/
├── backend/                 # Python FastAPI backend
├── frontend/                # React TypeScript frontend
├── docker/                  # Docker configurations
├── docs/                    # Additional documentation
├── scripts/                 # Utility scripts
├── .github/                 # GitHub Actions CI/CD
├── docker-compose.yml       # Docker orchestration
├── docker-compose.prod.yml  # Production Docker config
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore patterns
├── README.md               # Project overview
└── LICENSE                 # License file
```

---

## Backend Structure (Python/FastAPI)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI application entry point
│   ├── config.py                   # Configuration & settings
│   ├── database.py                 # Database connection & session
│   │
│   ├── models/                     # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── user.py                 # User model
│   │   ├── account.py              # Brokerage account model
│   │   ├── order.py                # Order model
│   │   ├── position.py             # Position model
│   │   ├── portfolio_history.py   # Portfolio history model
│   │   ├── watchlist.py            # Watchlist model
│   │   ├── price_alert.py          # Price alert model
│   │   └── base.py                 # Base model with common fields
│   │
│   ├── schemas/                    # Pydantic schemas (request/response)
│   │   ├── __init__.py
│   │   ├── user.py                 # User schemas
│   │   ├── token.py                # Auth token schemas
│   │   ├── order.py                # Order schemas
│   │   ├── position.py             # Position schemas
│   │   ├── portfolio.py            # Portfolio schemas
│   │   ├── watchlist.py            # Watchlist schemas
│   │   ├── alert.py                # Alert schemas
│   │   └── market_data.py          # Market data schemas
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/                     # API version 1
│   │       ├── __init__.py
│   │       ├── router.py           # Main API router
│   │       └── endpoints/          # API endpoint modules
│   │           ├── __init__.py
│   │           ├── auth.py         # Authentication endpoints
│   │           ├── users.py        # User management
│   │           ├── accounts.py     # Account management
│   │           ├── orders.py       # Order operations
│   │           ├── portfolio.py    # Portfolio endpoints
│   │           ├── positions.py    # Position endpoints
│   │           ├── market_data.py  # Market data endpoints
│   │           ├── watchlists.py   # Watchlist endpoints
│   │           └── alerts.py       # Price alert endpoints
│   │
│   ├── services/                   # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py         # Authentication logic
│   │   ├── user_service.py         # User management logic
│   │   ├── trading_service.py      # Trading operations
│   │   ├── portfolio_service.py    # Portfolio calculations
│   │   ├── market_data_service.py  # Market data fetching
│   │   ├── watchlist_service.py    # Watchlist logic
│   │   ├── alert_service.py        # Price alert logic
│   │   └── notification_service.py # Notifications
│   │
│   ├── core/                       # Core utilities
│   │   ├── __init__.py
│   │   ├── security.py             # JWT, password hashing
│   │   ├── dependencies.py         # FastAPI dependencies
│   │   ├── exceptions.py           # Custom exceptions
│   │   ├── middleware.py           # Custom middleware
│   │   └── config.py               # Core configuration
│   │
│   ├── integrations/               # External API integrations
│   │   ├── __init__.py
│   │   ├── alpaca/                 # Alpaca integration
│   │   │   ├── __init__.py
│   │   │   ├── client.py           # Alpaca API client
│   │   │   ├── models.py           # Alpaca data models
│   │   │   └── utils.py            # Alpaca utilities
│   │   ├── ccxt/                   # CCXT crypto integration
│   │   │   ├── __init__.py
│   │   │   ├── client.py           # CCXT wrapper
│   │   │   ├── exchanges.py        # Exchange configurations
│   │   │   └── utils.py            # CCXT utilities
│   │   ├── polygon/                # Polygon.io integration
│   │   │   ├── __init__.py
│   │   │   ├── client.py           # Polygon API client
│   │   │   └── utils.py            # Polygon utilities
│   │   └── yfinance/               # Yahoo Finance integration
│   │       ├── __init__.py
│   │       └── client.py           # yfinance wrapper
│   │
│   ├── websocket/                  # WebSocket functionality
│   │   ├── __init__.py
│   │   ├── manager.py              # WebSocket connection manager
│   │   ├── handlers.py             # WebSocket event handlers
│   │   ├── events.py               # Event definitions
│   │   └── streams.py              # Data streaming logic
│   │
│   ├── workers/                    # Background tasks
│   │   ├── __init__.py
│   │   ├── celery_app.py           # Celery application
│   │   ├── tasks.py                # Celery tasks
│   │   ├── order_monitor.py        # Monitor order status
│   │   ├── price_monitor.py        # Monitor price alerts
│   │   └── portfolio_snapshot.py   # Daily portfolio snapshots
│   │
│   └── utils/                      # Utility functions
│       ├── __init__.py
│       ├── logger.py               # Logging configuration
│       ├── validators.py           # Custom validators
│       ├── formatters.py           # Data formatters
│       ├── cache.py                # Redis cache utilities
│       └── helpers.py              # Helper functions
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── conftest.py                 # Pytest configuration
│   ├── test_auth.py                # Auth tests
│   ├── test_orders.py              # Order tests
│   ├── test_portfolio.py           # Portfolio tests
│   ├── test_market_data.py         # Market data tests
│   ├── test_integrations.py        # Integration tests
│   └── fixtures/                   # Test fixtures
│       ├── __init__.py
│       ├── users.py
│       ├── orders.py
│       └── market_data.py
│
├── alembic/                        # Database migrations
│   ├── versions/                   # Migration files
│   ├── env.py                      # Alembic environment
│   └── script.py.mako              # Migration template
│
├── requirements.txt                # Python dependencies
├── requirements-dev.txt            # Development dependencies
├── Dockerfile                      # Docker image definition
├── .dockerignore                   # Docker ignore patterns
├── pytest.ini                      # Pytest configuration
├── alembic.ini                     # Alembic configuration
├── .env.example                    # Environment variables template
└── README.md                       # Backend documentation
```

---

## Frontend Structure (React/TypeScript)

```
frontend/
├── public/                         # Static assets
│   ├── index.html
│   ├── favicon.ico
│   ├── logo.svg
│   ├── robots.txt
│   └── manifest.json
│
├── src/
│   ├── main.tsx                    # Application entry point
│   ├── App.tsx                     # Root component
│   ├── App.css                     # Global styles
│   ├── index.css                   # Base styles
│   │
│   ├── assets/                     # Images, fonts, etc.
│   │   ├── images/
│   │   │   ├── logo.svg
│   │   │   ├── hero-bg.jpg
│   │   │   └── icons/
│   │   ├── fonts/
│   │   └── animations/
│   │
│   ├── components/                 # Reusable components
│   │   ├── common/                 # Common UI components
│   │   │   ├── Button/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Button.test.tsx
│   │   │   │   └── Button.module.css
│   │   │   ├── Input/
│   │   │   │   ├── Input.tsx
│   │   │   │   └── Input.module.css
│   │   │   ├── Modal/
│   │   │   │   ├── Modal.tsx
│   │   │   │   └── Modal.module.css
│   │   │   ├── Loader/
│   │   │   │   ├── Loader.tsx
│   │   │   │   └── Loader.module.css
│   │   │   ├── Card/
│   │   │   ├── Badge/
│   │   │   ├── Tooltip/
│   │   │   └── Toast/
│   │   │
│   │   ├── layout/                 # Layout components
│   │   │   ├── Header/
│   │   │   │   ├── Header.tsx
│   │   │   │   └── Header.module.css
│   │   │   ├── Sidebar/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Sidebar.module.css
│   │   │   ├── Footer/
│   │   │   ├── Navigation/
│   │   │   └── Layout.tsx
│   │   │
│   │   ├── auth/                   # Authentication components
│   │   │   ├── LoginForm/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── LoginForm.module.css
│   │   │   ├── RegisterForm/
│   │   │   ├── ProtectedRoute/
│   │   │   └── UserMenu/
│   │   │
│   │   ├── trading/                # Trading components
│   │   │   ├── OrderForm/
│   │   │   │   ├── OrderForm.tsx
│   │   │   │   └── OrderForm.module.css
│   │   │   ├── OrderBook/
│   │   │   │   ├── OrderBook.tsx
│   │   │   │   └── OrderBook.module.css
│   │   │   ├── OrderList/
│   │   │   ├── TickerList/
│   │   │   ├── TickerCard/
│   │   │   ├── TickerSearch/
│   │   │   └── PriceDisplay/
│   │   │
│   │   ├── portfolio/              # Portfolio components
│   │   │   ├── PortfolioSummary/
│   │   │   │   ├── PortfolioSummary.tsx
│   │   │   │   └── PortfolioSummary.module.css
│   │   │   ├── PositionCard/
│   │   │   ├── PositionList/
│   │   │   ├── PerformanceChart/
│   │   │   ├── AssetAllocation/
│   │   │   └── TransactionHistory/
│   │   │
│   │   ├── charts/                 # Chart components
│   │   │   ├── TradingChart/
│   │   │   │   ├── TradingChart.tsx
│   │   │   │   └── TradingChart.module.css
│   │   │   ├── LineChart/
│   │   │   ├── PieChart/
│   │   │   ├── BarChart/
│   │   │   └── Candlestick/
│   │   │
│   │   ├── watchlist/              # Watchlist components
│   │   │   ├── WatchlistCard/
│   │   │   ├── WatchlistItem/
│   │   │   └── AddToWatchlist/
│   │   │
│   │   └── alerts/                 # Alert components
│   │       ├── PriceAlert/
│   │       ├── AlertList/
│   │       └── CreateAlert/
│   │
│   ├── pages/                      # Page components
│   │   ├── Home/
│   │   │   ├── HomePage.tsx
│   │   │   └── HomePage.module.css
│   │   ├── Login/
│   │   │   ├── LoginPage.tsx
│   │   │   └── LoginPage.module.css
│   │   ├── Register/
│   │   │   ├── RegisterPage.tsx
│   │   │   └── RegisterPage.module.css
│   │   ├── Dashboard/
│   │   │   ├── DashboardPage.tsx
│   │   │   └── DashboardPage.module.css
│   │   ├── Trade/
│   │   │   ├── TradePage.tsx
│   │   │   └── TradePage.module.css
│   │   ├── Portfolio/
│   │   │   ├── PortfolioPage.tsx
│   │   │   └── PortfolioPage.module.css
│   │   ├── Orders/
│   │   │   ├── OrdersPage.tsx
│   │   │   └── OrdersPage.module.css
│   │   ├── Watchlist/
│   │   ├── Settings/
│   │   └── NotFound/
│   │
│   ├── store/                      # Redux state management
│   │   ├── index.ts                # Store configuration
│   │   ├── hooks.ts                # Typed hooks
│   │   ├── slices/                 # Redux slices
│   │   │   ├── authSlice.ts
│   │   │   ├── userSlice.ts
│   │   │   ├── portfolioSlice.ts
│   │   │   ├── ordersSlice.ts
│   │   │   ├── positionsSlice.ts
│   │   │   ├── marketDataSlice.ts
│   │   │   ├── watchlistSlice.ts
│   │   │   └── uiSlice.ts
│   │   └── middleware/             # Custom middleware
│   │       └── websocketMiddleware.ts
│   │
│   ├── services/                   # API services
│   │   ├── api.ts                  # Axios instance
│   │   ├── authService.ts          # Auth API calls
│   │   ├── userService.ts          # User API calls
│   │   ├── tradingService.ts       # Trading API calls
│   │   ├── portfolioService.ts     # Portfolio API calls
│   │   ├── marketDataService.ts    # Market data API calls
│   │   ├── watchlistService.ts     # Watchlist API calls
│   │   ├── alertService.ts         # Alert API calls
│   │   └── websocket.ts            # WebSocket client
│   │
│   ├── hooks/                      # Custom React hooks
│   │   ├── useAuth.ts              # Authentication hook
│   │   ├── useWebSocket.ts         # WebSocket hook
│   │   ├── useRealTimePrice.ts     # Real-time price hook
│   │   ├── usePortfolio.ts         # Portfolio hook
│   │   ├── useOrders.ts            # Orders hook
│   │   ├── useMarketData.ts        # Market data hook
│   │   ├── useLocalStorage.ts      # LocalStorage hook
│   │   └── useDebounce.ts          # Debounce hook
│   │
│   ├── utils/                      # Utility functions
│   │   ├── formatters.ts           # Format numbers, dates, etc.
│   │   ├── validators.ts           # Input validation
│   │   ├── constants.ts            # App constants
│   │   ├── helpers.ts              # Helper functions
│   │   ├── api-helpers.ts          # API utilities
│   │   └── chart-helpers.ts        # Chart utilities
│   │
│   ├── types/                      # TypeScript type definitions
│   │   ├── index.ts                # Main types export
│   │   ├── user.ts                 # User types
│   │   ├── auth.ts                 # Auth types
│   │   ├── order.ts                # Order types
│   │   ├── position.ts             # Position types
│   │   ├── portfolio.ts            # Portfolio types
│   │   ├── marketData.ts           # Market data types
│   │   ├── watchlist.ts            # Watchlist types
│   │   ├── alert.ts                # Alert types
│   │   └── api.ts                  # API response types
│   │
│   ├── styles/                     # Global styles
│   │   ├── variables.css           # CSS variables
│   │   ├── mixins.css              # CSS mixins
│   │   ├── animations.css          # Animations
│   │   ├── typography.css          # Typography
│   │   └── utilities.css           # Utility classes
│   │
│   └── config/                     # Configuration
│       ├── index.ts                # Main config
│       ├── api.config.ts           # API configuration
│       ├── theme.config.ts         # Theme configuration
│       └── routes.config.ts        # Routes configuration
│
├── tests/                          # Test files (mirroring src)
│   ├── setup.ts                    # Test setup
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── utils/
│
├── .storybook/                     # Storybook configuration
│   ├── main.ts
│   └── preview.ts
│
├── package.json                    # NPM dependencies
├── package-lock.json               # NPM lock file
├── tsconfig.json                   # TypeScript configuration
├── tsconfig.node.json              # TypeScript Node config
├── vite.config.ts                  # Vite configuration
├── vitest.config.ts                # Vitest test configuration
├── .eslintrc.cjs                   # ESLint configuration
├── .prettierrc                     # Prettier configuration
├── Dockerfile                      # Docker image definition
├── .dockerignore                   # Docker ignore patterns
├── .env.example                    # Environment variables template
└── README.md                       # Frontend documentation
```

---

## Docker Structure

```
docker/
├── backend/
│   ├── Dockerfile                  # Backend Docker image
│   └── entrypoint.sh               # Backend entrypoint script
├── frontend/
│   ├── Dockerfile                  # Frontend Docker image
│   └── nginx.conf                  # Nginx configuration
├── postgres/
│   ├── init.sql                    # Database initialization
│   └── Dockerfile                  # Custom Postgres image (if needed)
└── redis/
    └── redis.conf                  # Redis configuration
```

---

## Scripts Directory

```
scripts/
├── setup.sh                        # Initial setup script
├── dev.sh                          # Start development environment
├── deploy.sh                       # Deployment script
├── backup.sh                       # Database backup script
├── seed-db.py                      # Seed database with test data
├── generate-api-docs.sh            # Generate API documentation
└── load-test.py                    # Load testing script
```

---

## GitHub Actions CI/CD

```
.github/
├── workflows/
│   ├── backend-tests.yml           # Backend test workflow
│   ├── frontend-tests.yml          # Frontend test workflow
│   ├── deploy-staging.yml          # Deploy to staging
│   ├── deploy-production.yml       # Deploy to production
│   └── security-scan.yml           # Security scanning
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   └── feature_request.md
└── pull_request_template.md
```

---

## Documentation Directory

```
docs/
├── api/
│   ├── authentication.md           # Auth API docs
│   ├── trading.md                  # Trading API docs
│   ├── portfolio.md                # Portfolio API docs
│   └── market-data.md              # Market data API docs
├── guides/
│   ├── getting-started.md          # Getting started guide
│   ├── development.md              # Development guide
│   ├── deployment.md               # Deployment guide
│   └── troubleshooting.md          # Troubleshooting guide
├── architecture/
│   ├── system-design.md            # System architecture
│   ├── database-schema.md          # Database design
│   └── security.md                 # Security architecture
└── images/                         # Documentation images
    ├── architecture-diagram.png
    └── er-diagram.png
```

---

## Configuration Files

### Root `.gitignore`

```gitignore
# Environment
.env
.env.local

# Dependencies
node_modules/
__pycache__/
*.pyc
venv/
.venv/

# Build outputs
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite

# Testing
coverage/
.coverage
htmlcov/

# Docker
docker-compose.override.yml
```

### Root `README.md` Template

```markdown
# SpeedTrade - Fast Trading for Small-Time Traders

## 🚀 Quick Start

\`\`\`bash
# Clone repository
git clone https://github.com/your-org/speedtrade.git
cd speedtrade

# Copy environment variables
cp .env.example .env

# Start with Docker
docker-compose up -d

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
\`\`\`

## 📚 Documentation

- [Getting Started Guide](docs/guides/getting-started.md)
- [API Documentation](docs/api/)
- [Development Guide](docs/guides/development.md)
- [Deployment Guide](docs/guides/deployment.md)

## 🛠️ Tech Stack

**Backend:** Python, FastAPI, PostgreSQL, Redis  
**Frontend:** React, TypeScript, Redux, TradingView  
**Trading:** Alpaca API, CCXT  
**Infrastructure:** Docker, Nginx

## 📄 License

MIT License - see LICENSE file for details
```

---

## Environment Variables

### Backend `.env.example`

```bash
# Database
DATABASE_URL=postgresql://speedtrade:password@localhost:5432/speedtrade_db

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-generate-with-openssl-rand-hex-32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Alpaca
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Binance
BINANCE_API_KEY=your_binance_api_key
BINANCE_SECRET_KEY=your_binance_secret_key

# Polygon
POLYGON_API_KEY=your_polygon_api_key

# Environment
ENVIRONMENT=development
DEBUG=True
```

### Frontend `.env.example`

```bash
# API URLs
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Feature Flags
VITE_ENABLE_CRYPTO=true
VITE_ENABLE_ANALYTICS=false

# Environment
VITE_ENVIRONMENT=development
```

---

## File Naming Conventions

### Backend (Python)
- **Files:** `snake_case.py`
- **Classes:** `PascalCase`
- **Functions:** `snake_case()`
- **Constants:** `UPPER_SNAKE_CASE`

### Frontend (TypeScript)
- **Components:** `PascalCase.tsx`
- **Utilities:** `camelCase.ts`
- **Types:** `PascalCase.ts`
- **Styles:** `ComponentName.module.css`

### Tests
- **Backend:** `test_feature_name.py`
- **Frontend:** `ComponentName.test.tsx`

---

## Code Organization Principles

### 1. **Feature-Based Structure**
Group related files by feature, not by type.

### 2. **Separation of Concerns**
- Models: Data structure
- Schemas: Data validation
- Services: Business logic
- API Endpoints: HTTP routing

### 3. **DRY (Don't Repeat Yourself)**
Create reusable components and utilities.

### 4. **Single Responsibility**
Each module should have one clear purpose.

### 5. **Clear Dependencies**
- Core → Models → Services → API
- No circular dependencies

---

## Quick Reference

### Find a specific file:

```bash
# Backend
cd backend/app

# Frontend  
cd frontend/src

# Documentation
cd docs

# Docker configs
cd docker

# Scripts
cd scripts
```

### Common tasks:

```bash
# Add new API endpoint
backend/app/api/v1/endpoints/new_feature.py

# Add new page
frontend/src/pages/NewPage/

# Add new component
frontend/src/components/feature/NewComponent/

# Add new service
backend/app/services/new_service.py

# Add database model
backend/app/models/new_model.py
```

---

## Best Practices

### Backend
1. Use type hints in Python
2. Write docstrings for functions
3. Keep endpoints thin, logic in services
4. Use Pydantic for validation
5. Write tests for business logic

### Frontend
1. Use TypeScript strictly
2. Component composition over inheritance
3. Keep components small (<200 lines)
4. Use custom hooks for logic
5. Test user interactions

### General
1. Commit frequently with clear messages
2. Keep .env files secure
3. Document complex logic
4. Review code before merging
5. Keep dependencies updated

---

**This structure supports:**
- ✅ Easy navigation
- ✅ Clear separation of concerns
- ✅ Scalability
- ✅ Team collaboration
- ✅ Testing
- ✅ Deployment

---

**Previous:** [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)  
**Next:** [SPEEDTRADE_PACKAGE.md](SPEEDTRADE_PACKAGE.md)
