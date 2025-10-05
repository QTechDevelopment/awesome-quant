# SpeedTrade - Comprehensive Testing Guide

## Overview
This guide provides detailed instructions for testing the SpeedTrade application, including setup, test execution, and troubleshooting.

---

## Quick Start

### Prerequisites
- Docker Desktop installed
- Node.js 18+ and Python 3.10+ (for local development)
- PostgreSQL client tools (optional)
- Postman or curl (for API testing)

### Start Testing Environment

**Option 1: Using Docker (Recommended)**
```bash
cd /path/to/awesome-quant
docker compose up -d
```

**Option 2: Local Development**
```bash
# Terminal 1 - Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm install
npm run dev
```

---

## Backend Testing

### 1. Health Check

**Test:** Verify backend is running

**Command:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy"
}
```

**Status:** ✅ Should return 200 OK

---

### 2. API Documentation

**Test:** Verify interactive API docs are accessible

**URL:** http://localhost:8000/docs

**Expected:** Swagger UI with all endpoints listed

**Manual Test Steps:**
1. Open browser to http://localhost:8000/docs
2. Verify all endpoint categories are visible:
   - Authentication
   - Orders
   - Portfolio
   - Positions
3. Try "Try it out" feature on any endpoint

**Status:** ✅ Should load documentation page

---

### 3. User Registration

**Test:** Create a new user account

**Endpoint:** `POST /api/v1/auth/register`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123"
  }'
```

**Expected Response:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-10-05T19:30:00.000Z"
}
```

**Edge Cases to Test:**
1. **Duplicate Username:**
   ```bash
   # Register same user again
   # Expected: 400 Bad Request - "Username already registered"
   ```

2. **Duplicate Email:**
   ```bash
   # Register with same email, different username
   # Expected: 400 Bad Request - "Email already registered"
   ```

3. **Invalid Email:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username": "test2", "email": "invalid-email", "password": "pass123"}'
   # Expected: 422 Unprocessable Entity - validation error
   ```

4. **Short Password:**
   ```bash
   curl -X POST http://localhost:8000/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"username": "test3", "email": "test3@example.com", "password": "short"}'
   # Expected: 422 Unprocessable Entity - password too short
   ```

**Status:** ✅ Registration should work for valid data

---

### 4. User Login

**Test:** Authenticate and receive JWT token

**Endpoint:** `POST /api/v1/auth/login`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=securepass123"
```

**Expected Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Save Token:**
```bash
export TOKEN="<paste-token-here>"
```

**Edge Cases to Test:**
1. **Wrong Password:**
   ```bash
   # Use incorrect password
   # Expected: 401 Unauthorized
   ```

2. **Non-existent User:**
   ```bash
   # Use username that doesn't exist
   # Expected: 401 Unauthorized
   ```

**Status:** ✅ Login should return valid JWT token

---

### 5. Get Current User

**Test:** Retrieve authenticated user information

**Endpoint:** `GET /api/v1/auth/me`

**Request:**
```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true,
  "is_verified": false,
  "created_at": "2024-10-05T19:30:00.000Z"
}
```

**Edge Cases to Test:**
1. **No Token:**
   ```bash
   curl http://localhost:8000/api/v1/auth/me
   # Expected: 401 Unauthorized
   ```

2. **Invalid Token:**
   ```bash
   curl http://localhost:8000/api/v1/auth/me \
     -H "Authorization: Bearer invalid-token"
   # Expected: 401 Unauthorized
   ```

3. **Expired Token:**
   ```bash
   # Wait 31 minutes (token expires in 30 minutes)
   # Expected: 401 Unauthorized
   ```

**Status:** ✅ Should return user info with valid token

---

### 6. Get Portfolio

**Test:** Retrieve user's portfolio summary

**Endpoint:** `GET /api/v1/portfolio`

**Request:**
```bash
curl http://localhost:8000/api/v1/portfolio \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "cash_balance": 0.0,
  "buying_power": 0.0,
  "portfolio_value": 0.0,
  "long_market_value": 0.0,
  "short_market_value": 0.0,
  "total_pl": 0.0,
  "total_pl_percent": 0.0,
  "day_pl": 0.0,
  "day_pl_percent": 0.0,
  "created_at": "2024-10-05T19:30:00.000Z",
  "updated_at": null
}
```

**Status:** ✅ Should return portfolio (initially zero balances)

---

### 7. Place Order

**Test:** Submit a trading order

**Endpoint:** `POST /api/v1/orders`

**Request (Market Order):**
```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "asset_type": "stock",
    "side": "buy",
    "order_type": "market",
    "qty": 1
  }'
```

**Request (Limit Order):**
```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "asset_type": "stock",
    "side": "buy",
    "order_type": "limit",
    "qty": 1,
    "limit_price": 150.00
  }'
```

**Expected Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "symbol": "AAPL",
  "asset_type": "stock",
  "side": "buy",
  "order_type": "market",
  "qty": 1,
  "filled_qty": 0,
  "status": "pending",
  "submitted_at": "2024-10-05T19:35:00.000Z"
}
```

**Edge Cases to Test:**
1. **Invalid Symbol:**
   ```bash
   # Use non-existent symbol
   # Expected: 400 Bad Request or broker error
   ```

2. **Negative Quantity:**
   ```bash
   # Use qty: -1
   # Expected: 422 Unprocessable Entity
   ```

3. **Limit Order Without Price:**
   ```bash
   # order_type: "limit" but no limit_price
   # Expected: 422 Unprocessable Entity
   ```

4. **Insufficient Buying Power:**
   ```bash
   # Try to buy more than buying_power allows
   # Expected: 400 Bad Request
   ```

**Status:** ⚠️ Requires Alpaca API keys to work fully

---

### 8. Get Orders

**Test:** Retrieve user's order history

**Endpoint:** `GET /api/v1/orders`

**Request:**
```bash
curl http://localhost:8000/api/v1/orders \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "symbol": "AAPL",
    "asset_type": "stock",
    "side": "buy",
    "order_type": "market",
    "qty": 1,
    "filled_qty": 1,
    "status": "filled",
    "submitted_at": "2024-10-05T19:35:00.000Z"
  }
]
```

**Status:** ✅ Should return list of orders

---

### 9. Cancel Order

**Test:** Cancel a pending order

**Endpoint:** `DELETE /api/v1/orders/{order_id}`

**Request:**
```bash
curl -X DELETE http://localhost:8000/api/v1/orders/550e8400-e29b-41d4-a716-446655440000 \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
{
  "message": "Order cancelled successfully"
}
```

**Edge Cases to Test:**
1. **Already Filled Order:**
   ```bash
   # Try to cancel filled order
   # Expected: 400 Bad Request - cannot cancel filled order
   ```

2. **Non-existent Order:**
   ```bash
   # Use invalid order_id
   # Expected: 404 Not Found
   ```

3. **Other User's Order:**
   ```bash
   # Try to cancel order belonging to different user
   # Expected: 403 Forbidden or 404 Not Found
   ```

**Status:** ⚠️ Requires active order to test

---

### 10. Get Positions

**Test:** Retrieve user's current positions

**Endpoint:** `GET /api/v1/positions`

**Request:**
```bash
curl http://localhost:8000/api/v1/positions \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "symbol": "AAPL",
    "asset_type": "stock",
    "qty": 1,
    "avg_price": 150.00,
    "current_price": 155.00,
    "market_value": 155.00,
    "cost_basis": 150.00,
    "unrealized_pl": 5.00,
    "unrealized_pl_percent": 3.33,
    "created_at": "2024-10-05T19:35:00.000Z"
  }
]
```

**Status:** ⚠️ Requires filled orders to have positions

---

### 11. WebSocket Connection

**Test:** Connect to WebSocket for real-time updates

**Endpoint:** `ws://localhost:8000/ws/{user_id}`

**Test with wscat:**
```bash
# Install wscat if not installed
npm install -g wscat

# Connect to WebSocket
wscat -c ws://localhost:8000/ws/1

# Subscribe to symbol
> {"action": "subscribe", "symbol": "AAPL"}

# Expect response
< {"event": "subscribed", "symbol": "AAPL"}

# Receive price updates
< {"event": "price_update", "symbol": "AAPL", "price": 155.23}
```

**Test with Python:**
```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws/1"
    async with websockets.connect(uri) as websocket:
        # Subscribe to symbol
        await websocket.send(json.dumps({
            "action": "subscribe",
            "symbol": "AAPL"
        }))
        
        # Receive messages
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data}")

asyncio.run(test_websocket())
```

**Status:** ⚠️ Requires authentication implementation

---

## Frontend Testing

### 1. Landing Page

**Test:** Verify frontend loads correctly

**URL:** http://localhost:3000

**Expected:**
- Login/Register links visible
- No console errors
- Responsive layout

**Manual Test:**
1. Open http://localhost:3000 in browser
2. Check developer console for errors
3. Verify page renders correctly
4. Test on different screen sizes

**Status:** ✅ Should load without errors

---

### 2. Registration Flow

**Test:** Complete user registration through UI

**Steps:**
1. Go to http://localhost:3000
2. Click "Register" link
3. Fill in form:
   - Username: `uitest`
   - Email: `uitest@example.com`
   - Password: `testpass123`
4. Click "Register" button

**Expected:**
- Form validation works (try invalid email first)
- Success message appears
- Redirect to login or dashboard
- No console errors

**Edge Cases:**
- Try registering with existing username
- Try registering with existing email
- Try short password
- Try invalid email format

**Status:** ✅ Should create account successfully

---

### 3. Login Flow

**Test:** Login with created account

**Steps:**
1. Go to http://localhost:3000/login
2. Enter credentials:
   - Username: `uitest`
   - Password: `testpass123`
3. Click "Login" button

**Expected:**
- Successful login
- Redirect to dashboard
- Token stored in localStorage
- User info loaded

**Verification:**
```javascript
// In browser console
localStorage.getItem('access_token')  // Should show token
```

**Edge Cases:**
- Try wrong password
- Try non-existent username
- Try with empty fields

**Status:** ✅ Should login successfully

---

### 4. Dashboard View

**Test:** View dashboard after login

**URL:** http://localhost:3000/dashboard

**Expected Elements:**
- Portfolio summary card
- Account balance
- Recent activity
- Navigation menu
- Logout button

**Manual Test:**
1. Verify all elements are visible
2. Check portfolio values display
3. Test navigation links
4. Verify logout functionality

**Status:** ✅ Should display dashboard

---

### 5. Trade Page

**Test:** Access trading interface

**URL:** http://localhost:3000/trade

**Steps:**
1. Navigate to Trade page
2. Enter symbol: `AAPL`
3. Select asset type: Stock
4. Select side: Buy
5. Select order type: Market
6. Enter quantity: 1
7. Click "Place Order"

**Expected:**
- Form validation works
- Order submitted successfully
- Success notification appears
- Order appears in order list

**Edge Cases:**
- Try invalid symbol
- Try negative quantity
- Try limit order without price
- Try placing order without funds

**Status:** ⚠️ Requires API keys to work

---

### 6. Portfolio Page

**Test:** View portfolio and positions

**URL:** http://localhost:3000/portfolio

**Expected:**
- List of positions
- P&L calculations
- Current prices
- Performance metrics

**Manual Test:**
1. Navigate to Portfolio page
2. Verify positions display
3. Check P&L calculations
4. Test sorting/filtering (if implemented)

**Status:** ⚠️ Requires positions to display

---

### 7. Orders Page

**Test:** View order history

**URL:** http://localhost:3000/orders

**Expected:**
- List of all orders
- Order status visible
- Cancel button for pending orders
- Order details expandable

**Manual Test:**
1. Navigate to Orders page
2. Verify order list displays
3. Try cancelling pending order
4. Check order filtering

**Status:** ✅ Should display orders

---

### 8. Real-time Updates

**Test:** Verify WebSocket connection and updates

**Steps:**
1. Login to application
2. Open browser DevTools → Network → WS
3. Navigate to Portfolio or Trade page
4. Verify WebSocket connection established
5. Check for price update messages

**Expected:**
- WebSocket connection successful
- Price updates received
- UI updates automatically
- No connection drops

**Status:** ⚠️ Requires WebSocket authentication

---

### 9. Logout

**Test:** User logout functionality

**Steps:**
1. Click "Logout" button
2. Verify redirect to login page
3. Try accessing protected route
4. Check localStorage cleared

**Expected:**
- Redirect to login page
- Token removed from localStorage
- Cannot access protected routes
- No errors in console

**Verification:**
```javascript
// In browser console (after logout)
localStorage.getItem('access_token')  // Should be null
```

**Status:** ✅ Should logout successfully

---

## Integration Testing

### End-to-End User Flow

**Complete Trading Flow:**
1. ✅ Register new account
2. ✅ Login with credentials
3. ✅ View dashboard
4. ⚠️ Fund account (requires external integration)
5. ⚠️ Place market order for stock
6. ⚠️ View order in order history
7. ⚠️ Wait for order to fill
8. ⚠️ View position in portfolio
9. ⚠️ Check P&L calculations
10. ⚠️ Place sell order
11. ✅ Logout

**Status:** Partial - requires API keys for trading

---

## Automated Testing

### Backend Unit Tests

**Run All Tests:**
```bash
cd backend
pytest
```

**Run with Coverage:**
```bash
pytest --cov=app --cov-report=html
```

**Run Specific Test File:**
```bash
pytest tests/test_auth.py -v
```

**Current Tests:**
- `test_auth.py` - Authentication tests
- More tests to be added

**Expected Output:**
```
====================== test session starts ======================
collected 11 items

tests/test_auth.py::test_register_user PASSED              [  9%]
tests/test_auth.py::test_register_duplicate_username PASSED [ 18%]
tests/test_auth.py::test_register_duplicate_email PASSED   [ 27%]
tests/test_auth.py::test_login_success PASSED              [ 36%]
tests/test_auth.py::test_login_wrong_password PASSED       [ 45%]
tests/test_auth.py::test_login_nonexistent_user PASSED     [ 54%]
tests/test_auth.py::test_get_current_user PASSED           [ 63%]
tests/test_auth.py::test_get_current_user_no_token PASSED  [ 72%]
tests/test_auth.py::test_get_current_user_invalid_token PASSED [ 81%]
tests/test_auth.py::test_logout PASSED                     [ 90%]
tests/test_auth.py::test_token_expiration PASSED           [100%]

====================== 11 passed in 2.34s =======================
```

---

### Frontend Unit Tests

**Run All Tests:**
```bash
cd frontend
npm test
```

**Run with Coverage:**
```bash
npm test -- --coverage
```

**Run in Watch Mode:**
```bash
npm test -- --watch
```

**Current Tests:**
- To be implemented

---

## Performance Testing

### Load Testing with Apache Bench

**Test API Endpoint:**
```bash
# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Expected:
# - Requests per second: > 500
# - Time per request: < 20ms
# - No failed requests
```

**Test Login Endpoint:**
```bash
# Create test.json with login credentials
echo '{"username":"testuser","password":"testpass123"}' > test.json

# Run load test
ab -n 100 -c 5 -p test.json -T application/json http://localhost:8000/api/v1/auth/login
```

---

### WebSocket Load Testing

**Test with Artillery:**
```yaml
# websocket-test.yml
config:
  target: "ws://localhost:8000"
  phases:
    - duration: 60
      arrivalRate: 5
scenarios:
  - engine: ws
    flow:
      - connect:
          url: "/ws/1"
      - send:
          payload: '{"action":"subscribe","symbol":"AAPL"}'
      - think: 10
      - send:
          payload: '{"action":"ping"}'
```

```bash
artillery run websocket-test.yml
```

---

## Security Testing

### SQL Injection

**Test:**
```bash
# Try SQL injection in username
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin;DROP TABLE users;--","email":"hack@test.com","password":"pass123"}'

# Expected: Should be safely escaped, no SQL injection
```

### XSS (Cross-Site Scripting)

**Test:**
```bash
# Try XSS in username
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"<script>alert(1)</script>","email":"xss@test.com","password":"pass123"}'

# Expected: Should be sanitized or rejected
```

### JWT Token Tampering

**Test:**
```bash
# Get valid token
TOKEN="valid-token-here"

# Modify token (change one character)
TAMPERED_TOKEN="${TOKEN:0:50}X${TOKEN:51}"

# Try to use tampered token
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TAMPERED_TOKEN"

# Expected: 401 Unauthorized
```

---

## Troubleshooting

### Issue: Backend Won't Start

**Symptoms:**
- Docker container exits immediately
- Connection refused errors

**Solutions:**
1. Check Docker logs:
   ```bash
   docker compose logs backend
   ```

2. Verify environment variables:
   ```bash
   docker compose exec backend env | grep DATABASE_URL
   ```

3. Check database connection:
   ```bash
   docker compose exec db psql -U speedtrade -d speedtrade_db -c "SELECT 1;"
   ```

4. Rebuild containers:
   ```bash
   docker compose down -v
   docker compose up --build
   ```

---

### Issue: Frontend Can't Connect to Backend

**Symptoms:**
- CORS errors in browser console
- Network errors in DevTools

**Solutions:**
1. Verify backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Check CORS configuration in `backend/app/main.py`

3. Verify frontend .env:
   ```bash
   cat frontend/.env
   # Should have: VITE_API_URL=http://localhost:8000
   ```

4. Clear browser cache and reload

---

### Issue: Database Migrations Fail

**Symptoms:**
- Alembic errors
- "relation does not exist" errors

**Solutions:**
1. Check alembic history:
   ```bash
   cd backend
   alembic current
   alembic history
   ```

2. Create initial migration:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

3. Apply migrations:
   ```bash
   alembic upgrade head
   ```

4. If stuck, reset database:
   ```bash
   docker compose down -v
   docker compose up -d db
   # Wait for db to be ready
   alembic upgrade head
   docker compose up backend
   ```

---

### Issue: Tests Fail

**Symptoms:**
- Pytest errors
- Import errors

**Solutions:**
1. Install test dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   pip install pytest pytest-asyncio httpx
   ```

2. Set test environment:
   ```bash
   export DATABASE_URL=sqlite:///./test.db
   export SECRET_KEY=test-secret-key
   ```

3. Run tests with verbose output:
   ```bash
   pytest -vv -s
   ```

---

## Test Checklist

### Before Deployment

**Backend:**
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] No linting errors
- [ ] Database migrations work
- [ ] API documentation generated
- [ ] Environment variables configured
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Error logging configured

**Frontend:**
- [ ] All unit tests passing
- [ ] No console errors
- [ ] Build succeeds
- [ ] All pages load correctly
- [ ] Forms validate correctly
- [ ] API calls work
- [ ] WebSocket connects
- [ ] Authentication works
- [ ] Responsive design works
- [ ] Cross-browser tested

**Integration:**
- [ ] End-to-end flows tested
- [ ] User registration works
- [ ] Login/logout works
- [ ] Order placement works
- [ ] Portfolio updates correctly
- [ ] Real-time updates work
- [ ] Error handling works
- [ ] Performance acceptable

---

## Test Report Template

```markdown
## Test Report

**Date:** YYYY-MM-DD
**Tester:** Name
**Environment:** Local/Staging/Production
**Version:** vX.X.X

### Summary
- Total Tests: XX
- Passed: XX
- Failed: XX
- Skipped: XX

### Failed Tests
1. Test Name
   - Expected: ...
   - Actual: ...
   - Steps to Reproduce: ...

### Performance
- Backend Response Time: Xms avg
- Frontend Load Time: Xs
- WebSocket Latency: Xms

### Issues Found
1. Issue description
   - Severity: High/Medium/Low
   - Status: Open/Fixed

### Recommendations
- Recommendation 1
- Recommendation 2
```

---

## Continuous Integration

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest
  
  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: 18
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm test
```

---

## Conclusion

This testing guide covers:
- ✅ Backend API testing
- ✅ Frontend UI testing
- ✅ Integration testing
- ✅ Performance testing
- ✅ Security testing
- ✅ Troubleshooting guide
- ✅ CI/CD setup

Use this guide as a checklist before each release to ensure SpeedTrade is production-ready.

**Remember:** Testing is ongoing. Add new tests as you add features!

---

**Last Updated:** October 2024  
**Version:** 1.0.0  
**Status:** Comprehensive Guide Complete ✅
