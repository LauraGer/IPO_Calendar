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
# WIP - not sure if I want a global db_helper

from app.config import HOST, DATABASE, USER, PASSWORD
from app.dba.models import Base, IPO_Calendar, MonthlyHistoryByStockSymbol, StockSymbols
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection parameters
db_params = {
    "host": HOST,
    "database": DATABASE,
    "user": USER,
    "password": PASSWORD,
}

print("##CREATE CONNECTION##")
def get_engine_by_db_params(db_params):
    engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")
    return engine


def get_session():
   # Create a session
    engine = get_engine_by_db_params(db_params)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# Define connection parameters
class PostgresIPOcalendarConfig:
    conn_id = "postgres_IPO_calendar"
    conn_type = "postgres"
    host = HOST
    database = DATABASE
    login = USER
    password = PASSWORD
    schema = "public"


def build_date_range(year, month):

    start_date = datetime(year, month, 1).date()
    next_month = start_date.replace(day=28) + timedelta(days=4)
    end_date = next_month - timedelta(days=next_month.day)

    return start_date, end_date


def get_entries_from_db(year, month):

    date_from, date_to = build_date_range(year, month)
    session = get_session()
    results = session.query(IPO_Calendar.date,IPO_Calendar.name, IPO_Calendar.symbol).filter(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to
    ).all()


    return(results)

def get_history_by_symbol(symbol):
    session = get_session()

    results = session.query(MonthlyHistoryByStockSymbol.date,
                            MonthlyHistoryByStockSymbol.open,
                            MonthlyHistoryByStockSymbol.high,
                            MonthlyHistoryByStockSymbol.low,
                            MonthlyHistoryByStockSymbol.volume).filter(
        MonthlyHistoryByStockSymbol.symbol == symbol
    ).all()


    return(results)

def get_symbols(year, month):
    date_from, date_to = build_date_range(year, month)

    session = get_session()
    results = session.query(IPO_Calendar.symbol).filter(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to,
        IPO_Calendar.symbol != None
    ).all()

    raw_strings = [item[0] for item in results]

    return(raw_strings)

def get_entries(year, month):
    date_from, date_to = build_date_range(year, month)

    session = get_session()
    results = session.query(
                        IPO_Calendar.date,
                        IPO_Calendar.symbol
                        ).filter(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to,
        IPO_Calendar.symbol != None
    ).all()
    return(results)

def get_entries_from_db(year, month ):
    print(year, month )
    session = get_session()
    date_from, date_to = build_date_range(year, month)
    print(date_from, date_to)
    results = session.query(IPO_Calendar.date,IPO_Calendar.name, IPO_Calendar.symbol).filter(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to
    ).all()
    return(results)

def get_symbol_details(symbol):
    session = get_session()
    results = session.query(StockSymbols.description,StockSymbols.currency).filter(
        StockSymbols.symbol == symbol
    ).first()
    return(results)
