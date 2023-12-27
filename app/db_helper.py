from config import HOST, DATABASE, USER, PASSWORD
from sqlalchemy import create_engine, select, func, Table, MetaData

from datetime import datetime, timedelta

# PostgreSQL connection parameters
db_params = {
    'host': "localhost",
    'database': DATABASE,
    'user': USER,
    'password': PASSWORD,
}

print('##CREATE CONNECTION##')
engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")

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