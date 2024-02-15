from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from dba.db_helper import get_engine_by_db_params
from sqlalchemy import MetaData, Table, exc, func, select
from datetime import datetime

engine = get_engine_by_db_params()
metadata = MetaData(bind=engine)

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
                print('##COMMIT TRANSACTION##')
                trans.commit()
            except exc.SQLAlchemyError as e:
                print(f"Error occurred: {e}")
                trans.rollback()
                raise

dag = DAG(
    'test_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
)

remove_dubplicates_task = PythonOperator(
    task_id='remove_dubplicates_task',
    python_callable=remove_duplicates,
    dag=dag
)

# task flow
remove_dubplicates_task