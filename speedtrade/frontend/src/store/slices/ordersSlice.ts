import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface Order {
  id: number
  symbol: string
  side: string
  type: string
  quantity: string
  filled_quantity: string
  limit_price?: string
  stop_price?: string
  filled_avg_price?: string
  status: string
  asset_type: string
  created_at: string
  submitted_at?: string
  filled_at?: string
  cancelled_at?: string
}

interface OrdersState {
  orders: Order[]
  loading: boolean
  error: string | null
}

const initialState: OrdersState = {
  orders: [],
  loading: false,
  error: null,
}

const ordersSlice = createSlice({
  name: 'orders',
  initialState,
  reducers: {
    setOrders: (state, action: PayloadAction<Order[]>) => {
      state.orders = action.payload
      state.loading = false
      state.error = null
    },
    addOrder: (state, action: PayloadAction<Order>) => {
      state.orders.unshift(action.payload)
    },
    updateOrder: (state, action: PayloadAction<Order>) => {
      const index = state.orders.findIndex(
        (order) => order.id === action.payload.id
      )
      if (index !== -1) {
        state.orders[index] = action.payload
      }
    },
    removeOrder: (state, action: PayloadAction<number>) => {
      state.orders = state.orders.filter((order) => order.id !== action.payload)
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload
      state.loading = false
    },
  },
})

export const {
  setOrders,
  addOrder,
  updateOrder,
  removeOrder,
  setLoading,
  setError,
} = ordersSlice.actions
export default ordersSlice.reducer
