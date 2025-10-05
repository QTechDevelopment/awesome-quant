import api from './api'

export const marketService = {
  async getQuote(symbol: string) {
    const response = await api.get(`/market/quote/${symbol}`)
    return response.data
  },

  async searchSymbols(query: string, limit?: number) {
    const response = await api.get('/market/search', {
      params: { query, limit },
    })
    return response.data
  },

  async getChartData(symbol: string, interval: string, period: string) {
    const response = await api.get(`/market/chart/${symbol}`, {
      params: { interval, period },
    })
    return response.data
  },

  async getTopGainers(limit?: number) {
    const response = await api.get('/market/movers/gainers', {
      params: { limit },
    })
    return response.data
  },

  async getTopLosers(limit?: number) {
    const response = await api.get('/market/movers/losers', {
      params: { limit },
    })
    return response.data
  },
}
