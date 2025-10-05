# 🚀 SpeedTrade - Fast Trading Application

A high-performance trading platform for stocks and cryptocurrencies under $100, built with FastAPI and React.

## Project Status

**Current Phase:** MVP Complete ✅  
**Next Phase:** Testing & Production Setup 🚧

### Completed ✅
- ✅ Backend API with 18 REST endpoints + WebSocket
- ✅ User authentication with JWT + bcrypt
- ✅ Database models (User, Order, Position, Portfolio)
- ✅ Trading integration (Alpaca for stocks, CCXT for crypto)
- ✅ Portfolio management with real-time P&L
- ✅ WebSocket server for live price updates
- ✅ Frontend React application (6 pages, Redux state)
- ✅ Docker containerization
- ✅ Database migrations with Alembic
- ✅ Comprehensive documentation (11 guides)

### In Progress 🚧
- Testing with live API keys
- Security hardening and audit
- Production infrastructure setup
- Monitoring and alerting
- CI/CD pipeline

### What You Can Do Now
- Register and login users
- Place market/limit orders (with API keys)
- Track portfolio and positions
- View order history
- Real-time WebSocket updates

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.10+ (for local development)
- Node.js 18+ (for frontend development)

### Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/QTechDevelopment/awesome-quant.git
   cd awesome-quant
   ```

2. **Start all services:**
   ```bash
   docker-compose up -d
   ```

3. **Access the application:**
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Interactive API: http://localhost:8000/redoc

4. **View logs:**
   ```bash
   docker-compose logs -f backend
   ```

5. **Stop services:**
   ```bash
   docker-compose down
   ```

### Local Development

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```

6. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Architecture

### Backend Stack
- **Framework:** FastAPI (Python 3.10+)
- **Database:** PostgreSQL 15
- **Cache:** Redis 7
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Authentication:** JWT with OAuth2
- **WebSocket:** Native FastAPI WebSocket support

### Frontend Stack
- **Framework:** React 18 + TypeScript ✅
- **State Management:** Redux Toolkit ✅
- **UI Components:** TailwindCSS ✅
- **Charts:** Recharts ✅
- **Build Tool:** Vite ✅
- **Forms:** React Hook Form + Zod ✅

### Trading APIs
- **Stocks:** Alpaca API (paper trading)
- **Crypto:** CCXT (multiple exchanges)
- **Market Data:** Polygon.io, Yahoo Finance

## Project Structure

```
awesome-quant/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── main.py          # Application entry point
│   │   ├── database.py      # Database configuration
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── api/v1/          # API endpoints
│   │   ├── core/            # Core configuration
│   │   └── websocket/       # WebSocket handlers
│   ├── alembic/             # Database migrations
│   ├── tests/               # Unit tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # React frontend ✅
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── components/      # Reusable components
│   │   ├── services/        # API services
│   │   ├── store/           # Redux store
│   │   └── types/           # TypeScript types
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml       # Docker orchestration
├── START_HERE.md            # 📖 Navigation guide
├── CHAT_LOG.md              # 📜 Development history
├── TESTING_GUIDE.md         # 🧪 Testing instructions
├── STATUS.md                # 📊 Current status
└── docs/                    # Additional documentation
    ├── START_HERE.md
    ├── PROJECT_SUMMARY.md
    ├── MVP_ARCHITECTURE.md
    ├── IMPLEMENTATION_GUIDE.md
    └── PROJECT_ROADMAP.md
```

## 📚 Documentation

SpeedTrade includes comprehensive documentation to help you understand and use the platform:

### Getting Started
- **[START_HERE.md](START_HERE.md)** - Your navigation hub and entry point
- **[STATUS.md](STATUS.md)** - Current project status and what's working
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - How to test the application

### Development History
- **[CHAT_LOG.md](CHAT_LOG.md)** - Complete development history (27k+ lines)
  - 20 phases documented
  - All design decisions explained
  - Challenges and solutions
  - Technology stack details

### Technical Documentation
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Executive overview
- **[MVP_ARCHITECTURE.md](MVP_ARCHITECTURE.md)** - Technical architecture
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Code examples
- **[PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)** - 8-week development plan
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - File organization
- **[SPEEDTRADE_PACKAGE.md](SPEEDTRADE_PACKAGE.md)** - Quick reference
- **[BUILD_SUMMARY.md](BUILD_SUMMARY.md)** - Build statistics

### Quick Stats
- 📄 **11 documentation files**
- 📝 **62,500+ characters** of documentation
- 💻 **5,500+ lines** of code
- 📦 **90+ files** created
- ⏱️ **~15 hours** development time

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Orders
- `POST /api/v1/orders` - Create new order
- `GET /api/v1/orders` - List user's orders
- `GET /api/v1/orders/{id}` - Get order details
- `DELETE /api/v1/orders/{id}` - Cancel order

### Portfolio
- `GET /api/v1/portfolio` - Get portfolio summary

### Positions
- `GET /api/v1/positions` - List current positions
- `GET /api/v1/positions/{symbol}` - Get position for symbol

### WebSocket
- `WS /ws/{user_id}` - WebSocket connection for real-time updates

## Features

### Current Features ✅
- ✅ User registration and authentication
- ✅ JWT-based security with bcrypt password hashing
- ✅ Order creation and management (market/limit orders)
- ✅ Portfolio tracking with real-time P&L
- ✅ Position management across stocks and crypto
- ✅ WebSocket support for real-time updates
- ✅ RESTful API with automatic documentation
- ✅ React frontend with 6 pages
- ✅ Redux state management
- ✅ Form validation with Zod
- ✅ Responsive design with TailwindCSS
- ✅ Trading integration (Alpaca + CCXT)
- ✅ Order history and cancellation

### Needs Testing ⚠️
- ⚠️ Live order placement (requires API keys)
- ⚠️ Real-time price streaming
- ⚠️ WebSocket authentication
- ⚠️ Position updates from trades
- ⚠️ Portfolio P&L calculations

### Upcoming Features 🚧
- 🚧 Security audit and hardening
- 🚧 Rate limiting
- 🚧 Production deployment
- 🚧 Advanced order types (stop-loss, trailing)
- 🚧 Technical indicators and charts
- 🚧 Price alerts and notifications
- 🚧 Account funding/withdrawal
- 🚧 Mobile apps (React Native)
- 🚧 Social trading features
- 🚧 Tax reporting (1099 forms)

## Development

### Running Tests

```bash
cd backend
pytest
```

### Creating Database Migrations

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Environment Variables

Key environment variables (see `backend/.env.example`):

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/speedtrade_db

# Security
SECRET_KEY=your-secret-key-here

# Trading APIs
ALPACA_API_KEY=your-alpaca-key
ALPACA_SECRET_KEY=your-alpaca-secret
```

## Documentation

Comprehensive documentation is available in the repository:

- **[START_HERE.md](START_HERE.md)** - Project overview and navigation
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Executive summary and feasibility
- **[MVP_ARCHITECTURE.md](MVP_ARCHITECTURE.md)** - Technical architecture
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Code examples and setup
- **[PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)** - 8-week development plan
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - File organization
- **[SPEEDTRADE_PACKAGE.md](SPEEDTRADE_PACKAGE.md)** - Quick reference

## Contributing

This is a work in progress. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

See LICENSE file for details.

## Roadmap

### Week 1-2: Foundation ✅
- [x] Backend structure
- [x] Authentication system
- [x] Database models
- [x] Basic API endpoints
- [ ] Frontend initialization

### Week 3-4: Trading Core 🚧
- [ ] Alpaca API integration
- [ ] Order execution
- [ ] Real-time price updates
- [ ] Portfolio sync

### Week 5-6: Real-Time Features 📋
- [ ] WebSocket price streaming
- [ ] Live order updates
- [ ] Advanced charts
- [ ] Price alerts

### Week 7-8: Polish & Launch 📋
- [ ] UI/UX refinement
- [ ] Load testing
- [ ] Security audit
- [ ] Beta launch

## Support

For questions and support:
- Open an issue on GitHub
- Check the documentation in the `docs/` directory
- Review the implementation guide

## Acknowledgments

Built using the awesome-quant library collection and following best practices from:
- FastAPI documentation
- React best practices
- Trading platform design patterns
- Alpaca API documentation
- CCXT library documentation

---

**Current Version:** 0.1.0 (Backend Foundation)  
**Last Updated:** 2024

🚀 Building the future of fast trading!
