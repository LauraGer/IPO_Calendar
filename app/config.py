import os
from dotenv import load_dotenv

load_dotenv()

#load environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
POSTGRES_DB = os.getenv("POSTGRES_DB")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")