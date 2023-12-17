from config import FINNHUB_API_KEY
import finnhub
import pandas as pd
from datetime import date, timedelta

finnhub_api_key = FINNHUB_API_KEY

def get_ipo_data():
    Preparation
    today = date.today()
    start=today - timedelta(days=30)
    end=today + timedelta(days=30)

    finnhub_client = finnhub.Client(api_key=finnhub_api_key)

    ipo_data = finnhub_client.ipo_calendar(_from=start, to=end)

    df = pd.json_normalize(ipo_data, "ipoCalendar")

    return df
