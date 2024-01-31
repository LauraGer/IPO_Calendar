import os
from dotenv import load_dotenv

"""
load environment variables
"""
load_dotenv()

HOST = os.getenv("HOST")
DATABASE = os.getenv("APP_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")

os.environ['TEST_DB_URL'] =f"postgresql://{USER}:{PASSWORD}@{HOST}:5432/test_db"


TEST_DB_URL = os.getenv("TEST_DB_URL")
print(f"TEST_DB_URL: '{TEST_DB_URL}'")
os.environ['SQLALCHEMY_SILENCE_UBER_WARNING'] = '1'