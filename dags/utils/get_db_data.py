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
# This file
"""
from dba.db_helper import build_date_range_year_month, IPO_Calendar, get_engine_by_db_params, MonthlyHistoryByStockSymbol
# from dags.utils.create_db_query import get_scalar_aggregation_from_table, get_list_of_column_values_from_table, get_columns_from_table
from dba.create_db_query import get_scalar_aggregation_from_table, get_query_list_of_column_values_from_table, get_query_columns_from_table
from dags.config import HOST, DATABASE, USER, PASSWORD, relevant_exchange
from sqlalchemy import select, Table, MetaData, and_, or_
from sqlalchemy.orm import sessionmaker

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

def get_session(db_params):
   # Create a session
    engine = get_engine_by_db_params(db_params)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

session = get_session(db_params)

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
    row_count = get_one_result_with_query(query)
    if row_count > 0:
        return True
    else:
        return False


def get_exchanges_from_db():
    table = Table("Exchanges", metadata, autoload=True)
    column_name = "code"

    data_list_query = get_query_list_of_column_values_from_table(table, column_name)

    with engine.connect() as conn:
        result = conn.execute(data_list_query)
        column_data_list = result.fetchall()

        # Extract the values from the list (assuming a single column)
        column_values = [item[0] for item in column_data_list]

        return column_values


def check_if_value_exist(table_name, column_name, value):
    """
    Check if a specific value exists in a given column of a table and delete corresponding rows if found.

    Parameters:
    - table_name: Name of the table to check and perform deletion.
    - column_name: Name of the column within the table to check for the specified value.
    - value: The value to check for and use as a condition for deletion.

    Returns:
    - True if the value is found and corresponding rows are deleted; False otherwise.

    Notes:
    - This function checks if a specified value exists in a given column of a table.
    - If the value is found, the corresponding rows are deleted from the table.
    - The function handles the case where the specified column does not exist in the table.
    - The status of deletion (success or failure) is indicated by the return value.
    - Actual deletion is commented out and marked for future use, as API limitations prevent frequent deletions.

    """
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
                # print("NO DELETION CURRENTLY - AS ONLY 25 REQAUEST PER DAY ALLOWED ON API")
                print(f"{len(rows_to_delete)} record(s) where '{column_name}' = '{value}' exist.")

                return True
            else:
                print(f"The value '{value}' does not exist in column '{column_name}' of table '{table_name}'.")

                return False

def get_entries(year, month):
    """
    Retrieve entries from the IPO Calendar for a specified date range.

    Parameters:
    - year: The year of the date range.
    - month: The month of the date range.

    Returns:
    - Result set containing entries from the IPO Calendar within the specified date range.

    Notes:
    - This function queries entries from the IPO Calendar based on the provided year and month.
    - It constructs a WHERE condition to filter entries within the specified date range.
    - Entries are filtered based on conditions such as date range and non-null symbol values.
    - Example usage is provided in the function's docstring.

    Example:
    - result = get_entries(2023, 5)
    - for row in result:
    -     print(row['date'], row['symbol'])

    """
    date_from, date_to = build_date_range_year_month(year, month)
    # table = Table("IPO_Calendar", metadata, autoload=True)

    # columns_to_fetch = ["date", "symbol"]
    where_condition = and_(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to,
        or_(IPO_Calendar.symbol != None,
            IPO_Calendar.symbol.isnot(None))  # Checking for symbol not being None
    )

    results = (session.query(IPO_Calendar.date,IPO_Calendar.symbol).filter(where_condition).all())
    symbol_list = [result.symbol for result in results if result.symbol != '']

    return(symbol_list)
    # bind_parameters = {
    #     'date_1': date_from,
    #     'date_2': date_to
    # }
    # select_statement = get_query_columns_from_table(metadata, IPO_Calendar.__tablename__, columns_to_fetch, where_condition, **bind_parameters)


    # with engine.connect() as conn:
    #     result = conn.execute(select_statement)
    # return(result)

def get_symbols(year, month):
    """
    Retrieve symbols for IPO events within a specified date range.

    Parameters:
    - year: The year of the date range.
    - month: The month of the date range.

    Returns:
    - List of symbols for IPO events within the specified date range.

    Example:
    - result = get_symbols(2023, 5)
    - print(result)
    - Output: ['AAPL', 'GOOGL', 'AMZN', ...]

    Notes:
    - This function queries symbols for IPO events based on the provided year and month.
    - It constructs a WHERE condition to filter IPO events within the specified date range.
    - Relevant symbols are filtered based on conditions such as date range and non-null symbol values.
    - Example usage is provided in the function's docstring.

    """
    relevant_symbol_list = relevant_exchange
    date_from, date_to = build_date_range_year_month(year, month)

    where_condition = and_(
        IPO_Calendar.date >= date_from,
        IPO_Calendar.date <= date_to,
        or_(IPO_Calendar.symbol.isnot(None),
            IPO_Calendar.symbol.in_(relevant_symbol_list)
            )
        )

    results = (session.query(IPO_Calendar.symbol).filter(where_condition).all())
    symbol_list = [result.symbol for result in results if result.symbol != '']

    return(symbol_list)

def get_historic_data_by_symbol(symbol):
    """
    Retrieve historic data for a specific stock symbol from the database.

    Example Usage:
    - table_name = MonthlyHistoryByStockSymbol.__tablename__
    - columns_to_fetch = ["monthly_history_id", "date", "symbol", "open", "high", "low", "close", "volume"]
    - where_condition = MonthlyHistoryByStockSymbol.symbol == symbol
    - bind_parameters = {'symbol_1': symbol}
    - result_values = get_query_columns_from_table(metadata, table_name, columns_to_fetch, where_condition, **bind_parameters)

    Parameters:
    - symbol: Stock symbol for which historic data is requested.

    Returns:
    - List of dictionaries, where each dictionary represents a row with selected columns.
      The columns include 'monthly_history_id', 'date', 'symbol', 'open', 'high', 'low', 'close', and 'volume'.

    Notes:
    - This function retrieves historical data for a specific stock symbol from the database.
    - It constructs a WHERE condition based on the provided stock symbol.
    - The result is a list of dictionaries, where each dictionary represents a row with the selected columns.
    - Example usage is provided in the function's docstring.

    Example:
    >>> result = get_historic_data_by_symbol('AAPL')
    >>> print(result)
    [{'monthly_history_id': 1, 'date': '2024-01-01', 'symbol': 'AAPL', 'open': 150.0, 'high': 160.0, 'low': 140.0, 'close': 155.0, 'volume': 100000},
     {'monthly_history_id': 2, 'date': '2024-02-01', 'symbol': 'AAPL', 'open': 155.0, 'high': 165.0, 'low': 145.0, 'close': 160.0, 'volume': 110000},
     ...]

    """
    table_name = MonthlyHistoryByStockSymbol.__tablename__
    columns_to_fetch = ["monthly_history_id", "date", "symbol", "open", "high", "low", "close", "volume"]
    where_condition = MonthlyHistoryByStockSymbol.symbol == symbol
    bind_parameters = {'symbol_1': symbol}
    result_values = get_query_columns_from_table(metadata, table_name, columns_to_fetch, where_condition, **bind_parameters)

    print(result_values)
    return(result_values)
