import finnhub
import pandas as pd
from config import FINNHUB_API_KEY
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

    start_str = get_str_date(start)  # Format as YYYY-MM-DD to be able to set condition
    result_df = pd.DataFrame()
    result_df = initial_df
    while start_str <= min_date:
        ipo_data = finnhub_client.ipo_calendar(_from=start, to=min_date)
        df_temp = pd.json_normalize(ipo_data, "ipoCalendar")

        result_df = pd.concat([result_df, df_temp], ignore_index=True)

        min_date = result_df.date.min()

    return result_df

def get_stock_symbols(finnhub_client=finnhub_client):

    stock_symbols_data = finnhub_client.stock_symbols('US')

    df = pd.DataFrame(stock_symbols_data)
    print(df.head)

    return df