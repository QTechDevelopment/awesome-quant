import { useEffect } from 'react'
import { useAppSelector, useAppDispatch } from '../hooks/redux'
import { portfolioService } from '../services/portfolioService'
import { ordersService } from '../services/ordersService'
import { setPortfolio, setPositions } from '../store/slices/portfolioSlice'
import { setOrders } from '../store/slices/ordersSlice'
import { TrendingUp, TrendingDown, DollarSign, Activity } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const dispatch = useAppDispatch()
  const { portfolio, positions } = useAppSelector((state) => state.portfolio)
  const { orders } = useAppSelector((state) => state.orders)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [portfolioData, positionsData, ordersData] = await Promise.all([
        portfolioService.getPortfolio(),
        portfolioService.getPositions(),
        ordersService.getOrders({ status: 'filled', limit: 10 }),
      ])

      dispatch(setPortfolio(portfolioData))
      dispatch(setPositions(positionsData))
      dispatch(setOrders(ordersData))
    } catch (error: any) {
      toast.error('Failed to load dashboard data')
    }
  }

  const stats = [
    {
      name: 'Portfolio Value',
      value: portfolio ? `$${portfolio.total_value.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '$0.00',
      icon: DollarSign,
      color: 'bg-primary-500',
    },
    {
      name: 'Day P&L',
      value: portfolio ? `$${portfolio.day_pl.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '$0.00',
      icon: portfolio && portfolio.day_pl >= 0 ? TrendingUp : TrendingDown,
      color: portfolio && portfolio.day_pl >= 0 ? 'bg-success-500' : 'bg-danger-500',
    },
    {
      name: 'Total P&L',
      value: portfolio ? `$${portfolio.total_pl.toLocaleString('en-US', { minimumFractionDigits: 2 })}` : '$0.00',
      icon: portfolio && portfolio.total_pl >= 0 ? TrendingUp : TrendingDown,
      color: portfolio && portfolio.total_pl >= 0 ? 'bg-success-500' : 'bg-danger-500',
    },
    {
      name: 'Active Positions',
      value: positions.length,
      icon: Activity,
      color: 'bg-blue-500',
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Welcome back! Here's your portfolio overview.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.name} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-1">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Positions */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Active Positions</h2>
        {positions.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No active positions</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Symbol</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Quantity</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Avg Cost</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Current Price</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">P&L</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">P&L %</th>
                </tr>
              </thead>
              <tbody>
                {positions.map((position) => (
                  <tr key={position.symbol} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 font-semibold text-gray-900">{position.symbol}</td>
                    <td className="py-3 px-4 text-right text-gray-700">{position.quantity}</td>
                    <td className="py-3 px-4 text-right text-gray-700">${position.average_cost.toFixed(2)}</td>
                    <td className="py-3 px-4 text-right text-gray-700">${position.current_price.toFixed(2)}</td>
                    <td className={`py-3 px-4 text-right font-semibold ${position.unrealized_pl >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                      {position.unrealized_pl >= 0 ? '+' : ''}${position.unrealized_pl.toFixed(2)}
                    </td>
                    <td className={`py-3 px-4 text-right font-semibold ${position.unrealized_pl_percent >= 0 ? 'text-success-600' : 'text-danger-600'}`}>
                      {position.unrealized_pl_percent >= 0 ? '+' : ''}{position.unrealized_pl_percent.toFixed(2)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Recent Orders */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Orders</h2>
        {orders.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No recent orders</p>
        ) : (
          <div className="space-y-3">
            {orders.slice(0, 5).map((order) => (
              <div key={order.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-4">
                  <div className={`px-3 py-1 rounded text-xs font-semibold ${
                    order.side === 'buy' ? 'bg-success-100 text-success-700' : 'bg-danger-100 text-danger-700'
                  }`}>
                    {order.side.toUpperCase()}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">{order.symbol}</p>
                    <p className="text-sm text-gray-600">
                      {order.quantity} shares @ ${order.filled_price?.toFixed(2) || order.limit_price?.toFixed(2) || 'Market'}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`text-sm font-semibold ${
                    order.status === 'filled' ? 'text-success-600' :
                    order.status === 'cancelled' ? 'text-gray-500' :
                    'text-blue-600'
                  }`}>
                    {order.status.toUpperCase()}
                  </p>
                  <p className="text-xs text-gray-500">{new Date(order.created_at).toLocaleString()}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
