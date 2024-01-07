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

# This file

from app.dba.db_helper import build_date_range, IPO_Calendar, get_engine_by_db_params
from dags.db_query_creator import get_scalar_aggregation_from_table
from config import HOST, DATABASE, USER, PASSWORD
from sqlalchemy import create_engine, select, func, Table, MetaData, and_, or_

# PostgreSQL connection parameters
db_params = {
    "host": "postgres",
    "database": DATABASE,
    "user": USER,
    "password": PASSWORD,
}
engine = get_engine_by_db_params(db_params)
# engine = create_engine(f"postgresql://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}/{db_params["database"]}")
metadata = MetaData(bind=engine)

def get_min_max_value_from_table(table_name, value):
    # EXAMPLE:
    # get_min_max_value_from_table(table_ipo_calendar.name, table_ipo_calendar.columns.date)
    table = Table(table_name, metadata, autoload=True)
    min_value_statement = get_scalar_aggregation_from_table(table, "min", value)
    max_value_statement = get_scalar_aggregation_from_table(table, "max", value)
    min_value = get_one_result_with_query(min_value_statement)
    max_value = get_one_result_with_query(max_value_statement)

    return min_value, max_value

def get_one_result_with_query(query):
    with engine.connect() as conn:
        result = conn.execute(query)
        one_result = result.scalar()
    return one_result

def check_if_records_exist(table_name):
    table = Table(table_name, metadata, autoload=True)
    query = get_scalar_aggregation_from_table(table, "count", "date")
    print(query)
    row_count = get_one_result_with_query(query)
    print(f"RowCount is: '{row_count}'")
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
                print("NO DELETION CURRENTLY - AS ONLY 25 REQAUEST PER DAY ALLOWED ON API")
                print(f"Deleted {len(rows_to_delete)} record(s) where '{column_name}' = '{value}'.")

                return True
            else:
                print(f"The value '{value}' does not exist in column '{column_name}' of table '{table_name}'.")

                return False

def get_entries(year, month):
    date_from, date_to = build_date_range(year, month)
    table = Table("IPO_Calendar", metadata, autoload=True)

    where_condition = and_(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to,
        or_(IPO_Calendar.symbol != None, IPO_Calendar.symbol.isnot(None))  # Checking for symbol not being None
    )
    select_statement = select([IPO_Calendar.date, IPO_Calendar.symbol]).where(where_condition)

    with engine.connect() as conn:
        result = conn.execute(select_statement)
    return(result)

def get_symbols(year, month):
    date_from, date_to = build_date_range(year, month)
    where_condition = and_(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to,
        or_(IPO_Calendar.symbol != None,
            IPO_Calendar.symbol != "",
            IPO_Calendar.symbol.isnot(None))  # Checking for symbol not being None
    )

    select_statement = select([IPO_Calendar.symbol]).where(where_condition)
    print ("SELECT-----")
    print(select_statement)
    with engine.connect() as conn:
        result = conn.execute(select_statement)

    raw_strings = [item[0] for item in result]

    return(raw_strings)