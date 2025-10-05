import { io, Socket } from 'socket.io-client';

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

class WebSocketService {
  private socket: Socket | null = null;
  private userId: number | null = null;

  connect(userId: number) {
    if (this.socket?.connected) {
      return;
    }

    this.userId = userId;
    this.socket = io(WS_URL, {
      transports: ['websocket'],
      path: `/ws/${userId}`,
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error);
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  subscribe(symbol: string) {
    if (this.socket?.connected) {
      this.socket.emit('message', JSON.stringify({
        action: 'subscribe',
        symbol: symbol,
      }));
    }
  }

  unsubscribe(symbol: string) {
    if (this.socket?.connected) {
      this.socket.emit('message', JSON.stringify({
        action: 'unsubscribe',
        symbol: symbol,
      }));
    }
  }

  onPriceUpdate(callback: (data: any) => void) {
    if (this.socket) {
      this.socket.on('price_update', callback);
    }
  }

  onOrderUpdate(callback: (data: any) => void) {
    if (this.socket) {
      this.socket.on('order_update', callback);
    }
  }

  onPortfolioUpdate(callback: (data: any) => void) {
    if (this.socket) {
      this.socket.on('portfolio_update', callback);
    }
  }

  removeListener(event: string) {
    if (this.socket) {
      this.socket.off(event);
    }
  }
}

export const websocketService = new WebSocketService();
