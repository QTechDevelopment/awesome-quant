// User types
export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

// Order types
export enum OrderSide {
  BUY = 'buy',
  SELL = 'sell',
}

export enum OrderType {
  MARKET = 'market',
  LIMIT = 'limit',
  STOP = 'stop',
  STOP_LIMIT = 'stop_limit',
}

export enum OrderStatus {
  PENDING = 'pending',
  OPEN = 'open',
  FILLED = 'filled',
  PARTIALLY_FILLED = 'partially_filled',
  CANCELLED = 'cancelled',
  REJECTED = 'rejected',
}

export interface Order {
  id: number;
  user_id: number;
  symbol: string;
  side: OrderSide;
  order_type: OrderType;
  quantity: number;
  limit_price?: number;
  stop_price?: number;
  filled_price?: number;
  filled_quantity: number;
  status: OrderStatus;
  external_order_id?: string;
  created_at: string;
  updated_at?: string;
  filled_at?: string;
}

export interface CreateOrderData {
  symbol: string;
  side: OrderSide;
  order_type: OrderType;
  quantity: number;
  limit_price?: number;
  stop_price?: number;
}

// Position types
export interface Position {
  id: number;
  user_id: number;
  symbol: string;
  quantity: number;
  average_entry_price: number;
  current_price?: number;
  market_value?: number;
  cost_basis: number;
  unrealized_pl: number;
  unrealized_pl_percent: number;
  asset_type: string;
  created_at: string;
  updated_at?: string;
}

// Portfolio types
export interface Portfolio {
  id: number;
  user_id: number;
  cash_balance: number;
  buying_power: number;
  portfolio_value: number;
  long_market_value: number;
  short_market_value: number;
  total_pl: number;
  total_pl_percent: number;
  day_pl: number;
  day_pl_percent: number;
  created_at: string;
  updated_at?: string;
}

// WebSocket message types
export interface WSMessage {
  event: string;
  data?: any;
}

export interface PriceUpdate {
  symbol: string;
  price: number;
  change: number;
  change_percent: number;
  timestamp: string;
}
