from config import HOST, DATABASE, USER, PASSWORD
from sqlalchemy import create_engine, select, func, Table, MetaData

# PostgreSQL connection parameters
db_params = {
    'host': "postgres",
    'database': DATABASE,
    'user': USER,
    'password': PASSWORD,
}

print('##CREATE CONNECTION##')
engine = create_engine(f"postgresql://{db_params['user']}:{db_params['password']}@{db_params['host']}/{db_params['database']}")

metadata = MetaData(bind=engine)

# Define connection parameters
class PostgresIPOcalendarConfig:
    conn_id = 'postgres_IPO_calendar'
    conn_type = 'postgres'
    host = HOST
    database = DATABASE
    login = USER
    password = PASSWORD
    schema = 'public'

def get_min_date_from_table(table):
    table = Table("IPO_Calendar", metadata, autoload=True)
    min_date_statement = select([func.min(table.columns.date)])
    with engine.connect() as conn:
        result = conn.execute(min_date_statement)
        min_date = result.scalar()
    return min_date

def check_if_records_exist(table):
    table = Table("IPO_Calendar", metadata, autoload=True)
    count_statement = select([func.count(table.columns.date)])

    with engine.connect() as conn:
        result = conn.execute(count_statement)
        row_count = result.scalar()

    if row_count > 0:
        return True
    else:
        return False
