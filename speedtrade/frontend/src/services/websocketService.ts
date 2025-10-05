import { io, Socket } from 'socket.io-client'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

class WebSocketService {
  private socket: Socket | null = null
  private token: string | null = null

  connect(token: string) {
    this.token = token
    this.socket = io(WS_URL, {
      query: { token },
      transports: ['websocket'],
    })

    this.socket.on('connect', () => {
      console.log('WebSocket connected')
    })

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected')
    })

    this.socket.on('error', (error) => {
      console.error('WebSocket error:', error)
    })

    return this.socket
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect()
      this.socket = null
    }
  }

  subscribe(symbols: string[]) {
    if (this.socket) {
      this.socket.emit('subscribe', { symbols })
    }
  }

  unsubscribe(symbols: string[]) {
    if (this.socket) {
      this.socket.emit('unsubscribe', { symbols })
    }
  }

  onQuote(callback: (data: any) => void) {
    if (this.socket) {
      this.socket.on('quote', callback)
    }
  }

  offQuote(callback?: (data: any) => void) {
    if (this.socket) {
      this.socket.off('quote', callback)
    }
  }

  isConnected() {
    return this.socket?.connected || false
  }
}

export const websocketService = new WebSocketService()
