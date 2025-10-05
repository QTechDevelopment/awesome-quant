from fastapi import WebSocket, WebSocketDisconnect
from app.websocket.manager import manager
import json


async def handle_websocket(websocket: WebSocket, user_id: int):
    """Handle WebSocket connection for a user"""
    
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            action = message.get('action')
            
            if action == 'subscribe':
                # Subscribe to symbol updates
                symbol = message.get('symbol')
                if symbol:
                    manager.subscribe(user_id, symbol)
                    await websocket.send_json({
                        'event': 'subscribed',
                        'symbol': symbol
                    })
            
            elif action == 'unsubscribe':
                # Unsubscribe from symbol updates
                symbol = message.get('symbol')
                if symbol:
                    manager.unsubscribe(user_id, symbol)
                    await websocket.send_json({
                        'event': 'unsubscribed',
                        'symbol': symbol
                    })
            
            elif action == 'ping':
                # Respond to ping to keep connection alive
                await websocket.send_json({'event': 'pong'})
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except Exception as e:
        print(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(user_id)
