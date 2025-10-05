# SpeedTrade Backend

FastAPI-based backend for the SpeedTrade trading application.

## Features

- ✅ User authentication with JWT
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Alembic database migrations
- ✅ Redis for caching and real-time data
- ✅ RESTful API design with versioning
- 🚧 Alpaca API integration for stock trading
- 🚧 CCXT integration for crypto trading
- 🚧 WebSocket support for real-time updates

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL 15+
- Redis 7+
- Docker (optional, for containerized setup)

### Installation

1. **Clone the repository:**
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

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### Docker Setup

1. **Start all services:**
   ```bash
   cd ..
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f backend
   ```

3. **Stop services:**
   ```bash
   docker-compose down
   ```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `GET /api/v1/auth/me` - Get current user information

### Health Check

- `GET /health` - Health check endpoint

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database configuration
│   ├── core/
│   │   └── config.py        # Application settings
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── order.py
│   │   ├── position.py
│   │   └── portfolio.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py
│   │   ├── order.py
│   │   ├── position.py
│   │   └── portfolio.py
│   ├── api/v1/
│   │   ├── router.py        # API router
│   │   └── endpoints/       # API endpoints
│   │       └── auth.py
│   ├── services/            # Business logic (TODO)
│   └── websocket/           # WebSocket handlers (TODO)
├── alembic/                 # Database migrations
├── requirements.txt
├── Dockerfile
└── README.md
```

## Development

### Running Tests

```bash
pytest
```

### Creating Database Migrations

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Code Style

Follow PEP 8 guidelines. Use `black` for formatting:

```bash
pip install black
black app/
```

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT secret key
- `ALPACA_API_KEY` - Alpaca API key for stock trading
- `ALPACA_SECRET_KEY` - Alpaca secret key

## Next Steps

- [ ] Implement order management endpoints
- [ ] Add Alpaca API integration
- [ ] Create WebSocket manager for real-time data
- [ ] Add portfolio tracking endpoints
- [ ] Implement position management
- [ ] Add comprehensive testing
- [ ] Set up CI/CD pipeline

## License

See LICENSE file in the root directory.
