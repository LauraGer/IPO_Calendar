import os

#load environment variables
HOST = os.getenv("HOST")
DATABASE = os.getenv("IPO_CALENDAR_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
FMP_KEY = os.getenv("ALPHA_VANTAGE_KEY")

ALPHA_MONTHLY_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=##SYMBOL##&apikey={ALPHA_VANTAGE_KEY}"

relevant_exchange = ["US", "F", "DE", "NS", "TW"]

base_dir = os.path.dirname(os.path.abspath(__file__))

local_data_dir = os.path.join(base_dir, "local_data")