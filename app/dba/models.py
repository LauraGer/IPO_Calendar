"""
Copyright 2023 Laura Gerlach

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from sqlalchemy import Column, Integer, String, Date, Float, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Table definition
class IPO_Calendar(Base):
    __tablename__ = "IPO_Calendar"
    __table_args__ = {"schema": "public"}  # Specify the schema

    ipo_calendar_id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(Date)
    exchange = Column(String(64))
    name = Column(String(255))
    numberOfShares = Column(Float)
    price = Column(String(32))
    status = Column(String(32))
    symbol = Column(String(32))
    totalSharesValue = Column(Float)

class IPO_CalendarArchive(Base):
    __tablename__ = "IPO_CalendarArchive"
    __table_args__ = {"schema": "public"}  # Specify the schema

    ipo_calendar_id = Column(BigInteger, primary_key=True, autoincrement=True)
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
    __tablename__ = "StockSymbols"
    __table_args__ = {"schema": "public"}  # Specify the schema

    symbol_id = Column(BigInteger, primary_key=True, autoincrement=True)
    currency = Column(String(8))
    description = Column(String(255))
    displaySymbol = Column(String(16))
    figi = Column(String(64))
    mic = Column(String(32))
    symbol = Column(String(32))
    type = Column(String(32))

class MonthlyHistoryByStockSymbol(Base):
    __tablename__ = "MonthlyHistoryByStockSymbol"
    __table_args__ = {"schema": "public"}  # Specify the schema

    monthly_history_id = Column(BigInteger, primary_key=True, autoincrement=True)
    symbol = Column(String(32))
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)