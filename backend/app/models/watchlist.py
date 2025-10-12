from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Watchlist(Base):
    """Watchlist model for tracking user's stock lists"""
    
    __tablename__ = "watchlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    items = relationship("WatchlistItem", back_populates="watchlist", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Watchlist(id={self.id}, name='{self.name}', user_id={self.user_id})>"


class WatchlistItem(Base):
    """Watchlist item model for individual stocks in a watchlist"""
    
    __tablename__ = "watchlist_items"
    
    id = Column(Integer, primary_key=True, index=True)
    watchlist_id = Column(Integer, ForeignKey("watchlists.id", ondelete="CASCADE"), nullable=False)
    symbol = Column(String(20), nullable=False, index=True)
    asset_type = Column(String(20), nullable=False)  # 'stock' or 'crypto'
    
    # Timestamps
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    watchlist = relationship("Watchlist", back_populates="items")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('watchlist_id', 'symbol', name='uq_watchlist_symbol'),
    )
    
    def __repr__(self):
        return f"<WatchlistItem(id={self.id}, symbol='{self.symbol}', watchlist_id={self.watchlist_id})>"
