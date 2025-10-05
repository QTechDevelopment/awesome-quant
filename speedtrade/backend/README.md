"""
README for SpeedTrade Backend
"""

# SpeedTrade Backend API

High-speed trading platform API for stocks and crypto under $100. Built with FastAPI, PostgreSQL, and Redis.

## Features

- **Authentication**: JWT-based auth with access and refresh tokens
- **Trading**: Place market and limit orders for stocks and crypto
- **Portfolio**: Track positions, P&L, and account balances
- **Market Data**: Real-time quotes, charts, and market movers
- **High Performance**: < 100ms order execution with async operations
- **Real-time Updates**: WebSocket support for live price feeds

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL 15 with SQLAlchemy ORM
- **Cache**: Redis 7
- **Trading APIs**: Alpaca (stocks), CCXT (crypto)
- **Market Data**: Polygon.io, yfinance
- **Authentication**: JWT with bcrypt
- **Monitoring**: Loguru, Sentry

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Alpaca API account (paper trading)

### Installation

1. **Clone the repository**
```bash
cd speedtrade/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys and database credentials
```

5. **Setup database**
```bash
# Create database
createdb speedtrade_db

# Run migrations
alembic upgrade head
```

6. **Start the server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

7. **Access the API**
- API Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- Health Check: http://localhost:8000/health

## Docker Setup

### Using Docker Compose (Recommended)

```bash
# Start all services (PostgreSQL, Redis, TimescaleDB, Backend)
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

### Build Docker Image

```bash
docker build -t speedtrade-backend .
docker run -p 8000:8000 --env-file .env speedtrade-backend
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user profile
- `POST /api/v1/auth/logout` - Logout

### Orders
- `POST /api/v1/orders` - Place new order
- `GET /api/v1/orders` - Get order history
- `GET /api/v1/orders/{id}` - Get order details
- `DELETE /api/v1/orders/{id}` - Cancel order

### Portfolio
- `GET /api/v1/portfolio` - Get portfolio summary
- `GET /api/v1/portfolio/positions` - Get open positions
- `GET /api/v1/portfolio/positions/{symbol}` - Get position details

### Market Data
- `GET /api/v1/market/quote/{symbol}` - Get real-time quote
- `GET /api/v1/market/search?query=` - Search symbols
- `GET /api/v1/market/chart/{symbol}` - Get historical chart data
- `GET /api/v1/market/movers/gainers` - Get top gainers
- `GET /api/v1/market/movers/losers` - Get top losers

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_auth.py

# Run specific test
pytest tests/unit/test_auth.py::test_register_user

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration
```

## Development

### Code Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py         # Authentication endpoints
│   │   │   ├── orders.py       # Order management
│   │   │   ├── portfolio.py    # Portfolio endpoints
│   │   │   └── market_data.py  # Market data endpoints
│   │   └── websocket/          # WebSocket handlers
│   ├── core/
│   │   ├── config.py           # Settings management
│   │   ├── database.py         # Database connection
│   │   └── security.py         # Auth utilities
│   ├── models/
│   │   ├── user.py             # User & Portfolio models
│   │   └── trading.py          # Order, Position, Trade models
│   ├── schemas/
│   │   ├── auth.py             # Auth Pydantic schemas
│   │   ├── orders.py           # Order schemas
│   │   ├── portfolio.py        # Portfolio schemas
│   │   └── market_data.py      # Market data schemas
│   ├── services/
│   │   ├── trading_service.py      # Trading logic
│   │   └── market_data_service.py  # Market data fetching
│   └── main.py                 # FastAPI application
├── alembic/                    # Database migrations
├── tests/                      # Test suite
├── requirements.txt
├── Dockerfile
└── README.md
```

### Adding New Endpoints

1. Create schema in `app/schemas/`
2. Add endpoint in `app/api/v1/`
3. Register router in `app/main.py`
4. Write tests in `tests/`

### Environment Variables

Required variables in `.env`:

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/speedtrade_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Alpaca API
ALPACA_API_KEY=your_key
ALPACA_SECRET_KEY=your_secret
ALPACA_PAPER_TRADING=true

# Polygon.io
POLYGON_API_KEY=your_key
```

## Performance Optimization

- **Connection Pooling**: SQLAlchemy pool configured for high concurrency
- **Redis Caching**: Market data cached for fast retrieval
- **Async Operations**: All I/O operations use async/await
- **Database Indexes**: Optimized indexes on frequently queried columns
- **Query Optimization**: N+1 queries eliminated with eager loading

## Monitoring

### Logs

Logs are written to `logs/speedtrade.log` with rotation:
- Rotation: 500 MB
- Retention: 10 days
- Format: JSON for production parsing

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "speedtrade-api",
  "version": "1.0.0",
  "environment": "development"
}
```

## Security

- **Password Hashing**: Bcrypt with salt
- **JWT Tokens**: HS256 algorithm, 30-minute expiry
- **CORS**: Configured for frontend origin
- **Rate Limiting**: TODO - Implement with Redis
- **Input Validation**: Pydantic schemas validate all inputs
- **SQL Injection**: Protected by SQLAlchemy ORM

## Deployment

### Production Checklist

- [ ] Set `DEBUG=false` in .env
- [ ] Use strong `SECRET_KEY`
- [ ] Configure proper CORS origins
- [ ] Enable HTTPS
- [ ] Set up Sentry for error tracking
- [ ] Configure database backups
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Enable rate limiting
- [ ] Configure firewall rules
- [ ] Use production-grade ASGI server (Gunicorn + Uvicorn)

### Production Server

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info \
  --access-logfile - \
  --error-logfile -
```

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Test connection
psql postgresql://speedtrade:password@localhost:5432/speedtrade_db
```

### Redis Connection Issues

```bash
# Check Redis is running
redis-cli ping

# Should return: PONG
```

### Migration Issues

```bash
# Reset database (WARNING: Destroys all data)
alembic downgrade base
alembic upgrade head
```

## Contributing

1. Create a feature branch
2. Make changes with tests
3. Run tests and linting
4. Submit pull request

## License

MIT License - see LICENSE file

## Support

- Documentation: /api/docs
- Issues: GitHub Issues
- Email: support@speedtrade.com

---

Built with ❤️ for high-speed traders
