# ⚡ SpeedTrade - Quick Reference Package

## 🎯 One-Page Overview

**What:** Robinhood-like trading app for stocks and crypto under $100  
**Why:** Speed-focused platform for small-time traders  
**When:** 8 weeks to MVP  
**Cost:** $84,000 (dev) + $1,134/month (ops)  
**Team:** 2 developers + 1 designer

---

## 📊 Key Numbers

| Metric | Value |
|--------|-------|
| **Development Time** | 8 weeks (40 days) |
| **Dev Cost** | $84,000 |
| **Monthly Operations** | $1,134 |
| **Break-Even Users** | 200 premium @ $9.99/mo |
| **Target Performance** | < 100ms order execution |
| **Concurrent Users (MVP)** | 1,000 |
| **Test Coverage Target** | 80% backend, 70% frontend |

---

## 🛠️ Technology Stack

### Backend
```
Python 3.10+ → FastAPI → PostgreSQL → Redis
```

**Libraries:**
- `fastapi` - Web framework
- `sqlalchemy` - ORM
- `alpaca-trade-api` - Stock trading
- `ccxt` - Crypto trading
- `yfinance` - Market data
- `python-socketio` - WebSocket

### Frontend
```
React 18 → TypeScript → Redux → Vite
```

**Libraries:**
- `@reduxjs/toolkit` - State management
- `react-router-dom` - Routing
- `axios` - HTTP client
- `socket.io-client` - WebSocket
- `lightweight-charts` - TradingView charts
- `@mui/material` - UI components

### Infrastructure
```
Docker → Nginx → PostgreSQL → Redis
```

**Production:**
- AWS/DigitalOcean VPS
- Cloudflare CDN
- GitHub Actions CI/CD
- Prometheus + Grafana monitoring

---

## 🚀 Quick Start Commands

### Development Setup

```bash
# 1. Clone project
git clone https://github.com/your-org/speedtrade.git
cd speedtrade

# 2. Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# 3. Start with Docker
docker-compose up -d

# 4. Access application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Without Docker

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Database Setup

```bash
# Run migrations
cd backend
alembic upgrade head

# Seed test data (optional)
python scripts/seed-db.py
```

---

## 📁 Project Structure Cheat Sheet

```
speedtrade/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI app
│       ├── models/              # Database models
│       ├── schemas/             # Pydantic schemas
│       ├── api/v1/endpoints/    # API endpoints
│       ├── services/            # Business logic
│       ├── integrations/        # Alpaca, CCXT
│       └── websocket/           # Real-time
│
├── frontend/
│   └── src/
│       ├── components/          # React components
│       ├── pages/               # Page components
│       ├── store/               # Redux store
│       ├── services/            # API calls
│       ├── hooks/               # Custom hooks
│       └── types/               # TypeScript types
│
└── docker-compose.yml           # Docker orchestration
```

---

## 🎯 API Endpoints Reference

### Authentication
```
POST   /api/v1/auth/register     # Register user
POST   /api/v1/auth/login        # Login (get JWT)
GET    /api/v1/auth/me           # Get current user
```

### Trading
```
POST   /api/v1/orders            # Place order
GET    /api/v1/orders            # List orders
GET    /api/v1/orders/{id}       # Get order
DELETE /api/v1/orders/{id}       # Cancel order
```

### Portfolio
```
GET    /api/v1/portfolio         # Portfolio summary
GET    /api/v1/positions         # List positions
GET    /api/v1/portfolio/history # Performance history
```

### Market Data
```
GET    /api/v1/market/quote/{symbol}  # Get quote
GET    /api/v1/market/under-100       # Assets under $100
GET    /api/v1/market/search          # Search symbols
```

---

## 🔑 Environment Variables

### Required Backend Variables
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
ALPACA_API_KEY=your-alpaca-key
ALPACA_SECRET_KEY=your-alpaca-secret
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

### Required Frontend Variables
```bash
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

---

## 📅 8-Week Milestone Checklist

- [ ] **Week 1** - Foundation: Auth, Docker, Project setup (12.5%)
- [ ] **Week 2** - Core: Database, Order placement, Alpaca (25%)
- [ ] **Week 3** - Trading: Limit orders, Crypto, Order book (37.5%)
- [ ] **Week 4** - Portfolio: Performance tracking, Charts (50%)
- [ ] **Week 5** - Real-Time: WebSocket, Live prices, Updates (62.5%)
- [ ] **Week 6** - UI: Dashboard, Trading interface, Polish (75%)
- [ ] **Week 7** - Testing: Unit tests, Load tests, Bug fixes (87.5%)
- [ ] **Week 8** - Launch: Beta testing, Docs, Deployment (100%)

---

## 🧪 Testing Commands

### Backend Tests
```bash
cd backend
pytest                           # Run all tests
pytest tests/test_auth.py        # Run specific test
pytest --cov=app                 # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test                         # Run all tests
npm test -- OrderForm.test.tsx   # Run specific test
npm run test:coverage            # With coverage
```

### Load Testing
```bash
# Install Locust
pip install locust

# Run load test
cd scripts
locust -f load-test.py
# Visit http://localhost:8089
```

---

## 🚢 Deployment Commands

### Build Production Images
```bash
docker-compose -f docker-compose.prod.yml build
```

### Deploy to Production
```bash
# Via Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Via Manual Deployment
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

cd frontend
npm run build
# Serve dist/ folder with Nginx
```

### Database Migration
```bash
cd backend
alembic upgrade head              # Apply migrations
alembic downgrade -1              # Rollback one migration
alembic revision --autogenerate -m "message"  # Create migration
```

---

## 🔐 Security Checklist

- [ ] Use HTTPS in production
- [ ] Store API keys in environment variables
- [ ] Hash passwords with bcrypt
- [ ] Use JWT with short expiration
- [ ] Validate all user inputs
- [ ] Implement rate limiting
- [ ] Enable CORS properly
- [ ] Encrypt sensitive data at rest
- [ ] Regular security audits
- [ ] Keep dependencies updated

---

## 🐛 Common Issues & Solutions

### Issue: Docker containers won't start
```bash
# Solution: Clean up Docker
docker-compose down
docker system prune -a
docker-compose up -d --build
```

### Issue: Database connection error
```bash
# Solution: Check PostgreSQL is running
docker-compose ps
# Restart PostgreSQL
docker-compose restart postgres
```

### Issue: Frontend can't connect to backend
```bash
# Solution: Check CORS settings
# In backend/app/main.py, ensure:
allow_origins=["http://localhost:3000"]
```

### Issue: WebSocket connection fails
```bash
# Solution: Ensure WebSocket endpoint is correct
# Frontend: VITE_WS_URL=ws://localhost:8000 (not wss://)
```

### Issue: Alpaca API errors
```bash
# Solution: Verify paper trading keys
# Visit: https://app.alpaca.markets/paper/dashboard/overview
# Regenerate API keys if needed
```

---

## 📚 Learning Resources

### Awesome-Quant Libraries
- [awesome-quant repo](https://github.com/QTechDevelopment/awesome-quant)
- [nautilus_trader](https://github.com/nautechsystems/nautilus_trader) - Trading platform
- [alpaca-trade-api](https://github.com/alpacahq/alpaca-trade-api-python) - Stock trading
- [ccxt](https://github.com/ccxt/ccxt) - Crypto trading
- [yfinance](https://github.com/ranaroussi/yfinance) - Market data

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [Alpaca API](https://alpaca.markets/docs/api-references/)
- [CCXT Docs](https://docs.ccxt.com/)
- [TradingView Charts](https://www.tradingview.com/lightweight-charts/)

### Tutorials
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [React TypeScript Tutorial](https://react-typescript-cheatsheet.netlify.app/)
- [Docker Tutorial](https://docs.docker.com/get-started/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)

---

## 💡 Pro Tips

### Development
1. **Use Docker** - Consistent environment for everyone
2. **Git branches** - Feature branches, PR reviews
3. **Daily standups** - 15-minute team sync
4. **Test as you go** - Don't leave testing for the end
5. **Document complex logic** - Future you will thank you

### Performance
1. **Cache aggressively** - Redis for hot data
2. **Database indexes** - On foreign keys and queries
3. **Optimize images** - Use WebP format
4. **Code splitting** - Lazy load routes
5. **CDN for static assets** - Cloudflare free tier

### Production
1. **Start with paper trading** - Don't risk real money
2. **Monitor everything** - Prometheus + Grafana
3. **Have a rollback plan** - Database backups daily
4. **Rate limit APIs** - Prevent abuse
5. **Error tracking** - Sentry for catching bugs

---

## 🎯 Success Metrics

### Technical Metrics
```
✅ Order Execution: < 100ms (P95)
✅ API Response: < 200ms (P95)
✅ Page Load: < 2 seconds
✅ WebSocket Latency: < 50ms
✅ Uptime: 99.5%
✅ Test Coverage: 80%
```

### Business Metrics
```
✅ Beta Users: 100 (Week 8)
✅ Active Users: 500 (Month 3)
✅ Premium Users: 200 (Month 6)
✅ Monthly Revenue: $3,500 (Break-even)
✅ User Retention: 40% (D7)
```

---

## 📞 Quick Links

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [START_HERE.md](START_HERE.md) | Navigation guide | First time here |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Executive overview | Decision making |
| [MVP_ARCHITECTURE.md](MVP_ARCHITECTURE.md) | Technical design | Architecture planning |
| [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) | Code examples | Start coding |
| [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) | 8-week plan | Daily tasks |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | File organization | Finding files |
| [SPEEDTRADE_PACKAGE.md](SPEEDTRADE_PACKAGE.md) | Quick reference | Quick lookups |

---

## 🏁 Ready to Start?

### This Week
1. ✅ Read [START_HERE.md](START_HERE.md)
2. ✅ Set up Alpaca paper trading account
3. ✅ Run `docker-compose up -d`
4. ✅ Explore the API docs at http://localhost:8000/docs

### Next Week
1. ✅ Follow [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md) Week 1 tasks
2. ✅ Complete authentication system
3. ✅ Integrate Alpaca API
4. ✅ Weekly team demo

---

## 📊 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024 | Initial comprehensive package |

---

## 💬 Support & Community

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Discord:** (Set up community server)
- **Email:** support@speedtrade.com

---

**🚀 Let's build something amazing!**

This is your complete reference package. Everything you need is here.

**Start with:** [START_HERE.md](START_HERE.md)  
**Need help?** Check [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)  
**Daily tasks?** See [PROJECT_ROADMAP.md](PROJECT_ROADMAP.md)

**Good luck! You got this! 💪**
