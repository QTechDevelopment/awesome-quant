import { useEffect } from 'react'
import { useAppSelector, useAppDispatch } from '../hooks/redux'
import { portfolioService } from '../services/portfolioService'
import { setPortfolio, setPositions } from '../store/slices/portfolioSlice'
import { TrendingUp, TrendingDown } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Portfolio() {
  const dispatch = useAppDispatch()
  const { portfolio, positions } = useAppSelector((state) => state.portfolio)

  useEffect(() => {
    loadPortfolioData()
  }, [])

  const loadPortfolioData = async () => {
    try {
      const [portfolioData, positionsData] = await Promise.all([
        portfolioService.getPortfolio(),
        portfolioService.getPositions(),
      ])
      dispatch(setPortfolio(portfolioData))
      dispatch(setPositions(positionsData))
    } catch (error: any) {
      toast.error('Failed to load portfolio data')
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Portfolio</h1>
        <button
          onClick={loadPortfolioData}
          className="btn-secondary"
        >
          Refresh
        </button>
      </div>

      {/* Portfolio Summary */}
      {portfolio && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card">
            <p className="text-sm text-gray-600 mb-2">Total Value</p>
            <p className="text-3xl font-bold text-gray-900">
              ${portfolio.total_value.toLocaleString('en-US', { minimumFractionDigits: 2 })}
            </p>
          </div>
          
          <div className="card">
            <p className="text-sm text-gray-600 mb-2">Cash Balance</p>
            <p className="text-3xl font-bold text-gray-900">
              ${portfolio.cash_balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}
            </p>
          </div>

          <div className="card">
            <p className="text-sm text-gray-600 mb-2">Total P&L</p>
            <p className={`text-3xl font-bold ${
              portfolio.total_pl >= 0 ? 'text-success-600' : 'text-danger-600'
            }`}>
              {portfolio.total_pl >= 0 ? '+' : ''}${portfolio.total_pl.toLocaleString('en-US', { minimumFractionDigits: 2 })}
            </p>
            <p className={`text-sm font-semibold mt-1 ${
              portfolio.total_pl_percent >= 0 ? 'text-success-600' : 'text-danger-600'
            }`}>
              {portfolio.total_pl_percent >= 0 ? '+' : ''}{portfolio.total_pl_percent.toFixed(2)}%
            </p>
          </div>
        </div>
      )}

      {/* Positions Table */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Positions</h2>
        
        {positions.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">No positions yet</p>
            <a href="/trade" className="btn-primary">
              Start Trading
            </a>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Symbol</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Quantity</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Avg Cost</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Current Price</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Market Value</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Total P&L</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">P&L %</th>
                  <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">Day P&L</th>
                </tr>
              </thead>
              <tbody>
                {positions.map((position) => (
                  <tr key={position.symbol} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-4 px-4">
                      <div>
                        <p className="font-bold text-gray-900">{position.symbol}</p>
                        <p className="text-xs text-gray-500">{position.asset_class}</p>
                      </div>
                    </td>
                    <td className="py-4 px-4 text-right text-gray-700">
                      {position.quantity}
                    </td>
                    <td className="py-4 px-4 text-right text-gray-700">
                      ${position.average_cost.toFixed(2)}
                    </td>
                    <td className="py-4 px-4 text-right text-gray-700">
                      ${position.current_price.toFixed(2)}
                    </td>
                    <td className="py-4 px-4 text-right font-semibold text-gray-900">
                      ${position.market_value.toFixed(2)}
                    </td>
                    <td className={`py-4 px-4 text-right font-semibold ${
                      position.unrealized_pl >= 0 ? 'text-success-600' : 'text-danger-600'
                    }`}>
                      <div className="flex items-center justify-end">
                        {position.unrealized_pl >= 0 ? (
                          <TrendingUp className="w-4 h-4 mr-1" />
                        ) : (
                          <TrendingDown className="w-4 h-4 mr-1" />
                        )}
                        {position.unrealized_pl >= 0 ? '+' : ''}${position.unrealized_pl.toFixed(2)}
                      </div>
                    </td>
                    <td className={`py-4 px-4 text-right font-semibold ${
                      position.unrealized_pl_percent >= 0 ? 'text-success-600' : 'text-danger-600'
                    }`}>
                      {position.unrealized_pl_percent >= 0 ? '+' : ''}{position.unrealized_pl_percent.toFixed(2)}%
                    </td>
                    <td className={`py-4 px-4 text-right font-semibold ${
                      position.day_pl >= 0 ? 'text-success-600' : 'text-danger-600'
                    }`}>
                      {position.day_pl >= 0 ? '+' : ''}${position.day_pl.toFixed(2)}
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
