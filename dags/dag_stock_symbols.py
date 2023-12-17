

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from dba.db_model import StockSymbols
from dba_helper import engine, db_params, migrate_data
from get_sources import get_stock_symbols
from sqlalchemy import create_engine, MetaData, Table, exc

metadata = MetaData(bind=engine)

def create_table_if_not_exist():
    if not metadata.tables.get('StockSymbols'):
        StockSymbols.__table__.create(engine, checkfirst=True)

def write_df_to_postgres():

        print('##READ IPO DATA INTO DF##')
        df = get_stock_symbols()
        print(df.head())

        print('##WRITE DF IPO DATA TO POSTGRES##')
        with engine.connect() as conn:
            print('##BEGIN TRANSACTION##')
            trans = conn.begin()
            try:

                print('##WRTIE DF TO_SQL##')
                df.to_sql('StockSymbols', conn, if_exists='replace', index=False)

                print('##COMMIT TRANSACTION##')
                trans.commit()
            except exc.SQLAlchemyError as e:
                print(f"Error occurred: {e}")
                trans.rollback()
                raise

dag = DAG(
    'load_stockSymbol_data_to_postgres',
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
)

create_table_task = PythonOperator(
    task_id='create_table_task',
    python_callable=create_table_if_not_exist,
    dag=dag
)

write_symbols_task = PythonOperator(
    task_id='write_symbols_task',
    python_callable=write_df_to_postgres,
    dag=dag
)

# task flow
create_table_task >> write_symbols_task