from app.dba.db_helper import get_entries_from_db, get_history_by_symbol, get_symbol_details
from app.generator_calendar import add_entries_to_calendar
from app.generator_graph import build_graph
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    add_entries_to_calendar(2023, 12)
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/IPOs",response_class=HTMLResponse)
async def get_dataset(request: Request):
    entries = get_entries_from_db(2023,12)
    title = "IPO's"
    table_name = "requested IPO's"

    return templates.TemplateResponse("tables.html",
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

    return templates.TemplateResponse("tables.html", {"request": request,
                                                      "title": title,
                                                      "count": count,
                                                      "table_name": table_name,
                                                      "entries": entries,
                                                      "columns": columns})

@app.get("/StockGraphSymbolFilter", response_class=HTMLResponse)
async def get_dataset(request: Request, symbol: str):
    symbol = "GBS"
    entries = get_history_by_symbol(symbol)
    graph_html = build_graph(symbol)

    details = get_symbol_details(symbol)
    symbol_details = f"Graph of {symbol} - {details[0]}"

    return templates.TemplateResponse("stock_graph.html", {"request": request,
                                                           "symbol_graph_title" : symbol_details,
                                                           "graph_html": graph_html})
