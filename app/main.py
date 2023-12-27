from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from generator import add_entries_to_calendar, get_entries_from_db

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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

    entries = get_entries_from_db(year, month)  # Adjust this according to your actual database query logic

    title = "IPO's"
    table_name = f"requested IPO's for Year: {year} and Month: {month}"

    return templates.TemplateResponse("tables.html",
                                      {"request": request,
                                       "title": title,
                                       "table_name": table_name,
                                       "entries": entries})