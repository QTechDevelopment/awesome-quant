import api from './api'

export const portfolioService = {
  async getPortfolio() {
    const response = await api.get('/portfolio')
    return response.data
  },

  async getPositions(assetType?: string) {
    const response = await api.get('/portfolio/positions', {
      params: { asset_type: assetType },
    })
    return response.data
  },

  async getPosition(symbol: string) {
    const response = await api.get(`/portfolio/positions/${symbol}`)
    return response.data
  },
}
