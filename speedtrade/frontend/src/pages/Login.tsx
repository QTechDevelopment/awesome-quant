import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAppDispatch } from '../hooks/redux'
import { loginStart, loginSuccess, loginFailure } from '../store/slices/authSlice'
import { authService } from '../services/authService'
import toast from 'react-hot-toast'
import { TrendingUp } from 'lucide-react'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const dispatch = useAppDispatch()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!email || !password) {
      toast.error('Please fill in all fields')
      return
    }

    setLoading(true)
    dispatch(loginStart())

    try {
      const response = await authService.login({
        username: email,
        password,
      })

      const user = await authService.getCurrentUser()

      dispatch(
        loginSuccess({
          user,
          accessToken: response.access_token,
          refreshToken: response.refresh_token,
        })
      )

      toast.success('Welcome back!')
      navigate('/dashboard')
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Login failed'
      dispatch(loginFailure(message))
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-800 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Logo & Title */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-white rounded-full mb-4">
            <TrendingUp className="w-8 h-8 text-primary-600" />
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">SpeedTrade</h1>
          <p className="text-primary-100">Trade at the speed of light</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Welcome Back</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email / Username
              </label>
              <input
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="input"
                placeholder="Enter your email or username"
                disabled={loading}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input"
                placeholder="Enter your password"
                disabled={loading}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-3 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-600">
              Don't have an account?{' '}
              <Link to="/register" className="text-primary-600 hover:text-primary-700 font-medium">
                Sign up
              </Link>
            </p>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-primary-100 text-sm mt-6">
          Paper trading mode • Risk-free environment
        </p>
      </div>
    </div>
  )
}
