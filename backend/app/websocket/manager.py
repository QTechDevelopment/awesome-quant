from fastapi import WebSocket
from typing import Dict, Set
import asyncio
import json


class ConnectionManager:
    """WebSocket connection manager for real-time updates"""
    
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.subscriptions: Dict[str, Set[int]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
    
    def disconnect(self, user_id: int):
        """Disconnect a user and remove all their subscriptions"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Remove from all subscriptions
        for symbol in self.subscriptions:
            self.subscriptions[symbol].discard(user_id)
    
    def subscribe(self, user_id: int, symbol: str):
        """Subscribe a user to price updates for a symbol"""
        if symbol not in self.subscriptions:
            self.subscriptions[symbol] = set()
        self.subscriptions[symbol].add(user_id)
    
    def unsubscribe(self, user_id: int, symbol: str):
        """Unsubscribe a user from price updates for a symbol"""
        if symbol in self.subscriptions:
            self.subscriptions[symbol].discard(user_id)
    
    async def broadcast_price_update(self, symbol: str, data: dict):
        """Broadcast price update to all subscribed users"""
        if symbol not in self.subscriptions:
            return
        
        disconnected_users = []
        
        for user_id in self.subscriptions[symbol]:
            if user_id in self.active_connections:
                websocket = self.active_connections[user_id]
                try:
                    await websocket.send_json({
                        'event': 'price_update',
                        'data': data
                    })
                except Exception as e:
                    print(f"Error sending to user {user_id}: {e}")
                    disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            self.disconnect(user_id)
    
    async def send_personal_message(self, user_id: int, message: dict):
        """Send a message to a specific user"""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"Error sending personal message to user {user_id}: {e}")
                self.disconnect(user_id)
    
    async def broadcast_order_update(self, user_id: int, order_data: dict):
        """Send order update to a specific user"""
        await self.send_personal_message(user_id, {
            'event': 'order_update',
            'data': order_data
        })
    
    async def broadcast_portfolio_update(self, user_id: int, portfolio_data: dict):
        """Send portfolio update to a specific user"""
        await self.send_personal_message(user_id, {
            'event': 'portfolio_update',
            'data': portfolio_data
        })


# Global connection manager instance
manager = ConnectionManager()
