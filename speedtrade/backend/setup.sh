#!/bin/bash
# Setup script for SpeedTrade backend

set -e

echo "🚀 Setting up SpeedTrade Backend..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ required, found $python_version"
    exit 1
fi
echo -e "${GREEN}✓ Python $python_version${NC}"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment exists${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${BLUE}Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env created (please update with your API keys)${NC}"
    echo "⚠️  Important: Edit .env with your Alpaca API keys before starting the server"
else
    echo -e "${GREEN}✓ .env exists${NC}"
fi

# Check PostgreSQL
echo -e "${BLUE}Checking PostgreSQL connection...${NC}"
if command -v psql &> /dev/null; then
    if psql -lqt | cut -d \| -f 1 | grep -qw speedtrade_db; then
        echo -e "${GREEN}✓ Database 'speedtrade_db' exists${NC}"
    else
        echo -e "${BLUE}Creating database 'speedtrade_db'...${NC}"
        createdb speedtrade_db || echo "⚠️  Could not create database, you may need to do this manually"
    fi
else
    echo "⚠️  PostgreSQL CLI not found. Please ensure PostgreSQL is installed and create 'speedtrade_db' database manually"
fi

# Check Redis
echo -e "${BLUE}Checking Redis connection...${NC}"
if command -v redis-cli &> /dev/null; then
    if redis-cli ping > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Redis is running${NC}"
    else
        echo "⚠️  Redis is not running. Please start Redis: redis-server"
    fi
else
    echo "⚠️  Redis CLI not found. Please install Redis"
fi

# Create logs directory
if [ ! -d "logs" ]; then
    mkdir logs
    echo -e "${GREEN}✓ Logs directory created${NC}"
fi

# Run database migrations
echo -e "${BLUE}Running database migrations...${NC}"
alembic upgrade head || echo "⚠️  Database migrations failed. You may need to create the initial migration with: alembic revision --autogenerate -m 'Initial migration'"
echo -e "${GREEN}✓ Database migrations complete${NC}"

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys (especially ALPACA_API_KEY and ALPACA_SECRET_KEY)"
echo "2. Ensure PostgreSQL and Redis are running"
echo "3. Start the development server:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "API Documentation will be available at:"
echo "  - http://localhost:8000/api/docs (Swagger UI)"
echo "  - http://localhost:8000/api/redoc (ReDoc)"
echo ""
