from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Table definition
class IPO_Calendar(Base):
    __tablename__ = 'IPO_Calendar'
    __table_args__ = {'schema': 'public'}  # Specify the schema

    ipo_calencar_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    exchange = Column(String(64))
    name = Column(String(255))
    agnumberOfShares = Column(Integer)
    price = Column(Float)
    status = Column(String(32))
    symbol = Column(String(32))
    totalShareValue = Column(Integer)

class IPO_CalendarArchive(Base):
    __tablename__ = 'IPO_CalendarArchive'
    __table_args__ = {'schema': 'public'}  # Specify the schema

    ipo_calencar_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    exchange = Column(String(64))
    name = Column(String(255))
    agnumberOfShares = Column(Integer)
    price = Column(Float)
    status = Column(String(32))
    symbol = Column(String(32))
    totalShareValue = Column(Integer)
    timestamp_column = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class StockSymbols(Base):
    __tablename__ = 'StockSymblos'
    __table_args__ = {'schema': 'public'}  # Specify the schema

    symbol_id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String(8))
    description = Column(String(255))
    displaySymbol = Column(String(16))
    figi = Column(String(64))
    mic = Column(String(32))
    symbol = Column(String(32))
    type = Column(String(32))