"""
Market data service for real-time quotes and historical data.
"""
from typing import List, Optional
from decimal import Decimal
from datetime import datetime, timedelta
import asyncio

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import (
    StockLatestQuoteRequest,
    StockBarsRequest,
    StockSnapshotRequest
)
from alpaca.data.timeframe import TimeFrame
import yfinance as yf
import ccxt.async_support as ccxt
from loguru import logger

from app.core.config import get_settings
from app.schemas.market_data import QuoteResponse, SearchResult, ChartData


settings = get_settings()


class MarketDataService:
    """Service for fetching market data from various sources."""
    
    def __init__(self):
        self.alpaca_data = StockHistoricalDataClient(
            api_key=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY
        )
        
        # Initialize crypto exchange for market data
        self.crypto_exchange = ccxt.binance({'enableRateLimit': True})
    
    async def get_quote(self, symbol: str) -> QuoteResponse:
        """
        Get real-time quote for a symbol.
        Auto-detects if stock or crypto based on symbol format.
        """
        # Check if crypto (contains /)
        if '/' in symbol:
            return await self._get_crypto_quote(symbol)
        else:
            return await self._get_stock_quote(symbol)
    
    async def _get_stock_quote(self, symbol: str) -> QuoteResponse:
        """Get stock quote from Alpaca."""
        try:
            # Get latest quote
            request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            quotes = self.alpaca_data.get_stock_latest_quote(request)
            quote = quotes[symbol]
            
            # Get daily bars for high/low/open/close
            bars_request = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=TimeFrame.Day,
                start=datetime.now().date()
            )
            bars = self.alpaca_data.get_stock_bars(bars_request)
            
            if symbol in bars:
                bar = bars[symbol][0]
                high = Decimal(str(bar.high))
                low = Decimal(str(bar.low))
                open_price = Decimal(str(bar.open))
                close = Decimal(str(bar.close))
                volume = bar.volume
            else:
                # Fallback to quote data
                high = Decimal(str(quote.ask_price))
                low = Decimal(str(quote.bid_price))
                open_price = Decimal(str(quote.bid_price))
                close = Decimal(str(quote.ask_price))
                volume = 0
            
            # Calculate previous close (simplified - should come from API)
            previous_close = close * Decimal('0.99')
            last_price = Decimal(str(quote.ask_price))
            change = last_price - previous_close
            change_percent = (change / previous_close) * 100
            
            return QuoteResponse(
                symbol=symbol,
                bid_price=Decimal(str(quote.bid_price)),
                ask_price=Decimal(str(quote.ask_price)),
                last_price=last_price,
                last_volume=int(quote.ask_size),
                high=high,
                low=low,
                open=open_price,
                previous_close=previous_close,
                change=change,
                change_percent=change_percent,
                volume=volume,
                timestamp=quote.timestamp
            )
            
        except Exception as e:
            logger.error(f"Failed to get stock quote for {symbol}: {str(e)}")
            raise
    
    async def _get_crypto_quote(self, symbol: str) -> QuoteResponse:
        """Get crypto quote from exchange."""
        try:
            ticker = await self.crypto_exchange.fetch_ticker(symbol)
            
            last_price = Decimal(str(ticker['last']))
            previous_close = Decimal(str(ticker['close']))
            change = last_price - previous_close
            change_percent = Decimal(str(ticker['percentage']))
            
            return QuoteResponse(
                symbol=symbol,
                bid_price=Decimal(str(ticker['bid'])),
                ask_price=Decimal(str(ticker['ask'])),
                last_price=last_price,
                last_volume=int(ticker['quoteVolume']),
                high=Decimal(str(ticker['high'])),
                low=Decimal(str(ticker['low'])),
                open=Decimal(str(ticker['open'])),
                previous_close=previous_close,
                change=change,
                change_percent=change_percent,
                volume=int(ticker['baseVolume']),
                timestamp=datetime.fromtimestamp(ticker['timestamp'] / 1000)
            )
            
        except Exception as e:
            logger.error(f"Failed to get crypto quote for {symbol}: {str(e)}")
            raise
    
    async def search_symbols(self, query: str, limit: int = 10) -> List[SearchResult]:
        """
        Search for symbols by name or ticker.
        Uses yfinance for stock search and CCXT for crypto.
        """
        results = []
        
        # Search stocks (simplified - in production use proper API)
        try:
            # Common stock symbols matching query
            ticker = yf.Ticker(query.upper())
            info = ticker.info
            if info and 'symbol' in info:
                results.append(SearchResult(
                    symbol=info['symbol'],
                    name=info.get('longName', info['symbol']),
                    asset_type='stock',
                    exchange=info.get('exchange')
                ))
        except:
            pass
        
        # Search crypto
        try:
            markets = await self.crypto_exchange.load_markets()
            crypto_matches = [
                SearchResult(
                    symbol=symbol,
                    name=symbol,
                    asset_type='crypto',
                    exchange='Binance'
                )
                for symbol in markets.keys()
                if query.upper() in symbol.upper()
            ]
            results.extend(crypto_matches[:limit - len(results)])
        except Exception as e:
            logger.error(f"Failed to search crypto symbols: {str(e)}")
        
        return results[:limit]
    
    async def get_chart_data(
        self,
        symbol: str,
        interval: str,
        period: str
    ) -> List[ChartData]:
        """Get historical chart data."""
        if '/' in symbol:
            return await self._get_crypto_chart(symbol, interval, period)
        else:
            return await self._get_stock_chart(symbol, interval, period)
    
    async def _get_stock_chart(
        self,
        symbol: str,
        interval: str,
        period: str
    ) -> List[ChartData]:
        """Get stock chart data from Alpaca."""
        try:
            # Map interval to TimeFrame
            timeframe_map = {
                '1m': TimeFrame.Minute,
                '5m': TimeFrame.Minute,
                '15m': TimeFrame.Minute,
                '30m': TimeFrame.Minute,
                '1h': TimeFrame.Hour,
                '1D': TimeFrame.Day
            }
            
            # Map period to start date
            period_map = {
                '1D': datetime.now() - timedelta(days=1),
                '5D': datetime.now() - timedelta(days=5),
                '1M': datetime.now() - timedelta(days=30),
                '3M': datetime.now() - timedelta(days=90),
                '6M': datetime.now() - timedelta(days=180),
                '1Y': datetime.now() - timedelta(days=365)
            }
            
            request = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=timeframe_map.get(interval, TimeFrame.Day),
                start=period_map.get(period, datetime.now() - timedelta(days=30))
            )
            
            bars = self.alpaca_data.get_stock_bars(request)
            
            chart_data = []
            if symbol in bars:
                for bar in bars[symbol]:
                    chart_data.append(ChartData(
                        timestamp=bar.timestamp,
                        open=Decimal(str(bar.open)),
                        high=Decimal(str(bar.high)),
                        low=Decimal(str(bar.low)),
                        close=Decimal(str(bar.close)),
                        volume=bar.volume
                    ))
            
            return chart_data
            
        except Exception as e:
            logger.error(f"Failed to get stock chart for {symbol}: {str(e)}")
            raise
    
    async def _get_crypto_chart(
        self,
        symbol: str,
        interval: str,
        period: str
    ) -> List[ChartData]:
        """Get crypto chart data from exchange."""
        try:
            # Map interval to exchange format
            interval_map = {
                '1m': '1m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '4h': '4h',
                '1D': '1d'
            }
            
            # Map period to limit
            period_limit = {
                '1D': 24,
                '5D': 120,
                '1M': 30,
                '3M': 90,
                '6M': 180,
                '1Y': 365
            }
            
            ohlcv = await self.crypto_exchange.fetch_ohlcv(
                symbol,
                timeframe=interval_map.get(interval, '1d'),
                limit=period_limit.get(period, 30)
            )
            
            chart_data = [
                ChartData(
                    timestamp=datetime.fromtimestamp(candle[0] / 1000),
                    open=Decimal(str(candle[1])),
                    high=Decimal(str(candle[2])),
                    low=Decimal(str(candle[3])),
                    close=Decimal(str(candle[4])),
                    volume=int(candle[5])
                )
                for candle in ohlcv
            ]
            
            return chart_data
            
        except Exception as e:
            logger.error(f"Failed to get crypto chart for {symbol}: {str(e)}")
            raise
    
    async def get_top_gainers(self, limit: int = 10) -> List[QuoteResponse]:
        """Get top gaining stocks (simplified - should use screener API)."""
        # In production, use Alpaca's screener or another API
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        quotes = []
        
        for symbol in symbols[:limit]:
            try:
                quote = await self._get_stock_quote(symbol)
                quotes.append(quote)
            except:
                continue
        
        return sorted(quotes, key=lambda x: x.change_percent, reverse=True)
    
    async def get_top_losers(self, limit: int = 10) -> List[QuoteResponse]:
        """Get top losing stocks (simplified - should use screener API)."""
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
        quotes = []
        
        for symbol in symbols[:limit]:
            try:
                quote = await self._get_stock_quote(symbol)
                quotes.append(quote)
            except:
                continue
        
        return sorted(quotes, key=lambda x: x.change_percent)
    
    async def close(self):
        """Close exchange connections."""
        await self.crypto_exchange.close()


# Global instance
_market_data_service: Optional[MarketDataService] = None


def get_market_data_service() -> MarketDataService:
    """Get or create market data service instance."""
    global _market_data_service
    if _market_data_service is None:
        _market_data_service = MarketDataService()
    return _market_data_service
