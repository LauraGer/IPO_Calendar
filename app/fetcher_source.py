import finnhub
import json
import os
import pandas as pd
import requests
from dags.config import FINNHUB_API_KEY, ALPHA_MONTHLY_URL, FMP_KEY, local_data_dir
from datetime import datetime

finnhub_api_key = FINNHUB_API_KEY
finnhub_client = finnhub.Client(api_key=finnhub_api_key)
unknown_file_path = 'unknown_symbols.json'

stock_sources = { "Finnhub": False
                , "Alpha Vantage": True
                , "FMP": False
                , "Polygon": True
                }

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

        url = ALPHA_MONTHLY_URL.replace("##SYMBOL##", symbol)
        request_json = requests.get(url)
        data = request_json.json()

        if "Error Message" in data:
            write_data_in_json_file(unknown_file_path, symbol)

            return "NO DATA"

        if "Meta Data" in data:
            monthly_data = [{"symbol": data["Meta Data"]["2. Symbol"], "date": key, **value, }
                            for key, value in data.get("Monthly Time Series", {}).items()]
            column_mapping = {"1. open": "open",
                            "2. high": "high",
                            "3. low": "low",
                            "4. close": "close",
                            "5. volume": "volume"}
            monthly_data = [{column_mapping.get(col, col): val for col, val in entry.items()} for entry in monthly_data]

            return monthly_data

        else:
            return "LIMIT REACHED"
    except Exception as e:
        print(f"[{__name__}] - an error occurred: {e}")