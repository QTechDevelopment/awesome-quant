import api from './api';
import type { Order, CreateOrderData, Position, Portfolio } from '../types';

export const tradingService = {
  // Orders
  createOrder: async (data: CreateOrderData): Promise<Order> => {
    const response = await api.post<Order>('/orders', data);
    return response.data;
  },

  getOrders: async (status?: string, symbol?: string): Promise<Order[]> => {
    const params = new URLSearchParams();
    if (status) params.append('status', status);
    if (symbol) params.append('symbol', symbol);
    
    const response = await api.get<Order[]>(`/orders?${params.toString()}`);
    return response.data;
  },

  getOrder: async (orderId: number): Promise<Order> => {
    const response = await api.get<Order>(`/orders/${orderId}`);
    return response.data;
  },

  cancelOrder: async (orderId: number): Promise<void> => {
    await api.delete(`/orders/${orderId}`);
  },

  // Portfolio
  getPortfolio: async (): Promise<Portfolio> => {
    const response = await api.get<Portfolio>('/portfolio');
    return response.data;
  },

  // Positions
  getPositions: async (): Promise<Position[]> => {
    const response = await api.get<Position[]>('/positions');
    return response.data;
  },

  getPosition: async (symbol: string): Promise<Position> => {
    const response = await api.get<Position>(`/positions/${symbol}`);
    return response.data;
  },
};
