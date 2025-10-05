from sqlalchemy import Column, String, DateTime, Enum, Numeric, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class OrderSide(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"


class OrderType(str, enum.Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    PARTIAL_FILL = "partial_fill"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class TimeInForce(str, enum.Enum):
    DAY = "day"
    GTC = "gtc"  # Good till cancelled
    IOC = "ioc"  # Immediate or cancel
    FOK = "fok"  # Fill or kill


class AssetType(str, enum.Enum):
    STOCK = "stock"
    CRYPTO = "crypto"
    ETF = "etf"


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Order details
    symbol = Column(String, nullable=False, index=True)
    asset_type = Column(Enum(AssetType), nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    type = Column(Enum(OrderType), nullable=False)
    
    # Quantities & Prices
    quantity = Column(Numeric(20, 8), nullable=False)
    filled_quantity = Column(Numeric(20, 8), default=0)
    price = Column(Numeric(20, 8), nullable=True)  # For limit orders
    stop_price = Column(Numeric(20, 8), nullable=True)  # For stop orders
    avg_fill_price = Column(Numeric(20, 8), nullable=True)
    
    # Status
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, index=True)
    time_in_force = Column(Enum(TimeInForce), default=TimeInForce.DAY)
    
    # External IDs (from broker)
    broker_order_id = Column(String, nullable=True, index=True)
    
    # Commission and fees
    commission = Column(Numeric(10, 2), default=0)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    filled_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Order {self.symbol} {self.side} {self.quantity} @ {self.status}>"


class Position(Base):
    __tablename__ = "positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    symbol = Column(String, nullable=False, index=True)
    asset_type = Column(Enum(AssetType), nullable=False)
    
    # Position details
    quantity = Column(Numeric(20, 8), nullable=False)
    avg_entry_price = Column(Numeric(20, 8), nullable=False)
    current_price = Column(Numeric(20, 8), default=0)
    market_value = Column(Numeric(20, 2), default=0)
    
    # Cost basis
    cost_basis = Column(Numeric(20, 2), nullable=False)
    
    # P&L
    unrealized_pnl = Column(Numeric(20, 2), default=0)
    unrealized_pnl_percent = Column(Numeric(10, 4), default=0)
    realized_pnl = Column(Numeric(20, 2), default=0)
    
    # Status
    is_closed = Column(Boolean, default=False)
    
    # Timestamps
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Position {self.symbol} {self.quantity}>"


class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    # Trade details
    symbol = Column(String, nullable=False, index=True)
    asset_type = Column(Enum(AssetType), nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    
    # Execution
    quantity = Column(Numeric(20, 8), nullable=False)
    price = Column(Numeric(20, 8), nullable=False)
    total_value = Column(Numeric(20, 2), nullable=False)
    commission = Column(Numeric(10, 2), default=0)
    
    # External reference
    broker_trade_id = Column(String, nullable=True)
    
    # Timestamp
    executed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<Trade {self.symbol} {self.side} {self.quantity} @ {self.price}>"
