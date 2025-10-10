# SpeedTrade - Quick Start Guide

Get SpeedTrade up and running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- OR: Python 3.10+, Node.js 18+, PostgreSQL, and Redis

## Option 1: Docker (Easiest)

### 1. Clone and Start

```bash
git clone https://github.com/QTechDevelopment/awesome-quant.git
cd awesome-quant
docker-compose up -d
```

### 2. Wait for Services to Start

```bash
# Check if services are running
docker-compose ps

# View logs if needed
docker-compose logs -f backend
```

### 3. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### 4. Create Your First User

1. Open http://localhost:3000
2. Click "Register" 
3. Create an account
4. Login with your credentials

### 5. Stop Services

```bash
docker-compose down
```

## Option 2: Local Development

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 5. Start PostgreSQL and Redis
# (Use Docker or install locally)

# 6. Run migrations
alembic upgrade head

# 7. Start server
uvicorn app.main:app --reload
```

Backend will be available at http://localhost:8000

### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Set up environment variables
cp .env.example .env
# Edit .env if needed (default values work with local backend)

# 4. Start development server
npm run dev
```

Frontend will be available at http://localhost:5173

## Configuration

### Essential Environment Variables

**Backend (.env):**
```env
DATABASE_URL=postgresql://speedtrade:password@localhost:5432/speedtrade_db
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Frontend (.env):**
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## Troubleshooting

### Frontend Build Issues

```bash
cd frontend
npm install
npm run build
```

If you see TypeScript errors, make sure you have the latest changes with `vite-env.d.ts` file.

### Backend Won't Start

```bash
# Check if database is running
docker-compose logs db

# Check backend logs
docker-compose logs backend

# Restart services
docker-compose restart backend
```

### CORS Errors

Make sure `ALLOWED_ORIGINS` in backend .env includes your frontend URL:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Database Connection Issues

```bash
# Reset database
docker-compose down -v
docker-compose up -d db
# Wait 10 seconds
docker-compose up backend
```

## Next Steps

1. **Add Trading API Keys** (Optional for testing):
   - Get Alpaca API keys from https://alpaca.markets
   - Add to backend/.env:
     ```env
     ALPACA_API_KEY=your_key
     ALPACA_SECRET_KEY=your_secret
     ```

2. **Explore API Documentation:**
   - Visit http://localhost:8000/docs
   - Try out API endpoints interactively

3. **Start Trading:**
   - Login to frontend
   - View portfolio
   - Place orders (requires API keys)

## Getting Help

- **Documentation:** Check SPEEDTRADE_README.md
- **Issues:** Check TESTING_GUIDE.md for common problems
- **Recent Fixes:** See FIXES.md for what was fixed

## Project Structure

```
awesome-quant/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── docker-compose.yml
├── QUICKSTART.md     # This file
├── SPEEDTRADE_README.md
├── TESTING_GUIDE.md
└── FIXES.md
```

## Development Commands

### Backend
```bash
cd backend
pytest                      # Run tests
black app/                  # Format code
alembic revision -m "msg"   # Create migration
alembic upgrade head        # Run migrations
```

### Frontend
```bash
cd frontend
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview production build
npm run lint     # Lint code
```

### Docker
```bash
docker-compose up -d         # Start all services
docker-compose down          # Stop all services
docker-compose logs -f       # View logs
docker-compose restart       # Restart services
docker-compose build         # Rebuild images
```

---

**Ready to Trade!** 🚀

For detailed information, see:
- [SPEEDTRADE_README.md](SPEEDTRADE_README.md) - Full documentation
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Testing instructions
- [FIXES.md](FIXES.md) - Recent bug fixes
