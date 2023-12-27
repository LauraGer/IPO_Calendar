from get_sources import get_ipo_data
from dotenv import load_dotenv
import finnhub
import os

# Load variables from .env file
load_dotenv()

#load environment variables
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

df = get_ipo_data(finnhub_client)
print(df)