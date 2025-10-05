import { useState, useEffect } from 'react'
import { useAppSelector, useAppDispatch } from '../hooks/redux'
import { marketService } from '../services/marketService'
import { ordersService } from '../services/ordersService'
import { portfolioService } from '../services/portfolioService'
import { setQuote, setSelectedSymbol } from '../store/slices/marketSlice'
import { addOrder } from '../store/slices/ordersSlice'
import { setPortfolio, setPositions } from '../store/slices/portfolioSlice'
import { Search, TrendingUp, TrendingDown } from 'lucide-react'
import toast from 'react-hot-toast'

type OrderSide = 'buy' | 'sell'
type OrderType = 'market' | 'limit'

export default function Trade() {
  const dispatch = useAppDispatch()
  const { selectedSymbol, quotes } = useAppSelector((state) => state.market)
  const { portfolio } = useAppSelector((state) => state.portfolio)
  
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState<any[]>([])
  const [side, setSide] = useState<OrderSide>('buy')
  const [orderType, setOrderType] = useState<OrderType>('market')
  const [quantity, setQuantity] = useState('')
  const [limitPrice, setLimitPrice] = useState('')
  const [loading, setLoading] = useState(false)

  const currentQuote = selectedSymbol ? quotes[selectedSymbol] : null

  useEffect(() => {
    if (searchQuery.length >= 2) {
      searchSymbols()
    } else {
      setSearchResults([])
    }
  }, [searchQuery])

  useEffect(() => {
    if (selectedSymbol) {
      loadQuote(selectedSymbol)
    }
  }, [selectedSymbol])

  const searchSymbols = async () => {
    try {
      const results = await marketService.searchSymbols(searchQuery)
      setSearchResults(results.slice(0, 5))
    } catch (error) {
      console.error('Search failed:', error)
    }
  }

  const loadQuote = async (symbol: string) => {
    try {
      const quote = await marketService.getQuote(symbol)
      dispatch(setQuote(quote))
    } catch (error: any) {
      toast.error(`Failed to load quote for ${symbol}`)
    }
  }

  const selectSymbol = (symbol: string) => {
    dispatch(setSelectedSymbol(symbol))
    setSearchQuery('')
    setSearchResults([])
  }

  const calculateEstimatedCost = () => {
    if (!quantity || isNaN(parseFloat(quantity))) return 0
    
    const qty = parseFloat(quantity)
    let price = 0

    if (orderType === 'market' && currentQuote) {
      price = side === 'buy' ? currentQuote.ask : currentQuote.bid
    } else if (orderType === 'limit' && limitPrice) {
      price = parseFloat(limitPrice)
    }

    return qty * price
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!selectedSymbol) {
      toast.error('Please select a symbol')
      return
    }

    if (!quantity || parseFloat(quantity) <= 0) {
      toast.error('Please enter a valid quantity')
      return
    }

    if (orderType === 'limit' && (!limitPrice || parseFloat(limitPrice) <= 0)) {
      toast.error('Please enter a valid limit price')
      return
    }

    const estimatedCost = calculateEstimatedCost()
    if (side === 'buy' && portfolio && estimatedCost > portfolio.buying_power) {
      toast.error('Insufficient buying power')
      return
    }

    setLoading(true)

    try {
      const orderData = {
        symbol: selectedSymbol,
        quantity: parseFloat(quantity),
        side,
        type: orderType,
        ...(orderType === 'limit' && { limit_price: parseFloat(limitPrice) }),
      }

      const order = await ordersService.placeOrder(orderData)
      dispatch(addOrder(order))
      toast.success(`${side.toUpperCase()} order placed successfully!`)

      // Refresh portfolio
      const [portfolioData, positionsData] = await Promise.all([
        portfolioService.getPortfolio(),
        portfolioService.getPositions(),
      ])
      dispatch(setPortfolio(portfolioData))
      dispatch(setPositions(positionsData))

      // Reset form
      setQuantity('')
      setLimitPrice('')
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Failed to place order'
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Trade</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Order Form */}
        <div className="lg:col-span-2 space-y-6">
          {/* Symbol Search */}
          <div className="card">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Select Symbol</h2>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value.toUpperCase())}
                placeholder="Search stocks or crypto (e.g., AAPL, BTC)"
                className="input pl-10"
              />
              
              {/* Search Results */}
              {searchResults.length > 0 && (
                <div className="absolute z-10 w-full mt-2 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                  {searchResults.map((result) => (
                    <button
                      key={result.symbol}
                      onClick={() => selectSymbol(result.symbol)}
                      className="w-full px-4 py-3 text-left hover:bg-gray-50 border-b border-gray-100 last:border-0"
                    >
                      <p className="font-semibold text-gray-900">{result.symbol}</p>
                      <p className="text-sm text-gray-600">{result.name}</p>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Selected Symbol */}
            {selectedSymbol && currentQuote && (
              <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-2xl font-bold text-gray-900">{selectedSymbol}</h3>
                    <p className="text-sm text-gray-600">{currentQuote.exchange}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-gray-900">${currentQuote.price.toFixed(2)}</p>
                    <p className={`text-sm font-semibold flex items-center justify-end ${
                      currentQuote.change_percent >= 0 ? 'text-success-600' : 'text-danger-600'
                    }`}>
                      {currentQuote.change_percent >= 0 ? (
                        <TrendingUp className="w-4 h-4 mr-1" />
                      ) : (
                        <TrendingDown className="w-4 h-4 mr-1" />
                      )}
                      {currentQuote.change_percent >= 0 ? '+' : ''}{currentQuote.change_percent.toFixed(2)}%
                    </p>
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4 mt-3 pt-3 border-t border-gray-200">
                  <div>
                    <p className="text-xs text-gray-500">Bid</p>
                    <p className="font-semibold text-gray-900">${currentQuote.bid.toFixed(2)}</p>
                  </div>
                  <div>
                    <p className="text-xs text-gray-500">Ask</p>
                    <p className="font-semibold text-gray-900">${currentQuote.ask.toFixed(2)}</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Order Entry Form */}
          {selectedSymbol && (
            <div className="card">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Place Order</h2>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Buy/Sell Toggle */}
                <div className="grid grid-cols-2 gap-4">
                  <button
                    type="button"
                    onClick={() => setSide('buy')}
                    className={`py-3 rounded-lg font-semibold ${
                      side === 'buy'
                        ? 'bg-success-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Buy
                  </button>
                  <button
                    type="button"
                    onClick={() => setSide('sell')}
                    className={`py-3 rounded-lg font-semibold ${
                      side === 'sell'
                        ? 'bg-danger-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    Sell
                  </button>
                </div>

                {/* Order Type */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Order Type
                  </label>
                  <select
                    value={orderType}
                    onChange={(e) => setOrderType(e.target.value as OrderType)}
                    className="input"
                  >
                    <option value="market">Market Order</option>
                    <option value="limit">Limit Order</option>
                  </select>
                </div>

                {/* Quantity */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Quantity
                  </label>
                  <input
                    type="number"
                    step="0.01"
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                    className="input"
                    placeholder="Enter quantity"
                    disabled={loading}
                  />
                </div>

                {/* Limit Price */}
                {orderType === 'limit' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Limit Price
                    </label>
                    <input
                      type="number"
                      step="0.01"
                      value={limitPrice}
                      onChange={(e) => setLimitPrice(e.target.value)}
                      className="input"
                      placeholder="Enter limit price"
                      disabled={loading}
                    />
                  </div>
                )}

                {/* Estimated Cost */}
                <div className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Estimated {side === 'buy' ? 'Cost' : 'Proceeds'}</span>
                    <span className="text-lg font-bold text-gray-900">
                      ${calculateEstimatedCost().toFixed(2)}
                    </span>
                  </div>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={loading || !quantity}
                  className={`w-full py-3 rounded-lg font-semibold text-white disabled:opacity-50 disabled:cursor-not-allowed ${
                    side === 'buy' ? 'bg-success-600 hover:bg-success-700' : 'bg-danger-600 hover:bg-danger-700'
                  }`}
                >
                  {loading ? 'Placing Order...' : `${side === 'buy' ? 'Buy' : 'Sell'} ${selectedSymbol}`}
                </button>
              </form>
            </div>
          )}
        </div>

        {/* Portfolio Summary */}
        <div className="space-y-6">
          {portfolio && (
            <>
              <div className="card">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Account</h2>
                <div className="space-y-3">
                  <div>
                    <p className="text-sm text-gray-600">Buying Power</p>
                    <p className="text-2xl font-bold text-gray-900">
                      ${portfolio.buying_power.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                    </p>
                  </div>
                  <div className="pt-3 border-t border-gray-200">
                    <p className="text-sm text-gray-600">Portfolio Value</p>
                    <p className="text-lg font-semibold text-gray-900">
                      ${portfolio.total_value.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                    </p>
                  </div>
                  <div className="pt-3 border-t border-gray-200">
                    <p className="text-sm text-gray-600">Cash Balance</p>
                    <p className="text-lg font-semibold text-gray-900">
                      ${portfolio.cash_balance.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                    </p>
                  </div>
                </div>
              </div>

              <div className="card">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Today's P&L</h2>
                <p className={`text-3xl font-bold ${
                  portfolio.day_pl >= 0 ? 'text-success-600' : 'text-danger-600'
                }`}>
                  {portfolio.day_pl >= 0 ? '+' : ''}${portfolio.day_pl.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                </p>
                <p className={`text-sm font-semibold mt-1 ${
                  portfolio.day_pl_percent >= 0 ? 'text-success-600' : 'text-danger-600'
                }`}>
                  {portfolio.day_pl_percent >= 0 ? '+' : ''}{portfolio.day_pl_percent.toFixed(2)}%
                </p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
