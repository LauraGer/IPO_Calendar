

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from dba.db_model import IPO_Calendar, IPO_CalendarArchive
from dba_helper import engine, db_params, migrate_data
from get_sources import get_ipo_data
from sqlalchemy import create_engine, MetaData, Table, exc
from datetime import datetime
import pandas as pd
import psycopg2

metadata = MetaData(bind=engine)

def create_table_if_not_exist():
    #migrate_data()
    #Base.metadata.create_all(engine)
    if not metadata.tables.get('IPO_Calendar'):
    # if not engine.dialect.has_table(engine, 'IPO_Calendar'):
        IPO_Calendar.__table__.create(engine, checkfirst=True)
    check = str(metadata.tables.get('IPO_CalendarArchive'))
    print( f"CHECK IF EXISTS--------{check}")
    if not metadata.tables.get('IPO_CalendarArchive'):
    # if not engine.dialect.has_table(engine, 'IPO_Calendar'):
        IPO_CalendarArchive.__table__.create(engine, checkfirst=True)

def write_df_to_postgres():
    try:

        print('##READ IPO DATA INTO DF##')
        df = get_ipo_data()

        print('##WRITE DF IPO DATA TO POSTGRES##')
        df.to_sql('IPO_Calendar', engine, if_exists='replace', index=False)


    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        print(f"db_params: {db_params}")

    except Exception as e:
        print(f"An error occurred: {e}")


def copy_data_into_archive():

    # Define source and destination tables
    source_table = Table('IPO_Calendar', metadata, autoload=True)
    destination_table = Table('IPO_CalendarArchive', metadata, autoload=True)
    
    # Execute SQL to copy data from source to destination
    columns = [source_table.c[name] for name in source_table.columns.keys()]
    copy_query = destination_table.insert().from_select(
        columns,
        source_table.select()
    )
    
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(copy_query)
            trans.commit()  # Commit the transaction
        except exc.SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            trans.rollback()  # Rollback changes if an exception occurs
            raise


dag = DAG(
    'load_ipo_data_to_postgres',
    start_date=datetime(2023, 1, 1),  # Adjust the start date
    schedule_interval=None,  # Set the scheduling interval (e.g., '@once' or a cron schedule)
)

create_table_task = PythonOperator(
    task_id='create_table_task',
    python_callable=create_table_if_not_exist,
    dag=dag
)

copy_to_archive_task = PythonOperator(
    task_id='copy_to_archive_task',
    python_callable=copy_data_into_archive,
    dag=dag
)

write_task = PythonOperator(
    task_id='write_dataframe_to_postgres_task',
    python_callable=write_df_to_postgres,
    dag=dag
)


# task flow
create_table_task >> copy_to_archive_task >> write_task