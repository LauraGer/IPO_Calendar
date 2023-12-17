import psycopg2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from dba.db_model import IPO_Calendar, IPO_CalendarArchive
from dba_helper import engine, db_params, migrate_data
from get_sources import get_ipo_data
from sqlalchemy import MetaData, Table, exc, cast, Date, Float, func, select

metadata = MetaData(bind=engine)
table_ipo_calendar = IPO_Calendar.__table__

def create_table_if_not_exist():
    if not metadata.tables.get('IPO_Calendar'):
        IPO_Calendar.__table__.create(engine, checkfirst=True)

    if not metadata.tables.get('IPO_CalendarArchive'):
        IPO_CalendarArchive.__table__.create(engine, checkfirst=True)


def write_df_to_postgres():
    try:
        df = get_ipo_data()
        df.to_sql('IPO_Calendar', engine, if_exists='replace', index=False)

    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        print(f"db_params: {db_params}")

    except Exception as e:
        print(f"An error occurred: {e}")


def copy_data_into_archive():
    source_table = Table("IPO_Calendar", metadata, autoload=True)
    destination_table = Table("IPO_CalendarArchive", metadata, autoload=True)

    columns = [
        destination_table.c[name]
        for name in destination_table.columns.keys()
        if name not in "ipo_calendar_id"
    ]
    print(f"COLUMNS: {columns}")
    copy_query = destination_table.insert().from_select(
        columns,
        source_table.select().with_only_columns([
            cast(source_table.c.date, Date),
            source_table.c.exchange,
            source_table.c.name,
            source_table.c.numberOfShares,
            source_table.c.price,
            source_table.c.status,
            source_table.c.symbol,
            cast(source_table.c.totalSharesValue, Float),
            func.now()
        ])
    )
    print(f"QUERY: {copy_query}")
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(copy_query)

            trans.commit()
        except exc.SQLAlchemyError as e:
            print(f"Error occurred: {e}")

            trans.rollback()
            raise

def remove_duplicates():

        distinct_table = Table("IPO_CalendarArchive", metadata, autoload=True)

        query = distinct_table.delete().where(
            distinct_table.c.ipo_calendar_id.notin_(
                select([func.min(distinct_table.c.ipo_calendar_id)]).group_by(distinct_table.c.symbol)
            )
        )
        print(f"QUERY: {query}")
        with engine.connect() as conn:
            trans = conn.begin()
            try:
                conn.execute(query)

                trans.commit()
            except exc.SQLAlchemyError as e:
                print(f"Error occurred: {e}")
                trans.rollback()
                raise



def truncate_table_ipo_calendar():

    with engine.connect() as conn:
        trans = conn.begin()
        try:
            delete_query = table_ipo_calendar.delete()
            conn.execute(delete_query)

            trans.commit()
        except exc.SQLAlchemyError as e:
            print(f"Error occurred: {e}")

            trans.rollback()
            raise


# DAG and schedule
dag_load_ipo_data = DAG(
    'load_ipo_data_to_postgres',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
)

# Tasks
create_table_task = PythonOperator(
    task_id='create_table_task',
    python_callable=create_table_if_not_exist,
    dag=dag_load_ipo_data
)

copy_to_archive_task = PythonOperator(
    task_id='copy_to_archive_task',
    python_callable=copy_data_into_archive,
    dag=dag_load_ipo_data
)

truncate_task = PythonOperator(
    task_id='truncate_ipo_calendar_task',
    python_callable=truncate_table_ipo_calendar,
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

# Task flow
create_table_task >> copy_to_archive_task >> truncate_task >> write_task >> remove_duplicates_task