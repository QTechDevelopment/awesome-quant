import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface User {
  id: number
  email: string
  username: string
  full_name: string
  kyc_status: string
  account_type: string
  account_status: string
}

interface AuthState {
  user: User | null
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  loading: boolean
  error: string | null
}

const initialState: AuthState = {
  user: null,
  accessToken: localStorage.getItem('accessToken'),
  refreshToken: localStorage.getItem('refreshToken'),
  isAuthenticated: !!localStorage.getItem('accessToken'),
  loading: false,
  error: null,
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    loginStart: (state) => {
      state.loading = true
      state.error = null
    },
    loginSuccess: (
      state,
      action: PayloadAction<{
        user: User
        accessToken: string
        refreshToken: string
      }>
    ) => {
      state.loading = false
      state.isAuthenticated = true
      state.user = action.payload.user
      state.accessToken = action.payload.accessToken
      state.refreshToken = action.payload.refreshToken
      state.error = null
      localStorage.setItem('accessToken', action.payload.accessToken)
      localStorage.setItem('refreshToken', action.payload.refreshToken)
    },
    loginFailure: (state, action: PayloadAction<string>) => {
      state.loading = false
      state.error = action.payload
    },
    logout: (state) => {
      state.user = null
      state.accessToken = null
      state.refreshToken = null
      state.isAuthenticated = false
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
    },
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload
    },
  },
})

export const { loginStart, loginSuccess, loginFailure, logout, setUser } =
  authSlice.actions
export default authSlice.reducer
