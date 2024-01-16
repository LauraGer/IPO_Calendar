import os

#load environment variables
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("APP_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
FMP_KEY = "nvuxIGgzjwuWGHsNt90VGFsWj46fVIZb"

DATABASE_URL ={f"postgresql://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}"}
ALPHA_MONTHLY_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=##SYMBOL##&apikey={ALPHA_VANTAGE_KEY}"



base_dir = os.path.dirname(os.path.abspath(__file__))

local_data_dir = os.path.join(base_dir, "local_data")