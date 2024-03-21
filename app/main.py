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
from app.fetcher_data import DataFetcher
from app.fetcher_source import stock_sources
from app.generator_calendar import add_entries_to_calendar
from app.generator_graph import build_graph
from app.generator_as_of_list import load_search_symbols_historical_data, process_list, process_query
from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

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

@app.get("/IPOsFilter", response_class=HTMLResponse)
async def get_dataset(request: Request, year: int, month: int):

    entries = DataFetcher.data_get_entries_from_db(year, month)

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

@app.get("/asof/", response_class=HTMLResponse)
async def read_form(request: Request):
    symbols_dropdown = DataFetcher.data_get_symbols_app()
    list_dropdown = DataFetcher.data_get_as_of_distinct_listnames()
    symbols_with_data = DataFetcher.data_get_symbols_min_date_key_app()
    return templates.TemplateResponse("asof_form.html", {"request": request,
                                                    "symbols_dropdown": symbols_dropdown,
                                                    "symbols_with_data": symbols_with_data,
                                                    "list_dropdown": list_dropdown,
                                                    "stock_sources": stock_sources})


# def send_progress(progress):
#     streamer = ProgressStreamer(progress)
#     return StreamingResponse(streamer.stream_progress(), media_type="text/event-stream")

@app.post("/asof/")
async def submit_form(request: Request,
    listnameSelect: str = Form(None),
    listnameNew: str = Form(None),
    symbols: str = Form(...),
    asOfDate: str = Form(...),
    volume: int = Form(...),
    price: float = Form(...)
):
    unprocessed = []
    processed = []
    table_data = []
    is_new = False
    list_name = listnameNew if listnameNew else listnameSelect

    for symbol in symbols:
        processed.insert(1, symbol)
    # for asOfDate, volume, price in zip(asOfDate, volume, price ):
    table_data.append({"as_of_date": asOfDate, "volume": volume, "price": price})

    if listnameNew:
        is_new = True

    as_of_list = {
        "listname":list_name,
        "as_of_date":asOfDate,
        "symbol":symbols,
        "volume":volume,
        "as_of_price":price,
        "is_new":is_new
    }

    list_name_return = process_list(as_of_list)
    return templates.TemplateResponse("asof_progress.html", {"request": request,
                                                    "processed": symbols,
                                                    "unprocessed": unprocessed,
                                                    "list_name_return": list_name_return})

@app.get("/asof/query", response_class=HTMLResponse)
async def run_query(value: str, searchType: str,):
    query_result = process_query(value, searchType)
        # print(value)
        # print(searchType)
    print(query_result)
    return HTMLResponse(content=str(query_result))

@app.get("/asof/value", response_class=HTMLResponse)
async def run_query(symbol:str, date:str):
    source_result = None
    print(symbol,date)
    return HTMLResponse(content=source_result)

# @app.get("/asof/listcreate", response_class=HTMLResponse)
# async def run_query(listName: str):
#     query_result = f"Query result for {listName}"
#     print(query_result)
#     return HTMLResponse(content=query_result)

@app.get("/asof/popup", response_class=HTMLResponse)
async def show_popup(request: Request, stockNew: str = Query(...), stockSource: str = Query(...)):
    print(stockSource)
    processed, unprocessed, cnt_bulk, cnt_update = load_search_symbols_historical_data(stockNew, stockSource)
    return templates.TemplateResponse("asof_form_popup.html", {"request": request,
                                                    "processed": processed,
                                                    "unprocessed": unprocessed,
                                                    "cnt_bulk": cnt_bulk,
                                                    "cnt_update": cnt_update })
