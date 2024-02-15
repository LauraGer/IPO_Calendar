
# Copyright 2023 Laura Gerlach

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
WIP - not sure if I want a global db_helper
"""

from app.config import HOST, IPO_CALENDAR_DB, USER, PASSWORD
from dba.models_dag import Base, IPO_Calendar, MonthlyHistoryByStockSymbol, StockSymbols
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection parameters
db_params = {
    "host": HOST,
    "database": IPO_CALENDAR_DB,
    "user": USER,
    "password": PASSWORD,
}

print("##CREATE CONNECTION##")
def get_engine_by_db_params(db_params=db_params):
    try:
        engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")

        return engine

    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")


def get_session(db_params=db_params):
    try:
        # Create a session
        engine = get_engine_by_db_params(db_params)
        Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = Session()

        return session

    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

session = get_session(db_params)

# Define connection parameters
class PostgresIPOcalendarConfig:
    conn_id = "postgres_IPO_calendar"
    conn_type = "postgres"
    host = HOST
    database = IPO_CALENDAR_DB
    login = USER
    password = PASSWORD
    schema = "public"

def get_year_month_integer(date_str):
    try:
        date_object = datetime.strptime(date_str, "%Y-%m-%d")
        year_month_numeric = date_object.year * 100 + date_object.month

        return year_month_numeric

    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

def build_date_range_year_month(year, month):
    try:
        start_date = datetime(year, month, 1).date()
        next_month = start_date.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)

        return start_date, end_date

    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

def get_entries_from_db(year, month, session = session):
    try:
        date_from, date_to = build_date_range_year_month(year, month)
        results = session.query(IPO_Calendar.date,IPO_Calendar.name, IPO_Calendar.symbol).filter(
            IPO_Calendar.date >= date_from,
            IPO_Calendar.date <= date_to
        ).all()


        return(results)
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

def get_history_by_symbol(symbol, session = session):
    try:
        results = session.query(MonthlyHistoryByStockSymbol.monthly_history_id,
                                MonthlyHistoryByStockSymbol.date,
                                MonthlyHistoryByStockSymbol.open,
                                MonthlyHistoryByStockSymbol.high,
                                MonthlyHistoryByStockSymbol.low,
                                MonthlyHistoryByStockSymbol.close,
                                MonthlyHistoryByStockSymbol.volume).filter(
            MonthlyHistoryByStockSymbol.symbol == symbol
        ).all()

        return(results)

    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

def get_symbols(year, month, session = session):
    try:
        date_from, date_to = build_date_range_year_month(year, month)

        results = session.query(IPO_Calendar.symbol).filter(
            IPO_Calendar.date >= date_from,
            IPO_Calendar.date <= date_to,
            IPO_Calendar.symbol != None,
            IPO_Calendar.symbol != ""
        ).all()

        raw_strings = [item[0] for item in results]

        return(raw_strings)

    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

def get_entries(year, month, session = session):
    try:
        date_from, date_to = build_date_range_year_month(year, month)
        results = (
            session.query(IPO_Calendar.date,
                        IPO_Calendar.symbol
                    )
            .filter(
                IPO_Calendar.date >= date_from,
                IPO_Calendar.date <= date_to,
                IPO_Calendar.symbol.isnot(None)
            )
            .all()
        )

        return(results)

    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

def get_entries_from_db(year, month , session = session):
    try:
        date_from, date_to = build_date_range_year_month(year, month)

        results = session.query(IPO_Calendar.date,IPO_Calendar.name, IPO_Calendar.symbol).filter(
            IPO_Calendar.date >= date_from,
            IPO_Calendar.date <= date_to
        ).all()
        return(results)

    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

def get_symbol_details(symbol, session = session):
    try:
        results = session.query(StockSymbols.description,StockSymbols.currency).filter(
            StockSymbols.symbol == symbol
        ).first()
        return(results)
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")
