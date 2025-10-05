from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Portfolio(Base):
    """Portfolio model for tracking overall account performance"""
    
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    
    # Cash balances
    cash_balance = Column(Float, default=0.0)
    buying_power = Column(Float, default=0.0)
    
    # Portfolio value
    portfolio_value = Column(Float, default=0.0)
    long_market_value = Column(Float, default=0.0)
    short_market_value = Column(Float, default=0.0)
    
    # Performance metrics
    total_pl = Column(Float, default=0.0)
    total_pl_percent = Column(Float, default=0.0)
    day_pl = Column(Float, default=0.0)
    day_pl_percent = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Portfolio(id={self.id}, user_id={self.user_id}, value={self.portfolio_value})>"
