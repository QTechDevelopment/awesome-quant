from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import time
import sys

from app.core.config import settings

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO" if not settings.DEBUG else "DEBUG"
)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="High-speed trading platform for stocks and crypto under $100",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Middleware - CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware - Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Middleware - Request timing
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.3f}"
    
    # Log request
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.3f}s"
    )
    
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        },
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.APP_ENV
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.APP_NAME} API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/health"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 Starting {settings.APP_NAME}")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # TODO: Initialize connections
    # - Database connection pool
    # - Redis connection
    # - Alpaca API client
    logger.info("✅ All connections initialized")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"🛑 Shutting down {settings.APP_NAME}")
    
    # Close trading service connections
    from app.services.trading_service import get_trading_service
    trading_service = get_trading_service()
    await trading_service.close()
    
    logger.info("✅ All connections closed")


# Include API routers
from app.api.v1 import auth, orders, portfolio, market_data
from app.api.websocket import market_stream

app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(orders.router, prefix="/api/v1", tags=["Orders"])
app.include_router(portfolio.router, prefix="/api/v1", tags=["Portfolio"])
app.include_router(market_data.router, prefix="/api/v1", tags=["Market Data"])
app.include_router(market_stream.router, tags=["WebSocket"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
