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

# This DAG load IPOs into postgres table.
# First it checks and creates if the table exists.
# It also creates the table if it does not exist.
# In the write task it set the initial loading date to 2010-01-01.
# The end date is 90 days in the future.
# The first load gets all historical data from now up to 90 days in advance.
# If data exists already it takes the latest date as start date.
# Just to reduce potential redundancy there is a delete method which removes based on symbol,name and keeps the latest IPO
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from app.dba.models import IPO_Calendar
from dags.get_db_data import engine, db_params, metadata
from datetime import date, timedelta, datetime
from dags.get_sources import get_ipo_data, get_quarter_range
from sqlalchemy import Table, exc, func, select

today = date.today()

def create_table_if_not_exist():
    if not metadata.tables.get('IPO_Calendar'):
        IPO_Calendar.__table__.create(engine, checkfirst=True)

def write_df_to_postgres():
    ###################################################
    # gets per quater IPO Calendar data from finnhub.io.
    # data gets written in postgres IPO_Calendar table.
    ###################################################
    table_ipo_calendar = Table("IPO_Calendar", metadata, autoload=True)
    start = datetime(2010,1,1)
    end=today + timedelta(days=90)
    try:
        processing_month = start
        while processing_month.strftime('%Y-%m-%d') < end.strftime('%Y-%m-%d'):
            processing_start, processing_end = get_quarter_range(processing_month)
            df = get_ipo_data(processing_start, processing_end)
            print(f"RECEIVED for start='{processing_start}'and end='{processing_end}' - '{len(df)}' RECORDS")
            # Convert DataFrame to a list of dictionaries for bulk insert
            data = df.to_dict(orient='records')
            with engine.connect() as conn:
                conn.execute(table_ipo_calendar.insert(), data)
            #set values for next iteration
            processing_month = processing_end

    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        print(f"db_params: {db_params}")

    except Exception as e:
        print(f"An error occurred: {e}")

def remove_duplicates():
        distinct_table = Table("IPO_Calendar", metadata, autoload=True)
        #get min ipo_calender_id grouped by symbols and delete them
        query = distinct_table.delete().where(
            distinct_table.c.ipo_calendar_id.notin_(
                select([func.min(distinct_table.c.ipo_calendar_id)]).group_by(distinct_table.c.symbol, distinct_table.c.name)
            )
        )
        with engine.connect() as conn:
            trans = conn.begin()
            try:
                conn.execute(query)
                trans.commit()
            except exc.SQLAlchemyError as e:
                print(f"Error occurred: {e}")
                trans.rollback()
                raise

# DAG DEFINITION AND SCHEDULE
dag_load_ipo_data = DAG(
    'load_ipo_data_to_postgres',
    start_date=datetime(2023, 1, 1),
    schedule_interval='0 7 * * 1',  # Schedule for Monday at 7 AM
    catchup=False
)
# TASKS
create_table_task = PythonOperator(
    task_id='create_table_task',
    python_callable=create_table_if_not_exist,
    dag=dag_load_ipo_data
)
write_task = PythonOperator(
    task_id='write_dataframe_to_postgres_task',
    python_callable=write_df_to_postgres,
    dag=dag_load_ipo_data
)
remove_duplicates_task = PythonOperator(
    task_id='remove_duplicates_task',
    python_callable=remove_duplicates,
    dag=dag_load_ipo_data
)
# TASK FLOW
create_table_task >>  write_task >> remove_duplicates_task



# def copy_data_into_archive():
#     table_ipo_calendar = Table("IPO_Calendar", metadata, autoload=True)
#     table_ipo_calendar_archive = Table("IPO_CalendarArchive", metadata, autoload=True)
#     records_exist = check_if_records_exist(table_ipo_calendar)
#     if records_exist:
#         columns = [
#             table_ipo_calendar_archive.c[name]
#             for name in table_ipo_calendar_archive.columns.keys()
#             if name not in "ipo_calendar_id"
#         ]
#         copy_query = table_ipo_calendar_archive.insert().from_select(
#             columns,
#             table_ipo_calendar.select().with_only_columns([
#                 cast(table_ipo_calendar.c.date, Date),
#                 table_ipo_calendar.c.exchange,
#                 table_ipo_calendar.c.name,
#                 table_ipo_calendar.c.numberOfShares,
#                 table_ipo_calendar.c.price,
#                 table_ipo_calendar.c.status,
#                 table_ipo_calendar.c.symbol,
#                 cast(table_ipo_calendar.c.totalSharesValue, Float),
#                 func.now().label('timestamp_column')
#             ])
#         )
#         print(f"###QUERY:{copy_query}")
#         with engine.connect() as conn:
#             trans = conn.begin()
#             try:
#                 conn.execute(copy_query)

#                 trans.commit()
#             except exc.SQLAlchemyError as e:
#                 print(f"Error occurred: {e}")

#                 trans.rollback()
#                 raise

# def truncate_table_ipo_calendar():
#     table_ipo_calendar = Table("IPO_Calendar", metadata, autoload=True)
#     with engine.connect() as conn:
#         trans = conn.begin()
#         try:
#             delete_query = table_ipo_calendar.delete()
#             conn.execute(delete_query)
#             trans.commit()
#         except exc.SQLAlchemyError as e:
#             print(f"Error occurred: {e}")
#             trans.rollback()
#             raise