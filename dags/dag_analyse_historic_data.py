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
# This DAG loads historical data per symbol and does some analysis.
# The analysis is stored on a dedicated table in postgres db.

import pandas as pd
from app.core.get_analysis import get_monthly_returns
from dba.models_dag import Analysis_SymbolMonthly
from dba.db_helper import get_history_by_symbol, get_year_month_integer, get_session
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from dags.utils.get_db_data import engine, db_params,metadata, get_historic_data_by_symbol


def create_table_if_not_exist():
    if not metadata.tables.get("Analysis_SymbolMonthly"):
        Analysis_SymbolMonthly.__table__.create(engine, checkfirst=True)

def analyse_monthly_data():
    symbol = "FNGN"

    session = get_session(db_params)
    print("----SESSION-----------")
    print(session)
   # df = get_history_by_symbol(symbol, session)

    columns = ["monthly_history_id", "date", "open", "high", "low", "close", "volume"]

    stock_data = pd.DataFrame(get_historic_data_by_symbol(symbol), columns=columns)

    df = (get_monthly_returns(stock_data))
    print(df)
    df["month_key"] = get_year_month_integer(df["Date"])
    df["symbol"] = symbol

    columns = [ "monthly_history_id", "month_key", "symbol", "monthly_returns"]
    selected_columns_df = df[columns]
    data_to_insert = selected_columns_df.to_dict(orient='records')

    with engine.connect() as connection:
        connection.execute(Analysis_SymbolMonthly.__table__.insert().values(data_to_insert))


dag = DAG(
    "analyse_historical_data",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
)

create_table_task = PythonOperator(
    task_id="create_table_task",
    python_callable=create_table_if_not_exist,
    dag=dag
)

analyse_monthly_data_task = PythonOperator(
    task_id="analyse_monthly_data_task",
    python_callable=analyse_monthly_data,
    dag=dag
)

# task flow
create_table_task >> analyse_monthly_data_task