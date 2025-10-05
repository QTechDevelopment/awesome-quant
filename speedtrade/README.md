# SpeedTrade

High-speed trading platform for stocks and crypto under $100, built for retail traders who value speed and volume.

## 🚀 Features

- **Lightning Fast**: < 100ms order execution
- **Multi-Asset**: Trade stocks and crypto from one platform
- **Real-Time Data**: Live price updates via WebSocket
- **Smart Filters**: Focus on assets under $100
- **Portfolio Management**: Track P&L and positions in real-time
- **Paper Trading**: Test strategies risk-free
- **Mobile-First**: Responsive design for trading on the go

## 📋 Project Status

**Current Phase**: MVP Development (Week 2/8)

### Completed ✅
- Backend API architecture
- Authentication system (JWT)
- Database models (Users, Orders, Positions, Portfolio)
- Trading service (Alpaca integration)
- Market data service (real-time quotes, charts)
- Order management (place, cancel, track)
- Portfolio tracking
- WebSocket for real-time updates
- Docker containerization
- Unit tests setup
- API documentation

### In Progress 🔄
- Frontend React application
- WebSocket client integration
- Advanced order types
- Risk management

### Upcoming 📅
- KYC integration (Plaid)
- Bank transfers (ACH)
- Push notifications
- Advanced charting
- Social features
- Mobile apps (iOS/Android)

## 🏗️ Architecture

```
speedtrade/
├── backend/          # FastAPI REST API + WebSocket
├── frontend/         # React + TypeScript SPA
├── infrastructure/   # Docker, K8s, Terraform
└── docs/            # Documentation
```

### Tech Stack

**Backend**:
- FastAPI (Python 3.11+)
- PostgreSQL (database)
- Redis (caching)
- SQLAlchemy (ORM)
- Alembic (migrations)
- Alpaca API (stock trading)
- CCXT (crypto trading)

**Frontend**:
- React 18 + TypeScript
- Redux Toolkit (state)
- TailwindCSS (styling)
- Recharts (charting)
- Socket.io (WebSocket)

**Infrastructure**:
- Docker + Docker Compose
- Kubernetes (production)
- Nginx (reverse proxy)
- TimescaleDB (time-series data)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### Backend Setup

```bash
cd backend
./setup.sh
```

Or manually:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run database migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

API will be available at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Docker Setup (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

This starts:
- Backend API (port 8000)
- PostgreSQL (port 5432)
- Redis (port 6379)
- TimescaleDB (port 5433)

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

App will be available at http://localhost:3000

## 📚 Documentation

- [Backend README](backend/README.md) - API documentation, deployment
- [START_HERE.md](START_HERE.md) - Navigation guide
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Executive overview
- [MVP_ARCHITECTURE.md](MVP_ARCHITECTURE.md) - Technical architecture
- [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - Code examples
- [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) - Development timeline
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - File organization

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/unit/test_auth.py
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm run test:coverage
```

## 🔑 API Keys Required

### Alpaca (Stock Trading - Required)
1. Sign up at https://alpaca.markets
2. Get API keys for paper trading
3. Add to `.env`:
   ```
   ALPACA_API_KEY=your_key
   ALPACA_SECRET_KEY=your_secret
   ALPACA_PAPER_TRADING=true
   ```

### Polygon.io (Market Data - Optional)
1. Sign up at https://polygon.io
2. Get free API key
3. Add to `.env`:
   ```
   POLYGON_API_KEY=your_key
   ```

### Coinbase (Crypto - Optional)
For crypto trading functionality

## 📖 API Examples

### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "trader@example.com",
    "username": "trader",
    "full_name": "Trader Joe",
    "password": "securepassword"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=trader@example.com&password=securepassword"
```

### Place Order
```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "side": "buy",
    "order_type": "market",
    "quantity": "10",
    "asset_type": "stock"
  }'
```

### Get Portfolio
```bash
curl http://localhost:8000/api/v1/portfolio \
  -H "Authorization: Bearer <access_token>"
```

### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/market?token=<access_token>');

// Subscribe to symbols
ws.send(JSON.stringify({
  action: 'subscribe',
  symbols: ['AAPL', 'BTC/USD']
}));

// Receive price updates
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Price update:', data);
};
```

## 🛣️ Roadmap

### Phase 1: MVP (Weeks 1-8) ✅
- Core trading functionality
- Portfolio management
- Basic market data
- Authentication & security

### Phase 2: Enhancement (Weeks 9-16)
- Advanced order types
- Technical indicators
- Price alerts
- Trade history & analytics

### Phase 3: Social (Weeks 17-24)
- User profiles
- Trade sharing
- Leaderboards
- Educational content

### Phase 4: Mobile (Weeks 25-32)
- iOS app
- Android app
- Push notifications
- Biometric auth

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- [Alpaca](https://alpaca.markets) - Stock trading API
- [CCXT](https://github.com/ccxt/ccxt) - Crypto exchange library
- [FastAPI](https://fastapi.tiangolo.com) - Web framework
- [React](https://react.dev) - Frontend framework

## 📞 Support

- **Email**: support@speedtrade.com
- **Documentation**: [API Docs](http://localhost:8000/api/docs)
- **Issues**: [GitHub Issues](https://github.com/yourusername/speedtrade/issues)

---

Built with ⚡ for speed traders

*Note: This is paper trading software. Always test thoroughly before using real money.*
