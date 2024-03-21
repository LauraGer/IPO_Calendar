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

# This file gets data from various sources and APIs

import finnhub
import json
import os
import pandas as pd
import requests
from dags.config import  ALPHA_MONTHLY_URL, FINNHUB_API_KEY, FMP_KEY, POLYGON_KEY, local_data_dir
from datetime import datetime
from utils.schema import ColumnMapping
from utils.data_transformation import update_timestamps

finnhub_api_key = FINNHUB_API_KEY
finnhub_client = finnhub.Client(api_key=finnhub_api_key)
unknown_file_path = 'unknown_symbols.json'
# create unknown_file_path if not existing
if not os.path.exists(unknown_file_path):
    with open(unknown_file_path, 'w') as file:
        json.dump(unknown_file_path, file, indent=2)

def get_str_date(date):
    try:
        date_obj = datetime.combine(date)
        date_str = date_obj.strftime('%Y-%m-%d')

        return date_str
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")


def get_quarter_range(processing_month):
    """
    Calculate the start and end dates for a processing period based on the given month.

    Parameters:
    - processing_month (datetime): The month for which the processing period is calculated.

    Returns:
    - processing_start (datetime): The start date of the processing period.
    - processing_end (datetime): The end date of the processing period.

    Example:
    processing_month = datetime(2023, 5, 15)
    calculate_processing_period(processing_month)
    # Returns (datetime(2023, 5, 1), datetime(2023, 8, 1))
    """
    try:
        month_day = 1
        current_quarter = (processing_month.month - 1) // 3 + 1
        next_quarter_start_month = current_quarter * 3 + 1 if current_quarter < 4 else 1
        current_year = processing_month.year
        next_year = current_year if next_quarter_start_month != 1 else current_year + 1
        month = processing_month.month
        processing_start = datetime(current_year, month, int(month_day))
        processing_end = datetime(next_year, next_quarter_start_month, int(month_day))

        return processing_start, processing_end
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")


def get_ipo_data(start, end, finnhub_client=finnhub_client):
    """
    Retrieve Initial Public Offering (IPO) data within a specified date range.

    Parameters:
    - start (str): Start date of the desired IPO data range (formatted as 'YYYY-MM-DD').
    - end (str): End date of the desired IPO data range (formatted as 'YYYY-MM-DD').
    - finnhub_client (FinnhubClient, optional): An instance of the FinnhubClient class.
      Defaults to a pre-initialized FinnhubClient.

    Returns:
    - initial_df (DataFrame): A pandas DataFrame containing IPO data for the specified date range.

    Example:
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    client = FinnhubClient(api_key='your_api_key')
    get_ipo_data(start_date, end_date, finnhub_client=client)
    # Returns a DataFrame with IPO data for the specified date range.
    """
    try:
        ipo_data = finnhub_client.ipo_calendar(_from=start, to=end)
        initial_df = pd.json_normalize(ipo_data, "ipoCalendar")

        return initial_df
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")


def write_data_in_json_file(file_path, data):
    """
    Write data to a JSON file, either creating a new file or appending to an existing one.

    Parameters:
    - file_path (str): The path to the JSON file.
    - data (dict or list): The data to be written to the JSON file.

    Example:
    file_path = 'example.json'
    data_to_write = {"name": "John Doe", "age": 30, "city": "Example City"}
    write_data_in_json_file(file_path, data_to_write)
    # Writes data_to_write to 'example.json' or appends it if the file exists.
    """
    try:
        existing_data = {}
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
        existing_data.append(data)
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

def check_data_in_json_file(target_data):
    """
    Check if specified data is present in a JSON file.

    Parameters:
    - target_data (str, list, dict, etc.): The data to be checked in the JSON file.

    Returns:
    - result_tuple (tuple): A tuple containing a boolean indicating if all target data is found,
      and a list of items not found in the JSON file.

    Example:
    target_data_single = "John Doe"
    check_data_in_json_file(target_data_single)
    # Returns (True, []) if "John Doe" is found in the JSON file, otherwise (False, ["John Doe"]).

    target_data_list = ["John Doe", "Jane Smith", "Bob Johnson"]
    check_data_in_json_file(target_data_list)
    # Returns (True, []) if all items are found in the JSON file,
    # otherwise (False, ["Jane Smith", "Bob Johnson"]).
    """
    try:
        with open(unknown_file_path, 'r') as file:
            existing_data = json.load(file)
            not_found_items = []

            # If target_data is a list, check each item
            if isinstance(target_data, list):
                for item in target_data:
                    if item not in existing_data:
                        not_found_items.append(item)
                return (len(not_found_items) < len(target_data), not_found_items)

            else:

                return (target_data in existing_data, [])
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")


def is_json(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("{}")  # Write an empty JSON object
            print(f"Empty JSON file created: {file_path}")
    #File exist
    return True


def is_value_in_jsonfile(json_path, target_value):
    try:
        with open(json_path, 'r') as file:
            json_data = json.load(file)
            if target_value in json_data:
                return True
    except FileNotFoundError:
        print(f"[{__name__}] - File not found: {json_path}")
    except json.JSONDecodeError:
        print(f"[{__name__}] - Invalid JSON format in file: {json_path}")
    return False

def get_exchanges_from_csv():
    try:
        csv_file_name = "20240118_FinnhubExchanges.csv"
        csv_file_path = os.path.join(local_data_dir, csv_file_name)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)
        print(df)
        return df
    except:
        print(f"[{__name__}] - You need to safe the file as '{csv_file_path}'")
        print(f"[{__name__}] - from url: https://docs.google.com/spreadsheets/d/1I3pBxjfXB056-g_JYf_6o3Rns3BV2kMGG1nCatb91ls/edit#gid=0")

def get_stock_symbols(exchange, finnhub_client=finnhub_client):
    print(f"GET_STOCK_SYMBOLS ECHANGE: '{exchange}'")
    try:
        stock_symbols_data = finnhub_client.stock_symbols(exchange)
        df = pd.DataFrame(stock_symbols_data)

        return df
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")


def get_stock_details_with_exchange_fmp_api(fmp_key=FMP_KEY):
    try:
        fmp_exchange_url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={fmp_key}"
        request_json = requests.get(fmp_exchange_url)
        exchange_data = request_json.json()
        exchange_data = pd.json_normalize(exchange_data)

        return exchange_data
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")

class AlphaVantage:
    def get_historical_values_by_symbol(symbol):
        """
        Get historical monthly values for a given stock symbol using the Alpha Vantage API.

        Parameters:
        - symbol (str): The stock symbol for which historical data is requested.

        Returns:
        - result (list or str): If successful, returns a list of dictionaries containing historical monthly data
        including open, high, low, close, volume, and date. If the symbol is empty, returns "NO SYMBOL."
        If the API request fails, writes the symbol to a JSON file and returns "NO DATA." If the symbol already exists
        in the JSON file, returns "NO DATA AVAILABLE." If the API request limit is reached, returns "LIMIT REACHED."

        Example:
        symbol_to_query = "AAPL"
        get_historical_values_by_symbol(symbol_to_query)
        # Returns a list of historical monthly data for Apple Inc. if the API request is successful.
        """
        try:
            is_json(unknown_file_path)

            if is_value_in_jsonfile(unknown_file_path, symbol):
                return "NO DATA AVAILABLE"
            if symbol == "":
                return "NO SYMBOL"

            url = ALPHA_MONTHLY_URL.replace("##SYMBOL##", symbol)
            print(url)
            request_json = requests.get(url)
            print(request_json)
            data = request_json.json()
            print(data)

            if "Error Message" in data:
                write_data_in_json_file(unknown_file_path, symbol)

                return "NO DATA"

            if "Meta Data" in data:
                monthly_data = [{"symbol": data["Meta Data"]["2. Symbol"], "date": key, **value, }
                                for key, value in data.get("Monthly Time Series", {}).items()]
                column_mapping = ColumnMapping.alpha_historical_data
                print(column_mapping)
                monthly_data = [{column_mapping.get(col, col): val for col, val in entry.items()} for entry in monthly_data]
                print(monthly_data)
                return monthly_data

            else:
                return "LIMIT REACHED"
        except Exception as e:
            print(f"[{__name__}] - an error occurred: {e}")

class Finnhub:
    def get_monthly_historical_data(symbol):
        """
        Get monthly aggregated historical stock data from Finnhub API for a specific symbol.

        Parameters:
            symbol (str): The stock symbol (e.g., AAPL for Apple Inc.).
            start_date (str): The start date of the historical data (format: 'YYYY-MM-DD').
            end_date (str): The end date of the historical data (format: 'YYYY-MM-DD').

        Returns:
            dict: Monthly aggregated historical stock data in JSON format.
        """
        base_url = 'https://finnhub.io/api/v1'
        endpoint = '/stock/candle'
        end_date = datetime.today().strftime('%Y-%m-%d')

        params = {
            'symbol': symbol,
            'resolution': 'M',  # Monthly resolution
            'from': '2023-01-01',
            'to': end_date,
            'token': finnhub_api_key  # Replace 'your_finnhub_api_token' with your actual API token
        }
        response = requests.get(base_url + endpoint, params=params)
        data = response.json()
        return data

class PoligonIo:
    def get_monthly_historical_data(symbol):
        """
        Get monthly aggregated historical stock data from POLGON API for a specific symbol.

        Parameters:
            symbol (str): The stock symbol (e.g., AAPL for Apple Inc.).
            start_date (str): The start date of the historical data (format: 'YYYY-MM-DD').
            end_date (str): The end date of the historical data (format: 'YYYY-MM-DD').

        Returns:
            dict: Monthly aggregated historical stock data in JSON format.
        """
        base_url = 'https://api.polygon.io/v2'
        start_date = "2020-01-01"
        end_date = datetime.today().strftime('%Y-%m-%d')
        endpoint = f"/aggs/ticker/{symbol}/range/1/month/{start_date}/{end_date}"

        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": 50000,
            'apiKey': POLYGON_KEY
        }
        response = requests.get(base_url + endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            update_timestamps(data, "t", "%Y-%m-%d")
            monthly_data = [{"symbol": data["ticker"], "date": result["t"], **{k: result[k] for k in ["o", "h", "l", "c", "v"]}}
                for result in data.get("results", [])]
            column_mapping = ColumnMapping.poligon_historical_data
            monthly_data = [{column_mapping[key] if key in column_mapping else key: value for key, value in entry.items()} for entry in monthly_data]

            return monthly_data

        else:
            print("Failed to fetch data:", response.status_code)