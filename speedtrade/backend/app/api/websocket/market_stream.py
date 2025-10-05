"""
WebSocket endpoint for real-time market data streaming.
"""
from typing import Set, Dict
import asyncio
import json
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from loguru import logger

from app.core.security import decode_token
from app.services.market_data_service import get_market_data_service


router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections and broadcasting."""
    
    def __init__(self):
        # Map of symbol -> set of websocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        # Map of websocket -> set of subscribed symbols
        self.subscriptions: Dict[WebSocket, Set[str]] = {}
    
    async def connect(self, websocket: WebSocket):
        """Accept WebSocket connection."""
        await websocket.accept()
        self.subscriptions[websocket] = set()
        logger.info(f"WebSocket connected: {websocket.client}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection and its subscriptions."""
        if websocket in self.subscriptions:
            # Remove from all symbol subscriptions
            for symbol in self.subscriptions[websocket]:
                if symbol in self.active_connections:
                    self.active_connections[symbol].discard(websocket)
                    if not self.active_connections[symbol]:
                        del self.active_connections[symbol]
            
            del self.subscriptions[websocket]
        
        logger.info(f"WebSocket disconnected: {websocket.client}")
    
    def subscribe(self, websocket: WebSocket, symbol: str):
        """Subscribe a connection to a symbol."""
        if symbol not in self.active_connections:
            self.active_connections[symbol] = set()
        
        self.active_connections[symbol].add(websocket)
        self.subscriptions[websocket].add(symbol)
        
        logger.info(f"Subscribed {websocket.client} to {symbol}")
    
    def unsubscribe(self, websocket: WebSocket, symbol: str):
        """Unsubscribe a connection from a symbol."""
        if symbol in self.active_connections:
            self.active_connections[symbol].discard(websocket)
            if not self.active_connections[symbol]:
                del self.active_connections[symbol]
        
        if websocket in self.subscriptions:
            self.subscriptions[websocket].discard(symbol)
        
        logger.info(f"Unsubscribed {websocket.client} from {symbol}")
    
    async def broadcast_to_symbol(self, symbol: str, message: dict):
        """Broadcast message to all connections subscribed to a symbol."""
        if symbol not in self.active_connections:
            return
        
        disconnected = []
        for connection in self.active_connections[symbol]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Failed to send to {connection.client}: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()


async def get_current_user_from_ws(token: str) -> int:
    """Authenticate WebSocket connection via token."""
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        return user_id
    except Exception:
        raise ValueError("Invalid authentication token")


@router.websocket("/ws/market")
async def websocket_market_data(
    websocket: WebSocket,
    token: str = Query(..., description="JWT access token")
):
    """
    WebSocket endpoint for real-time market data.
    
    Authentication:
    - Connect with ?token=<jwt_access_token>
    
    Message Format (Client -> Server):
    {
        "action": "subscribe" | "unsubscribe",
        "symbols": ["AAPL", "BTC/USD", ...]
    }
    
    Message Format (Server -> Client):
    {
        "type": "quote",
        "symbol": "AAPL",
        "data": {
            "bid": 150.00,
            "ask": 150.05,
            "last": 150.02,
            "change": 1.5,
            "change_percent": 1.01,
            "timestamp": "2024-01-15T10:30:00Z"
        }
    }
    """
    try:
        # Authenticate user
        user_id = await get_current_user_from_ws(token)
        logger.info(f"User {user_id} connecting to WebSocket")
    except ValueError as e:
        await websocket.close(code=1008, reason=str(e))
        return
    
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            action = data.get("action")
            symbols = data.get("symbols", [])
            
            if action == "subscribe":
                for symbol in symbols:
                    manager.subscribe(websocket, symbol)
                
                await websocket.send_json({
                    "type": "subscribed",
                    "symbols": symbols
                })
            
            elif action == "unsubscribe":
                for symbol in symbols:
                    manager.unsubscribe(websocket, symbol)
                
                await websocket.send_json({
                    "type": "unsubscribed",
                    "symbols": symbols
                })
            
            elif action == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.utcnow().isoformat()
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"User {user_id} disconnected from WebSocket")
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


async def price_update_broadcaster():
    """
    Background task to fetch and broadcast price updates.
    This should be started when the app starts.
    """
    market_service = get_market_data_service()
    
    while True:
        try:
            # Get all subscribed symbols
            symbols = list(manager.active_connections.keys())
            
            if not symbols:
                await asyncio.sleep(1)
                continue
            
            # Fetch quotes for all subscribed symbols
            for symbol in symbols:
                try:
                    quote = await market_service.get_quote(symbol)
                    
                    # Broadcast to all subscribers
                    await manager.broadcast_to_symbol(symbol, {
                        "type": "quote",
                        "symbol": symbol,
                        "data": {
                            "bid": float(quote.bid_price),
                            "ask": float(quote.ask_price),
                            "last": float(quote.last_price),
                            "high": float(quote.high),
                            "low": float(quote.low),
                            "volume": quote.volume,
                            "change": float(quote.change),
                            "change_percent": float(quote.change_percent),
                            "timestamp": quote.timestamp.isoformat()
                        }
                    })
                
                except Exception as e:
                    logger.error(f"Failed to fetch quote for {symbol}: {e}")
            
            # Update every second (adjust based on rate limits)
            await asyncio.sleep(1)
        
        except Exception as e:
            logger.error(f"Price broadcaster error: {e}")
            await asyncio.sleep(5)
