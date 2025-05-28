import uuid
from sqlalchemy import Column, String, Integer, DateTime, Text, func, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base

class CryptoMetadata(Base):
    __tablename__ = "crypto_metadata"
    __table_args__ = {'schema': 'reporting_schema'}

    crypto_metadata_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crypto_name = Column(String(255), nullable=False)
    crypto_symbol = Column(String(10), nullable=False, unique=True)
    market_cap_rank = Column(Integer)
    circulating_supply = Column(BigInteger)
    max_supply = Column(BigInteger)
    listed_exchange = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)
    notes = Column(Text)

    # 🔥 NEW FIELDS BELOW

    # Stores a readable price change summary (e.g., "Change over 7 days: +3.5%")
    trend_info = Column(String(255))

    # Stores the most recent headline related to the coin (e.g., "2025-05-26: SEC approves ETH ETF")
    recent_headline = Column(String(512))
