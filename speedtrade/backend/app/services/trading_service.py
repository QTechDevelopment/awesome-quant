"""
Trading service for order execution and management.
Integrates with Alpaca for stocks and CCXT for crypto trading.
"""
from typing import Optional, List, Dict, Any
from decimal import Decimal
from datetime import datetime
import asyncio

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide as AlpacaOrderSide, TimeInForce as AlpacaTimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest
import ccxt.async_support as ccxt
from loguru import logger

from app.core.config import get_settings
from app.models.trading import (
    Order, OrderSide, OrderType, OrderStatus, 
    TimeInForce, AssetType, Position, Trade
)
from app.models.user import Portfolio


settings = get_settings()


class TradingService:
    """Service for handling trading operations across multiple brokers."""
    
    def __init__(self):
        # Initialize Alpaca client
        self.alpaca_trading = TradingClient(
            api_key=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY,
            paper=settings.ALPACA_PAPER_TRADING
        )
        self.alpaca_data = StockHistoricalDataClient(
            api_key=settings.ALPACA_API_KEY,
            secret_key=settings.ALPACA_SECRET_KEY
        )
        
        # Initialize CCXT exchanges
        self.exchanges: Dict[str, ccxt.Exchange] = {}
        self._init_exchanges()
    
    def _init_exchanges(self):
        """Initialize cryptocurrency exchanges."""
        # Coinbase Pro for crypto trading
        if settings.COINBASE_API_KEY:
            self.exchanges['coinbase'] = ccxt.coinbasepro({
                'apiKey': settings.COINBASE_API_KEY,
                'secret': settings.COINBASE_SECRET,
                'password': settings.COINBASE_PASSPHRASE,
                'enableRateLimit': True
            })
    
    async def place_order(
        self,
        db: Session,
        user_id: int,
        symbol: str,
        side: OrderSide,
        order_type: OrderType,
        quantity: Decimal,
        asset_type: AssetType,
        limit_price: Optional[Decimal] = None,
        stop_price: Optional[Decimal] = None,
        time_in_force: TimeInForce = TimeInForce.DAY
    ) -> Order:
        """
        Place a trading order.
        
        Args:
            db: Database session
            user_id: User ID placing the order
            symbol: Trading symbol (e.g., 'AAPL', 'BTC/USD')
            side: Buy or sell
            order_type: Market, limit, stop, or stop_limit
            quantity: Order quantity
            asset_type: Stock or crypto
            limit_price: Limit price for limit orders
            stop_price: Stop price for stop orders
            time_in_force: Order duration
            
        Returns:
            Created Order object
            
        Raises:
            ValueError: If order validation fails
            Exception: If broker API call fails
        """
        # Validate order
        await self._validate_order(db, user_id, symbol, side, quantity, asset_type)
        
        # Create order in database
        order = Order(
            user_id=user_id,
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity,
            limit_price=limit_price,
            stop_price=stop_price,
            time_in_force=time_in_force,
            asset_type=asset_type,
            status=OrderStatus.PENDING
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        
        try:
            # Route to appropriate broker
            if asset_type == AssetType.STOCK:
                broker_order = await self._place_alpaca_order(order)
            elif asset_type == AssetType.CRYPTO:
                broker_order = await self._place_crypto_order(order)
            else:
                raise ValueError(f"Unsupported asset type: {asset_type}")
            
            # Update order with broker details
            order.broker_order_id = str(broker_order['id'])
            order.status = OrderStatus.SUBMITTED
            order.submitted_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Order placed: {order.id} - {symbol} {side.value} {quantity}")
            
            return order
            
        except Exception as e:
            order.status = OrderStatus.REJECTED
            order.rejection_reason = str(e)
            db.commit()
            logger.error(f"Order rejected: {order.id} - {str(e)}")
            raise
    
    async def _place_alpaca_order(self, order: Order) -> Dict[str, Any]:
        """Place order with Alpaca."""
        # Convert enums to Alpaca format
        alpaca_side = AlpacaOrderSide.BUY if order.side == OrderSide.BUY else AlpacaOrderSide.SELL
        alpaca_tif = self._convert_time_in_force(order.time_in_force)
        
        if order.type == OrderType.MARKET:
            order_request = MarketOrderRequest(
                symbol=order.symbol,
                qty=float(order.quantity),
                side=alpaca_side,
                time_in_force=alpaca_tif
            )
        elif order.type == OrderType.LIMIT:
            order_request = LimitOrderRequest(
                symbol=order.symbol,
                qty=float(order.quantity),
                side=alpaca_side,
                time_in_force=alpaca_tif,
                limit_price=float(order.limit_price)
            )
        else:
            raise ValueError(f"Unsupported order type for Alpaca: {order.type}")
        
        # Submit order
        alpaca_order = self.alpaca_trading.submit_order(order_request)
        
        return {
            'id': alpaca_order.id,
            'status': alpaca_order.status,
            'filled_qty': float(alpaca_order.filled_qty or 0),
            'filled_avg_price': float(alpaca_order.filled_avg_price or 0)
        }
    
    async def _place_crypto_order(self, order: Order) -> Dict[str, Any]:
        """Place order with crypto exchange."""
        exchange = self.exchanges.get('coinbase')
        if not exchange:
            raise ValueError("No crypto exchange configured")
        
        # Convert order type
        order_type_map = {
            OrderType.MARKET: 'market',
            OrderType.LIMIT: 'limit'
        }
        
        try:
            result = await exchange.create_order(
                symbol=order.symbol,
                type=order_type_map[order.type],
                side=order.side.value,
                amount=float(order.quantity),
                price=float(order.limit_price) if order.limit_price else None
            )
            
            return {
                'id': result['id'],
                'status': result['status'],
                'filled_qty': result.get('filled', 0),
                'filled_avg_price': result.get('average', 0)
            }
            
        except Exception as e:
            logger.error(f"Crypto order failed: {str(e)}")
            raise
    
    async def _validate_order(
        self,
        db: Session,
        user_id: int,
        symbol: str,
        side: OrderSide,
        quantity: Decimal,
        asset_type: AssetType
    ):
        """Validate order before placement."""
        # Get user's portfolio
        portfolio = db.query(Portfolio).filter(Portfolio.user_id == user_id).first()
        if not portfolio:
            raise ValueError("Portfolio not found")
        
        # Check buying power for buy orders
        if side == OrderSide.BUY:
            # Get current price
            price = await self._get_current_price(symbol, asset_type)
            order_value = quantity * Decimal(str(price))
            
            if order_value > portfolio.cash_balance:
                raise ValueError(f"Insufficient buying power: ${portfolio.cash_balance} available, ${order_value} required")
        
        # Check position for sell orders
        elif side == OrderSide.SELL:
            position = db.query(Position).filter(
                and_(
                    Position.user_id == user_id,
                    Position.symbol == symbol,
                    Position.asset_type == asset_type
                )
            ).first()
            
            if not position or position.quantity < quantity:
                raise ValueError(f"Insufficient shares: {position.quantity if position else 0} available, {quantity} required")
    
    async def _get_current_price(self, symbol: str, asset_type: AssetType) -> float:
        """Get current market price for symbol."""
        if asset_type == AssetType.STOCK:
            request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            quotes = self.alpaca_data.get_stock_latest_quote(request)
            return float(quotes[symbol].ask_price)
        
        elif asset_type == AssetType.CRYPTO:
            exchange = self.exchanges.get('coinbase')
            if exchange:
                ticker = await exchange.fetch_ticker(symbol)
                return ticker['ask']
        
        raise ValueError(f"Could not get price for {symbol}")
    
    def _convert_time_in_force(self, tif: TimeInForce) -> AlpacaTimeInForce:
        """Convert TimeInForce enum to Alpaca format."""
        mapping = {
            TimeInForce.DAY: AlpacaTimeInForce.DAY,
            TimeInForce.GTC: AlpacaTimeInForce.GTC,
            TimeInForce.IOC: AlpacaTimeInForce.IOC,
            TimeInForce.FOK: AlpacaTimeInForce.FOK
        }
        return mapping[tif]
    
    async def cancel_order(self, db: Session, order_id: int, user_id: int) -> Order:
        """Cancel a pending order."""
        order = db.query(Order).filter(
            and_(Order.id == order_id, Order.user_id == user_id)
        ).first()
        
        if not order:
            raise ValueError("Order not found")
        
        if order.status not in [OrderStatus.PENDING, OrderStatus.SUBMITTED]:
            raise ValueError(f"Cannot cancel order in status: {order.status}")
        
        try:
            # Cancel with broker
            if order.asset_type == AssetType.STOCK:
                self.alpaca_trading.cancel_order_by_id(order.broker_order_id)
            elif order.asset_type == AssetType.CRYPTO:
                exchange = self.exchanges.get('coinbase')
                if exchange:
                    await exchange.cancel_order(order.broker_order_id)
            
            order.status = OrderStatus.CANCELLED
            order.cancelled_at = datetime.utcnow()
            db.commit()
            
            logger.info(f"Order cancelled: {order_id}")
            return order
            
        except Exception as e:
            logger.error(f"Failed to cancel order {order_id}: {str(e)}")
            raise
    
    def get_orders(
        self,
        db: Session,
        user_id: int,
        status: Optional[OrderStatus] = None,
        limit: int = 50
    ) -> List[Order]:
        """Get user's orders."""
        query = db.query(Order).filter(Order.user_id == user_id)
        
        if status:
            query = query.filter(Order.status == status)
        
        return query.order_by(Order.created_at.desc()).limit(limit).all()
    
    def get_positions(self, db: Session, user_id: int) -> List[Position]:
        """Get user's open positions."""
        return db.query(Position).filter(
            and_(Position.user_id == user_id, Position.quantity > 0)
        ).all()
    
    async def sync_order_status(self, db: Session, order_id: int):
        """Sync order status with broker."""
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order or not order.broker_order_id:
            return
        
        try:
            if order.asset_type == AssetType.STOCK:
                alpaca_order = self.alpaca_trading.get_order_by_id(order.broker_order_id)
                
                # Update status
                status_map = {
                    'new': OrderStatus.SUBMITTED,
                    'partially_filled': OrderStatus.PARTIALLY_FILLED,
                    'filled': OrderStatus.FILLED,
                    'canceled': OrderStatus.CANCELLED,
                    'rejected': OrderStatus.REJECTED
                }
                
                order.status = status_map.get(alpaca_order.status, order.status)
                order.filled_quantity = Decimal(str(alpaca_order.filled_qty or 0))
                order.filled_avg_price = Decimal(str(alpaca_order.filled_avg_price or 0))
                
                if order.status == OrderStatus.FILLED:
                    order.filled_at = datetime.utcnow()
                    await self._update_position(db, order)
                
                db.commit()
                
        except Exception as e:
            logger.error(f"Failed to sync order {order_id}: {str(e)}")
    
    async def _update_position(self, db: Session, order: Order):
        """Update position after order fill."""
        position = db.query(Position).filter(
            and_(
                Position.user_id == order.user_id,
                Position.symbol == order.symbol,
                Position.asset_type == order.asset_type
            )
        ).first()
        
        if not position:
            position = Position(
                user_id=order.user_id,
                symbol=order.symbol,
                asset_type=order.asset_type,
                quantity=Decimal(0),
                average_entry_price=Decimal(0)
            )
            db.add(position)
        
        # Update quantity and average price
        if order.side == OrderSide.BUY:
            total_cost = (position.quantity * position.average_entry_price + 
                         order.filled_quantity * order.filled_avg_price)
            position.quantity += order.filled_quantity
            position.average_entry_price = total_cost / position.quantity
        else:  # SELL
            position.quantity -= order.filled_quantity
            if position.quantity == 0:
                position.average_entry_price = Decimal(0)
        
        # Create trade record
        trade = Trade(
            order_id=order.id,
            user_id=order.user_id,
            symbol=order.symbol,
            side=order.side,
            quantity=order.filled_quantity,
            price=order.filled_avg_price,
            asset_type=order.asset_type,
            executed_at=datetime.utcnow()
        )
        db.add(trade)
        
        # Update portfolio
        portfolio = db.query(Portfolio).filter(Portfolio.user_id == order.user_id).first()
        if portfolio:
            order_value = order.filled_quantity * order.filled_avg_price
            if order.side == OrderSide.BUY:
                portfolio.cash_balance -= order_value
            else:
                portfolio.cash_balance += order_value
        
        db.commit()
    
    async def close(self):
        """Close all exchange connections."""
        for exchange in self.exchanges.values():
            await exchange.close()


# Global instance
_trading_service: Optional[TradingService] = None


def get_trading_service() -> TradingService:
    """Get or create trading service instance."""
    global _trading_service
    if _trading_service is None:
        _trading_service = TradingService()
    return _trading_service
