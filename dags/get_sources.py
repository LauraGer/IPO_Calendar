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
import pandas as pd
import requests
from config import FINNHUB_API_KEY, ALPHA_MONTHLY_URL
from datetime import datetime

finnhub_api_key = FINNHUB_API_KEY
finnhub_client = finnhub.Client(api_key=finnhub_api_key)


def get_str_date(date):
    print(f"date in get_str_date'{date}'")
    date_obj = datetime.combine(date)
    print(f"1. date_obj'{date_obj}'")
    date_str = date_obj.strftime('%Y-%m-%d')

    return date_str

def get_quarter_range(processing_month):
    month_day = 1
    current_quarter = (processing_month.month - 1) // 3 + 1
    next_quarter_start_month = current_quarter * 3 + 1 if current_quarter < 4 else 1
    current_year = processing_month.year
    next_year = current_year if next_quarter_start_month != 1 else current_year + 1
    month = processing_month.month
    processing_start = datetime(current_year, month, int(month_day))
    processing_end = datetime(next_year, next_quarter_start_month, int(month_day))

    return processing_start, processing_end

def get_ipo_data(start, end, finnhub_client=finnhub_client):
    ipo_data = finnhub_client.ipo_calendar(_from=start, to=end)
    initial_df = pd.json_normalize(ipo_data, "ipoCalendar")

    return initial_df

def get_historical_values_by_symbol(symbol):
    url = ALPHA_MONTHLY_URL.replace("##SYMBOL##", symbol)
    request_json = requests.get(url)
    data = request_json.json()
    if "'Note':" or "'Information':" in data:
        return "LIMIT REACHED"
    # if data
    # data: '*** Found local files:{'Information': 'Thank you for using Alpha Vantage! Our standard API r
    monthly_data = [{"symbol": data["Meta Data"]["2. Symbol"], "date": key, **value, }
                    for key, value in data.get("Monthly Time Series", {}).items()]
    column_mapping = {"1. open": "open",
                      "2. high": "high",
                      "3. low": "low",
                      "4. close": "close",
                      "5. volume": "volume"}
    monthly_data = [{column_mapping.get(col, col): val for col, val in entry.items()} for entry in monthly_data]

    return monthly_data

def get_stock_symbols(finnhub_client=finnhub_client):
    stock_symbols_data = finnhub_client.stock_symbols("US")
    df = pd.DataFrame(stock_symbols_data)

    return df