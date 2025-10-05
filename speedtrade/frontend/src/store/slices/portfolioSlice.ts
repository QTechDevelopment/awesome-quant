import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface Position {
  id: number
  symbol: string
  asset_type: string
  quantity: string
  average_entry_price: string
  current_price: string
  current_value: string
  unrealized_pnl: string
  unrealized_pnl_pct: string
}

interface Portfolio {
  user_id: number
  cash_balance: string
  crypto_balance: string
  position_value: string
  total_equity: string
  unrealized_pnl: string
  realized_pnl: string
  total_pnl: string
}

interface PortfolioState {
  portfolio: Portfolio | null
  positions: Position[]
  loading: boolean
  error: string | null
}

const initialState: PortfolioState = {
  portfolio: null,
  positions: [],
  loading: false,
  error: null,
}

const portfolioSlice = createSlice({
  name: 'portfolio',
  initialState,
  reducers: {
    setPortfolio: (state, action: PayloadAction<Portfolio>) => {
      state.portfolio = action.payload
      state.loading = false
      state.error = null
    },
    setPositions: (state, action: PayloadAction<Position[]>) => {
      state.positions = action.payload
      state.loading = false
      state.error = null
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

export const { setPortfolio, setPositions, setLoading, setError } =
  portfolioSlice.actions
export default portfolioSlice.reducer
