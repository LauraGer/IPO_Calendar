import finnhub
import json
import os
import pandas as pd
import requests
from config import FINNHUB_API_KEY, ALPHA_MONTHLY_URL, json
from datetime import datetime

finnhub_api_key = FINNHUB_API_KEY
finnhub_client = finnhub.Client(api_key=finnhub_api_key)

# def get_ipo_data(start, end, finnhub_client=finnhub_client):

#     ipo_data = finnhub_client.ipo_calendar(_from=start, to=end)

#     df = pd.json_normalize(ipo_data, "ipoCalendar")

#     return df
def get_str_date(date):
    date_obj = datetime(*date)
    date_str = date_obj.strftime('%Y-%m-%d')

    return date_str

def get_ipo_data(start, end, finnhub_client=finnhub_client):

    ipo_data = finnhub_client.ipo_calendar(_from=start, to=end)
    initial_df = pd.json_normalize(ipo_data, "ipoCalendar")

    min_date = initial_df.date.min()

    start_str = get_str_date(start)
    result_df = pd.DataFrame()
    result_df = initial_df
    # iterate till the whole timeframe is concatenated
    while start_str <= min_date:
        ipo_data = finnhub_client.ipo_calendar(_from=start, to=min_date)
        df_temp = pd.json_normalize(ipo_data, "ipoCalendar")

        result_df = pd.concat([result_df, df_temp], ignore_index=True)

        min_date = result_df.date.min()

    return result_df

def get_historical_values_by_symbol(symbol):

    url = ALPHA_MONTHLY_URL.replace("##SYMBOL##", symbol)
    # request_json = requests.get(url)
    # data = request_json.json()

    data = json

    print(data)
    monthly_data = [{"symbol": data["Meta Data"]["2. Symbol"], "date": key, **value, }
                    for key, value in data.get("Monthly Time Series", {}).items()]

    column_mapping = {"1. open": "open",
                      "2. high": "high",
                      "3. low": "low",
                      "4. close": "close",
                      "5. volume": "volume"}
    print("monthly data of get_hisrical....")
    print(monthly_data)

    monthly_data = [{column_mapping.get(col, col): val for col, val in entry.items()} for entry in monthly_data]

    return monthly_data

def get_stock_symbols(finnhub_client=finnhub_client):

    stock_symbols_data = finnhub_client.stock_symbols('US')

    df = pd.DataFrame(stock_symbols_data)

    return df