"""
Copyright 2023 Laura Gerlach

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import asyncpg
from app.config import HOST, USER, PASSWORD, APP_DB, db_params_ipo_calendar, db_params_app
from dba.db_helper import get_entries_from_db, get_entries, get_engine_by_db_params, get_session
from dba import models_app, crud, schemas_app
from app.generator_calendar import add_entries_to_calendar
from app.generator_graph import build_graph
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

engine = get_engine_by_db_params(db_params_ipo_calendar)
try:
    models_app.Base.metadata.create_all(bind=engine, checkfirst=True, tables=[models_app.WatchlistUser.__table__])
except IntegrityError as e:
    print(f"An error occurred: {e}")

# Connect to the APP_DB database
async def connect_to_db():
    return await asyncpg.connect(f"postgresql://{USER}:{PASSWORD}@{HOST}/{APP_DB}")

# Disconnect from the APP_DB database
async def close_db_connection(connection):
    await connection.close()

def get_db():
    session = get_session()
    try:
        yield session
    finally:
        session.close()

class DataFetcher:
    def data_result(year,month):
        result = get_entries(year,month)
        print(result)
        return get_entries(year,month)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    add_entries_to_calendar(2023, 12)
    return templates.TemplateResponse(request, "index.html", {"request": request})


@app.get("/calendar", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "calendar.html", {"request": request})

# Route to fetch data from PostgreSQL
@app.get("/calendar/data/{year}/{month}")
async def get_data(year: int, month: int):
    try:
        result = DataFetcher.data_result(year,month)
        data = []
        for row in result:
            if len(row) == 2:
                date_str = row[0]
                symbol = row[1]
                row_dict = {
                    "date": date_str,
                    "symbol": symbol,
                }
                data.append(row_dict)
            else:
                print(f"Warning: 'date' or 'symbol' not found in row: {row}")

    except Exception as e:
        return JSONResponse(content={"error": f"An error occurred: {e}"}, status_code=500)

    return data

@app.get("/IPOs",response_class=HTMLResponse)
async def get_dataset(request: Request):
    entries = get_entries_from_db(2023,12)
    title = "IPO's"
    table_name = "requested IPO's"

    return templates.TemplateResponse(request, "tables.html",
                                      {"request": request,
                                       "title": title,
                                       "table_name": table_name,
                                       "entries": entries})

@app.get("/IPOsFilter", response_class=HTMLResponse)
async def get_dataset(request: Request, year: int, month: int):

    entries = get_entries_from_db(year, month)

    count =  f"total of {len(entries)}"

    title = "IPO's"
    table_name = f"requested IPO's for Year: {year} and Month: {month}"
    columns = ["Date", "Desciption", "Symbol"]

    return templates.TemplateResponse(request, "tables.html", {"request": request,
                                                      "title": title,
                                                      "count": count,
                                                      "table_name": table_name,
                                                      "entries": entries,
                                                      "columns": columns})

@app.get("/StockGraphSymbolFilter", response_class=HTMLResponse)
async def get_dataset(request: Request, symbol: str):
    #entries = get_history_by_symbol(symbol)
    graph_html = build_graph(symbol)

    symbol_details = f"Historical data graph for {symbol}"

    return templates.TemplateResponse(request, "stock_graph.html", {"request": request,
                                                           "symbol_graph_title" : symbol_details,
                                                           "graph_html": graph_html})

@app.get("/watchlist/", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/watchlist/login/", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    return templates.TemplateResponse("loggedin.html", {"request": request, "username": username})

@app.get("/watchlist/register/", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/watchlist/register")
def create_user(user: schemas_app.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)