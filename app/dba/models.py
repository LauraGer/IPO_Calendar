from sqlalchemy import Column, Integer, String, Date, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Table definition
class IPO_Calendar(Base):
    __tablename__ = 'IPO_Calendar'
    __table_args__ = {'schema': 'public'}  # Specify the schema

    ipo_calendar_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    exchange = Column(String(64))
    name = Column(String(255))
    numberOfShares = Column(Float)
    price = Column(String(32))
    status = Column(String(32))
    symbol = Column(String(32))
    totalSharesValue = Column(Float)

class IPO_CalendarArchive(Base):
    __tablename__ = 'IPO_CalendarArchive'
    __table_args__ = {'schema': 'public'}  # Specify the schema

    ipo_calendar_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    exchange = Column(String(64))
    name = Column(String(255))
    numberOfShares = Column(Float)
    price = Column(String(32))
    status = Column(String(32))
    symbol = Column(String(32))
    totalShareValue = Column(Float)
    timestamp_column = Column(DateTime)


class StockSymbols(Base):
    __tablename__ = 'StockSymbols'
    __table_args__ = {'schema': 'public'}  # Specify the schema

    symbol_id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String(8))
    description = Column(String(255))
    displaySymbol = Column(String(16))
    figi = Column(String(64))
    mic = Column(String(32))
    symbol = Column(String(32))
    type = Column(String(32))