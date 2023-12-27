import os


#load environment variables
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("APP_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

DATABASE_URL ={f"postgresql://{USER}:{PASSWORD}@{HOST}:5432/{DATABASE}"}