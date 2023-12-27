from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
# from dba_helper import engine
from datetime import datetime

# metadata = MetaData(bind=engine)


def remove_duplicates():
    import sys
    print(f"SYSPATH: {sys.path}")


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