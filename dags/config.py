import os

#load environment variables
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("APP_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")

DATABASE_URL ={f"postgresql://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}"}
ALPHA_MONTHLY_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=##SYMBOL##&apikey={ALPHA_VANTAGE_KEY}"