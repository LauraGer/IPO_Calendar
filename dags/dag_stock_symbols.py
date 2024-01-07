""""
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
# DESCRIPTION TO ADD

from app.dba.models import StockSymbols
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from db_helper import engine, metadata
from get_sources import get_stock_symbols
from sqlalchemy import  exc


def create_table_if_not_exist():
    if not metadata.tables.get("StockSymbols"):
        StockSymbols.__table__.create(engine, checkfirst=True)


def write_df_to_postgres():
        df = get_stock_symbols()
        print(df.head())

        print("##WRITE DF IPO DATA TO POSTGRES##")
        with engine.connect() as conn:
            print("##BEGIN TRANSACTION##")
            trans = conn.begin()
            try:

                print("##WRTIE DF TO_SQL##")
                df.to_sql("StockSymbols", conn, if_exists="replace", index=False)

                print("##COMMIT TRANSACTION##")
                trans.commit()
            except exc.SQLAlchemyError as e:
                print(f"Error occurred: {e}")
                trans.rollback()
                raise

dag = DAG(
    "load_stockSymbol_data_to_postgres",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
)

create_table_task = PythonOperator(
    task_id="create_table_task",
    python_callable=create_table_if_not_exist,
    dag=dag
)

write_symbols_task = PythonOperator(
    task_id="write_symbols_task",
    python_callable=write_df_to_postgres,
    dag=dag
)

# task flow
create_table_task >> write_symbols_task