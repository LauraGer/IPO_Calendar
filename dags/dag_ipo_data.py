import psycopg2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import date, timedelta, datetime
from app.dba.models import IPO_Calendar, IPO_CalendarArchive
from dags.db_helper import engine, db_params, check_if_records_exist, metadata
from get_sources import get_ipo_data
from sqlalchemy import Table, exc, cast, Date, Float, func, select

today = date.today()

def create_table_if_not_exist():
    if not metadata.tables.get('IPO_Calendar'):
        IPO_Calendar.__table__.create(engine, checkfirst=True)

    # if not metadata.tables.get('IPO_CalendarArchive'):
    #     IPO_CalendarArchive.__table__.create(engine, checkfirst=True)


def write_df_to_postgres():
    table_ipo_calendar = Table("IPO_Calendar", metadata, autoload=True)
    #initial start - get IPOs from 2010
    start=(2010,1,1)
    end=today + timedelta(days=90)
    try:
        records_exist = check_if_records_exist("IPO_Calendar")
        if records_exist:
            #get latest date from IPO_Calender and take it as start date
            max_date_statement = select([func.max(table_ipo_calendar.columns.date)])

            with engine.connect() as conn:
                result = conn.execute(max_date_statement)
                max_date = result.scalar()
            if max_date == end:
                # all records are already in the db
                return
            start=max_date
        # get IPO data
        df = get_ipo_data(start,end)

        ipo_calendar_table = Table('IPO_Calendar', metadata, autoload=True)  # Load the existing table structure
        # Convert DataFrame to a list of dictionaries for bulk insert
        data = df.to_dict(orient='records')
        with engine.connect() as conn:
            conn.execute(ipo_calendar_table.insert(), data)

    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        print(f"db_params: {db_params}")

    except Exception as e:
        print(f"An error occurred: {e}")


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



def truncate_table_ipo_calendar():
    table_ipo_calendar = Table("IPO_Calendar", metadata, autoload=True)
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


# DAG DEFINITION AND SCHEDULE
dag_load_ipo_data = DAG(
    'load_ipo_data_to_postgres',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
)

# TASKS
create_table_task = PythonOperator(
    task_id='create_table_task',
    python_callable=create_table_if_not_exist,
    dag=dag_load_ipo_data
)

# copy_to_archive_task = PythonOperator(
#     task_id='copy_to_archive_task',
#     python_callable=copy_data_into_archive,
#     dag=dag_load_ipo_data
# )

# truncate_task = PythonOperator(
#     task_id='truncate_ipo_calendar_task',
#     python_callable=truncate_table_ipo_calendar,
#     dag=dag_load_ipo_data
# )

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