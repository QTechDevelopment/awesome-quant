import api from './api'

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  email: string
  username: string
  full_name: string
  password: string
}

export const authService = {
  async login(credentials: LoginCredentials) {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  async register(data: RegisterData) {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me')
    return response.data
  },

  async logout() {
    const response = await api.post('/auth/logout')
    return response.data
  },
}
