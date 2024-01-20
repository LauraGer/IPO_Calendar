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
from app.dba.db_helper import get_entries_from_db, get_symbol_details, get_entries
from app.generator_calendar import add_entries_to_calendar
from app.generator_graph import build_graph
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

class DataFetcher:
    def data_result(year,month):
        return get_entries(year,month)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    add_entries_to_calendar(2023, 12)
    #return templates.TemplateResponse("index.html", {"request": request})
    return templates.TemplateResponse(request, "index.html", {"request": request})


@app.get("/calendar", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "calendar.html", {"request": request})

    # return templates.TemplateResponse("calendar.html", {"request": request})

# Route to fetch data from PostgreSQL
@app.get("/calendar/data/{year}/{month}")
async def get_data(year: int, month: int):
    try:
        result = DataFetcher.data_result(year,month)
        data = []
        for row in result:
            if 'date' in row and 'symbol' in row:
                date_str = row['date']
                symbol = row['symbol']
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

    details = get_symbol_details(symbol)
    if details:
        symbol_details = f"Graph of {symbol} - {details[0]}"
    else:
        symbol_details = f"Graph of {symbol} - No details available!"

    return templates.TemplateResponse(request, "stock_graph.html", {"request": request,
                                                           "symbol_graph_title" : symbol_details,
                                                           "graph_html": graph_html})
