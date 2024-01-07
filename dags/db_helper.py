from config import HOST, DATABASE, USER, PASSWORD
from sqlalchemy import create_engine, select, func, Table, MetaData, delete

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

def check_if_value_exist_and_drop(table_name, column_name, value):
    table = Table(table_name, metadata, autoload=True)

    if column_name not in table.columns:
        print(f"Column '{column_name}' does not exist in the table '{table_name}'.")

        return False
    else:
        with engine.connect() as conn:
            query = select([table]).where(table.columns[column_name] == value)
            result = conn.execute(query)

            rows_to_delete = result.fetchall()

            if rows_to_delete:
                # delete_query = delete(table).where(table.columns[column_name] == value)
                # conn.execute(delete_query)
                print("NO DELETION CURRENTLY")
                print(f"Deleted {len(rows_to_delete)} record(s) where '{column_name}' = '{value}'.")

                return True
            else:
                print(f"The value '{value}' does not exist in column '{column_name}' of table '{table_name}'.")

                return False
