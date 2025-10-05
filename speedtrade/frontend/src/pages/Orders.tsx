import { useEffect, useState } from 'react'
import { useAppSelector, useAppDispatch } from '../hooks/redux'
import { ordersService } from '../services/ordersService'
import { setOrders } from '../store/slices/ordersSlice'
import { XCircle } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Orders() {
  const dispatch = useAppDispatch()
  const { orders } = useAppSelector((state) => state.orders)
  const [filter, setFilter] = useState<string>('all')
  const [cancelling, setCancelling] = useState<string | null>(null)

  useEffect(() => {
    loadOrders()
  }, [filter])

  const loadOrders = async () => {
    try {
      const params = filter !== 'all' ? { status: filter } : {}
      const ordersData = await ordersService.getOrders(params)
      dispatch(setOrders(ordersData))
    } catch (error: any) {
      toast.error('Failed to load orders')
    }
  }

  const handleCancelOrder = async (orderId: string) => {
    setCancelling(orderId)
    try {
      await ordersService.cancelOrder(orderId)
      toast.success('Order cancelled')
      loadOrders()
    } catch (error: any) {
      toast.error('Failed to cancel order')
    } finally {
      setCancelling(null)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'filled':
        return 'bg-success-100 text-success-700'
      case 'cancelled':
      case 'rejected':
        return 'bg-gray-100 text-gray-700'
      case 'pending':
        return 'bg-blue-100 text-blue-700'
      case 'partially_filled':
        return 'bg-yellow-100 text-yellow-700'
      default:
        return 'bg-gray-100 text-gray-700'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Orders</h1>
        <button onClick={loadOrders} className="btn-secondary">
          Refresh
        </button>
      </div>

      {/* Filter Tabs */}
      <div className="flex space-x-2 border-b border-gray-200">
        {['all', 'pending', 'filled', 'cancelled'].map((tab) => (
          <button
            key={tab}
            onClick={() => setFilter(tab)}
            className={`px-4 py-2 font-medium capitalize ${
              filter === tab
                ? 'text-primary-600 border-b-2 border-primary-600'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Orders Table */}
      <div className="card">
        {orders.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">No orders found</p>
            <a href="/trade" className="btn-primary">
              Place an Order
            </a>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Date</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Symbol</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Side</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Type</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Quantity</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Limit Price</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Filled Price</th>
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Status</th>
                  <th className="text-center py-3 px-4 text-sm font-semibold text-gray-700">Action</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((order) => (
                  <tr key={order.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-4 px-4 text-sm text-gray-700">
                      {new Date(order.created_at).toLocaleString()}
                    </td>
                    <td className="py-4 px-4 font-semibold text-gray-900">
                      {order.symbol}
                    </td>
                    <td className="py-4 px-4">
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${
                        order.side === 'buy'
                          ? 'bg-success-100 text-success-700'
                          : 'bg-danger-100 text-danger-700'
                      }`}>
                        {order.side.toUpperCase()}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-sm text-gray-700 capitalize">
                      {order.type}
                    </td>
                    <td className="py-4 px-4 text-right text-gray-700">
                      {order.quantity}
                    </td>
                    <td className="py-4 px-4 text-right text-gray-700">
                      {order.limit_price ? `$${order.limit_price.toFixed(2)}` : '-'}
                    </td>
                    <td className="py-4 px-4 text-right font-semibold text-gray-900">
                      {order.filled_price ? `$${order.filled_price.toFixed(2)}` : '-'}
                    </td>
                    <td className="py-4 px-4">
                      <span className={`px-2 py-1 rounded text-xs font-semibold ${getStatusColor(order.status)}`}>
                        {order.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-center">
                      {order.status === 'pending' && (
                        <button
                          onClick={() => handleCancelOrder(order.id)}
                          disabled={cancelling === order.id}
                          className="text-danger-600 hover:text-danger-700 disabled:opacity-50"
                        >
                          <XCircle className="w-5 h-5" />
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
