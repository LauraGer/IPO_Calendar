import os
#helps while developing and loads the .env
from dotenv import load_dotenv

#load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("APP_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")


base_dir = os.path.dirname(os.path.abspath(__file__))

font_dir = os.path.join(base_dir, "static", "fonts")
default_font = "Urbanist-Bold.ttf"
font_path = os.path.join(font_dir,default_font)

static_path = os.path.join(base_dir, "static")
