import api from './api'

export interface OrderRequest {
  symbol: string
  side: 'buy' | 'sell'
  order_type: 'market' | 'limit' | 'stop' | 'stop_limit'
  quantity: string
  asset_type: 'stock' | 'crypto'
  limit_price?: string
  stop_price?: string
  time_in_force?: 'day' | 'gtc' | 'ioc' | 'fok'
}

export const ordersService = {
  async placeOrder(order: OrderRequest) {
    const response = await api.post('/orders', order)
    return response.data
  },

  async getOrders(status?: string, limit?: number) {
    const response = await api.get('/orders', {
      params: { status, limit },
    })
    return response.data
  },

  async getOrder(orderId: number) {
    const response = await api.get(`/orders/${orderId}`)
    return response.data
  },

  async cancelOrder(orderId: number) {
    const response = await api.delete(`/orders/${orderId}`)
    return response.data
  },
}
