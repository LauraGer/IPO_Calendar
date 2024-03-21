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
from sqlalchemy import Column, Integer, String, Date, Float, DateTime, BigInteger, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class WatchlistUser(Base):
    __tablename__ = "WatchlistUsers"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String(164))

class AsOfList(Base):
    __tablename__ = "AsOfList"
    __table_args__ = {"schema": "public"}

    as_of_list_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    listname = Column(String, index=True)
    as_of_date = Column(Date, index=True)
    symbol = Column(String, index=True)
    volume = Column(String)
    as_of_price = Column(Float)



class AsOfStockHistory(Base):
    __tablename__ = "AsOfStockHistory"
    __table_args__ = {"schema": "public"}

    as_of_stock_history_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    symbol = Column(String(32), index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)