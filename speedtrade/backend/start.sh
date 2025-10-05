#!/bin/bash
# Quick start script for SpeedTrade Backend

set -e

echo "🚀 Starting SpeedTrade Backend..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in Docker or local
if [ -f "/.dockerenv" ]; then
    echo -e "${BLUE}Running in Docker container${NC}"
    IS_DOCKER=true
else
    echo -e "${BLUE}Running locally${NC}"
    IS_DOCKER=false
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from template...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env with your API keys before continuing!${NC}"
    exit 1
fi

# If not in Docker, activate venv
if [ "$IS_DOCKER" = false ]; then
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}⚠️  Virtual environment not found. Run ./setup.sh first${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Activating virtual environment...${NC}"
    source venv/bin/activate
fi

# Check database connection
echo -e "${BLUE}Checking database connection...${NC}"
python3 -c "
import os
from sqlalchemy import create_engine
try:
    engine = create_engine(os.getenv('DATABASE_URL', 'postgresql://speedtrade:password@localhost:5432/speedtrade_db'))
    conn = engine.connect()
    conn.close()
    print('✓ Database connected')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    print('Make sure PostgreSQL is running and database exists')
    exit(1)
"

# Check Redis connection
echo -e "${BLUE}Checking Redis connection...${NC}"
python3 -c "
import redis
import os
try:
    r = redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
    r.ping()
    print('✓ Redis connected')
except Exception as e:
    print(f'⚠️  Redis connection failed: {e}')
    print('Redis is optional for MVP but recommended for production')
"

# Run migrations
echo -e "${BLUE}Running database migrations...${NC}"
# alembic upgrade head || echo -e "${YELLOW}⚠️  Migrations failed, you may need to run: alembic revision --autogenerate -m 'Initial'${NC}"

# Start the server
echo ""
echo -e "${GREEN}✅ Starting FastAPI server...${NC}"
echo ""
echo "API Documentation:"
echo "  - Swagger UI: http://localhost:8000/api/docs"
echo "  - ReDoc: http://localhost:8000/api/redoc"
echo "  - Health Check: http://localhost:8000/health"
echo ""
echo "WebSocket:"
echo "  - Market Data: ws://localhost:8000/ws/market?token=<jwt_token>"
echo ""

# Start with uvicorn
if [ "$1" = "--reload" ]; then
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    uvicorn app.main:app --host 0.0.0.0 --port 8000
fi
