from fastapi import APIRouter
from app.api.v1.endpoints import auth, orders, portfolio, positions, watchlist

api_router = APIRouter()

# Include authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Include trading routes
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
api_router.include_router(positions.router, prefix="/positions", tags=["positions"])
api_router.include_router(watchlist.router, prefix="/watchlist", tags=["watchlist"])
