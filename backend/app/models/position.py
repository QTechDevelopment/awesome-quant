from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Position(Base):
    """Position model for tracking current holdings"""
    
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Position details
    symbol = Column(String(20), nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    average_entry_price = Column(Float, nullable=False)
    
    # Current valuation
    current_price = Column(Float, nullable=True)
    market_value = Column(Float, nullable=True)
    
    # P&L tracking
    cost_basis = Column(Float, nullable=False)
    unrealized_pl = Column(Float, default=0.0)
    unrealized_pl_percent = Column(Float, default=0.0)
    
    # Asset type
    asset_type = Column(String(20), default="stock")  # stock, crypto, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Position(id={self.id}, symbol='{self.symbol}', quantity={self.quantity})>"
