from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Table definition
class IPO_Calendar(Base):
    __tablename__ = 'IPO_Calendar'
    __table_args__ = {'schema': 'public'}  # Specify the schema

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    exchange = Column(String(64))
    name = Column(String(255))
    agnumberOfShares = Column(Integer)
    price = Column(Float)
    status = Column(String(32))
    symbol = Column(String(32))
    totalShareValue = Column(Integer)