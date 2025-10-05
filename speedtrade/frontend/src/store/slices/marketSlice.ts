import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface Quote {
  symbol: string
  bid_price: string
  ask_price: string
  last_price: string
  high: string
  low: string
  open: string
  volume: number
  change: string
  change_percent: string
  timestamp: string
}

interface MarketState {
  quotes: Record<string, Quote>
  selectedSymbol: string | null
  loading: boolean
  error: string | null
}

const initialState: MarketState = {
  quotes: {},
  selectedSymbol: null,
  loading: false,
  error: null,
}

const marketSlice = createSlice({
  name: 'market',
  initialState,
  reducers: {
    setQuote: (state, action: PayloadAction<Quote>) => {
      state.quotes[action.payload.symbol] = action.payload
    },
    setQuotes: (state, action: PayloadAction<Record<string, Quote>>) => {
      state.quotes = action.payload
    },
    updateQuote: (state, action: PayloadAction<Quote>) => {
      const symbol = action.payload.symbol
      if (state.quotes[symbol]) {
        state.quotes[symbol] = action.payload
      }
    },
    setSelectedSymbol: (state, action: PayloadAction<string | null>) => {
      state.selectedSymbol = action.payload
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
  setQuote,
  setQuotes,
  updateQuote,
  setSelectedSymbol,
  setLoading,
  setError,
} = marketSlice.actions
export default marketSlice.reducer
