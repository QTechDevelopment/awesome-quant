import { useAppSelector, useAppDispatch } from '../../hooks/redux'
import { logout } from '../../store/slices/authSlice'
import { useNavigate } from 'react-router-dom'
import { LogOut, User, TrendingUp } from 'lucide-react'

export default function Header() {
  const { user } = useAppSelector((state) => state.auth)
  const { portfolio } = useAppSelector((state) => state.portfolio)
  const dispatch = useAppDispatch()
  const navigate = useNavigate()

  const handleLogout = () => {
    dispatch(logout())
    navigate('/login')
  }

  return (
    <header className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 z-40 h-16">
      <div className="flex items-center justify-between h-full px-6">
        {/* Logo */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-10 h-10 bg-primary-600 rounded-lg">
            <TrendingUp className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-bold text-gray-900">SpeedTrade</span>
        </div>

        {/* Portfolio Value */}
        {portfolio && (
          <div className="flex items-center space-x-8">
            <div>
              <p className="text-sm text-gray-500">Portfolio Value</p>
              <p className="text-lg font-bold text-gray-900">
                ${portfolio.total_value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Buying Power</p>
              <p className="text-lg font-bold text-gray-900">
                ${portfolio.buying_power.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Today's P&L</p>
              <p className={`text-lg font-bold ${portfolio.day_pl >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                {portfolio.day_pl >= 0 ? '+' : ''}${portfolio.day_pl.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </p>
            </div>
          </div>
        )}

        {/* User Menu */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-primary-600" />
            </div>
            <span className="text-sm font-medium text-gray-700">{user?.username}</span>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </header>
  )
}
