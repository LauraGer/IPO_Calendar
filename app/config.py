# Copyright 2023 Laura Gerlach

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
"""
helps while developing and loads the .env
"""
from dotenv import load_dotenv

"""
load environment variables
"""
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HOST = os.getenv("HOST")
APP_DB = os.getenv("APP_DB")
USER = os.getenv("POSTGRES_USER")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
IPO_CALENDAR_DB = os.getenv("IPO_CALENDAR_DB")


base_dir = os.path.dirname(os.path.abspath(__file__))

font_dir = os.path.join(base_dir, "static", "fonts")
default_font = "Urbanist-Bold.ttf"
font_path = os.path.join(font_dir,default_font)

static_path = os.path.join(base_dir, "static")

db_params_ipo_calendar = {
    "host": HOST,
    "database": IPO_CALENDAR_DB,
    "user": USER,
    "password": PASSWORD,
}

db_params_app = {
    "host": HOST,
    "database": APP_DB,
    "user": USER,
    "password": PASSWORD,
}