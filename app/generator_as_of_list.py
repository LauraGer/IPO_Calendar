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
from app.fetcher_data import DataFetcher
from dba.crud import BulkInsert, Create, Update
from dba.models_app import AsOfList
from utils.check import check_result
from utils.get_sources import PoligonIo, Finnhub, AlphaVantage
from utils.schema import ColumnMapping
from app.config import db_params_app
from collections import defaultdict

def load_search_symbols_historical_data(symbols, stock_source):
    # keys_monthly_data = ColumnMapping.expected_fields_as_of_history
    try:
        processed = []
        unprocessed = []
        print(symbols)
        if isinstance(symbols, list):
            # If symbols is already a list, no need to split
            symbols = [value.strip() for value in symbols]
        else:
            # If symbols is a string, split it by comma
            symbols = [value.strip() for value in symbols.split(",")]

        for symbol in symbols:
            if symbol:
                print(symbol)

                if stock_source == "Polygon":
                    monthly_data = PoligonIo.get_monthly_historical_data(symbol)
                elif stock_source == "Alpha Vantage":
                    monthly_data = AlphaVantage.get_historical_values_by_symbol(symbol)
                elif stock_source == "FMP":
                    monthly_data = None
                elif stock_source == "Finnhub":
                    monthly_data = Finnhub.get_monthly_historical_data(symbol)
                print("MONTHLY DATA")
                print(monthly_data)
                if monthly_data:
                    processed.insert(1, symbol)
                    print("BEFOR IS FIT")
                    # is_fit = check_result(monthly_data, keys_monthly_data)
                    # print(monthly_data)
                    is_fit = True
                    print(is_fit)
                    if is_fit:
                        cnt_bulk, cnt_update = BulkInsert.bulk_insert_or_replace(monthly_data, symbol, db_params_app)
                else:
                    unprocessed.insert(1, symbol)

        return processed, unprocessed, cnt_bulk, cnt_update
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

def process_list(as_of_list):
    as_of_list_instance = AsOfList(
        listname=as_of_list["listname"],
        as_of_date=as_of_list["as_of_date"],
        symbol=as_of_list["symbol"],
        volume=as_of_list["volume"],
        as_of_price=as_of_list["as_of_price"]
    )
    try:
        # if as_of_list["is_new"]:
        Create.create_as_of_list_record(as_of_list_instance, db_params_app)
        # else:
        #     Update.update_list(as_of_list_instance, db_params_app)

        return as_of_list["listname"]
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

def process_query(value, type):
    try:
        print("hello")
        if type == "listName":
            query_result = DataFetcher.data_get_list_details(value)
        elif type == "asOfDateChange":
            print(value)
            query_result = 666.0

        return query_result
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")