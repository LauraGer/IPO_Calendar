import psycopg2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from app.dba.models import IPO_Calendar, MonthlyHistoryByStockSymbol
from app.dba.db_helper import get_symbols
from dags.db_helper import engine, db_params, metadata, check_if_value_exist_and_drop
from dags.get_sources import get_historical_values_by_symbol
from datetime import date, datetime
from sqlalchemy import Table, insert

today = date.today()
history_table_name = 'MonthlyHistoryByStockSymbol'

def create_table_if_not_exist():
    if not metadata.tables.get(history_table_name):
        MonthlyHistoryByStockSymbol.__table__.create(engine, checkfirst=True)

def load_by_month_ipo_history():
    year = 2020
    month = 12
    cnt = 0
    try:
        symbols = get_symbols(year, month)
        for symbol in symbols:
            print(symbol)
            if cnt > 1:
                break
            #currently only from output.json - as it need logic to iterate daily 25 IPOs
            if check_if_value_exist_and_drop(history_table_name, 'symbol', symbol):
                continue

            cnt += 1
            historical_data = get_historical_values_by_symbol(symbol)
            if historical_data:
                monthly_history_table = Table(history_table_name, metadata, autoload=True)

                with engine.connect() as conn:
                    conn.execute(monthly_history_table.insert(), historical_data)
            #because only 25 requests per day are possible
            if cnt > 25:
                break


    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        print(f"db_params: {db_params}")

    except Exception as e:
        print(f"An error occurred: {e}")

# DAG DEFINITION AND SCHEDULE
dag_load_monthly_history_data = DAG(
    'load_monthly_history_stock_values',
    start_date=datetime(2023, 1, 1),
    schedule_interval='0 7 * * *',  # Schedule for 8 AM daily
    catchup=False
)

# TASKS
create_table_task = PythonOperator(
    task_id='create_table_task',
    python_callable=create_table_if_not_exist,
    dag=dag_load_monthly_history_data
)

load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_by_month_ipo_history,
    dag=dag_load_monthly_history_data
)

# TASK FLOW
create_table_task >> load_data_task