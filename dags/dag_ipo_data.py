import pandas as pd
import psycopg2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from config import HOST, DATABASE, USER, PASSWORD
from sources import get_ipo_data


def write_df_to_postgres():
    df = get_ipo_data()
    print('##DEBUG MESSAGE##')
    print(df.head())
    # PostgreSQL connection parameters
    db_params = {
        'host': HOST,
        'database': DATABASE,
        'user': USER,
        'password': PASSWORD,
    }

    # Connect to the database
    conn = psycopg2.connect(**db_params)

    # Write the DataFrame to the PostgreSQL table
    df.to_sql('IPO_Calendar', conn, if_exists='replace', index=False)

    # Close the database connection
    conn.close()

dag = DAG(
    'write_df_to_postgres',
    start_date=datetime(2023, 1, 1),  # Adjust the start date
    schedule_interval=None,  # Set the scheduling interval (e.g., '@once' or a cron schedule)
)

write_to_postgres_task = PythonOperator(
    task_id='write_to_postgres_task',
    python_callable=write_df_to_postgres,
    dag=dag
)

# Other tasks (if needed) before writing to PostgreSQL
write_to_postgres_task