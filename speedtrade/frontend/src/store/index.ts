import { configureStore } from '@reduxjs/toolkit'
import authReducer from './slices/authSlice'
import portfolioReducer from './slices/portfolioSlice'
import marketReducer from './slices/marketSlice'
import ordersReducer from './slices/ordersSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    portfolio: portfolioReducer,
    market: marketReducer,
    orders: ordersReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
