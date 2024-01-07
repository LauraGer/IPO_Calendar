from app.config import HOST, DATABASE, USER, PASSWORD
from app.dba.models import Base, IPO_Calendar, MonthlyHistoryByStockSymbol, StockSymbols
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection parameters
db_params = {
    'host': '0.0.0.0',
    'database': DATABASE,
    'user': USER,
    'password': PASSWORD,
}

print('##CREATE CONNECTION##')
engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define connection parameters
class PostgresIPOcalendarConfig:
    conn_id = 'postgres_IPO_calendar'
    conn_type = 'postgres'
    host = HOST
    database = DATABASE
    login = USER
    password = PASSWORD
    schema = 'public'


def build_date_range(year, month):

    start_date = datetime(year, month, 1).date()
    next_month = start_date.replace(day=28) + timedelta(days=4)
    end_date = next_month - timedelta(days=next_month.day)

    return start_date, end_date


def get_entries_from_db(year, month):

    date_from, date_to = build_date_range(year, month)

    results = session.query(IPO_Calendar.date,IPO_Calendar.name, IPO_Calendar.symbol).filter(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to
    ).all()


    return(results)

def get_history_by_symbol(symbol):

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

    results = session.query(IPO_Calendar.symbol).filter(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to,
        IPO_Calendar.symbol != None
    ).all()

    raw_strings = [item[0] for item in results]

    return(raw_strings)

def get_entries(year, month):
    date_from, date_to = build_date_range(year, month)

    results = session.query(
                        IPO_Calendar.date,
                        IPO_Calendar.symbol
                        ).filter(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to
    ).all()

    entries = {
        (date.year, date.month, date.day): event_name
        for date, event_name in results
    }
    return(entries)

def get_entries_from_db(year, month ):
    print(year, month )
    date_from, date_to = build_date_range(year, month)
    print(date_from, date_to)
    results = session.query(IPO_Calendar.date,IPO_Calendar.name, IPO_Calendar.symbol).filter(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to
    ).all()
    return(results)

def get_symbol_details(symbol):
    results = session.query(StockSymbols.description,StockSymbols.currency).filter(
        StockSymbols.symbol == symbol
    ).first()
    return(results)
