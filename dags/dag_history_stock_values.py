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

# This DAG saves historic stock data into postgres database.
# First taks is to create the postgres table if it not existing.
# The load task is iterating through IPO date.
# It iterates from the past to future IPOs and gets historical data by symbol.
# If the symbol keeps already data in the db it will move on.
# This is done like that, because the free API only allowes 25 calls per day.
import psycopg2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from app.dba.models import MonthlyHistoryByStockSymbol
from dags.db_helper import engine, db_params, metadata, check_if_value_exist_and_drop, get_symbols, get_min_max_value_from_table
from dags.get_sources import get_historical_values_by_symbol
from datetime import date, datetime
from sqlalchemy import Table

today = date.today()
history_table_name = "MonthlyHistoryByStockSymbol"

def create_table_if_not_exist():
    if not metadata.tables.get(history_table_name):
        MonthlyHistoryByStockSymbol.__table__.create(engine, checkfirst=True)

def load_by_month_ipo_history():
    table_ipo_calendar = Table("IPO_Calendar", metadata, autoload=True)
    min_date, max_date = get_min_max_value_from_table(table_ipo_calendar.name, table_ipo_calendar.columns.date)
    year_min = min_date.year
    print(f"year_min='{year_min}'")
    year_max = max_date.year
    print(f"year_min='{year_min}'")
    cnt = 0
    for year in range(year_min, year_max + 1):
        start_month = min_date.month if year == year_min else 1
        end_month = max_date.month if year == year_max else 12
        if cnt > 25:
            break
        for month in range(start_month, end_month + 1):
            try:
                symbols = get_symbols(year, month)
                for symbol in symbols:
                    if cnt > 25:
                        print(cnt)
                        return
                    if check_if_value_exist_and_drop(history_table_name, "symbol", symbol):
                        continue

                    historical_data = get_historical_values_by_symbol(symbol)
                    # file_path = f"output_{symbol}.json"
                    # # Write the data to the JSON file
                    # with open(file_path, "w") as json_file:
                    #     print(f"WRITE JSON to {file_path}")
                    #     json.dump(historical_data, json_file)
                    # if historical_data or
                    # cnt += 1
                    if historical_data == "LIMIT REACHED":
                        print("############################################")
                        print("Limit for today reached - continue tomorrow!")
                        print("############################################")
                        return
                    if historical_data:
                        cnt += 1
                        monthly_history_table = Table(history_table_name, metadata, autoload=True)
                        with engine.connect() as conn:
                            conn.execute(monthly_history_table.insert(), historical_data)
            except psycopg2.OperationalError as e:
                print(f"Error connecting to the database: {e}")
                print(f"db_params: {db_params}")
            except Exception as e:
                print(f"An error occurred: {e}")

# DAG DEFINITION AND SCHEDULE
dag_load_monthly_history_data = DAG(
    "load_monthly_history_stock_values",
    start_date=datetime(2023, 1, 1),
    schedule_interval="0 7 * * *",  # Schedule for 7 AM daily
    catchup=False
)
# TASKS
create_table_task = PythonOperator(
    task_id="create_table_task",
    python_callable=create_table_if_not_exist,
    dag=dag_load_monthly_history_data
)
load_data_task = PythonOperator(
    task_id="load_data_task",
    python_callable=load_by_month_ipo_history,
    dag=dag_load_monthly_history_data
)
# TASK FLOW
create_table_task >> load_data_task