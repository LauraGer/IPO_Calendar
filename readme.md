# This is a little project to analyse IPO's
# 🚨 🚧 - all WIP - 🚧 🚨

## Current ToDo's
### 1. get IPO and historical data
- [x] load IPO calendar into postgres
  - [x] initial load which gets IPOs from the past till now
    - [x] the API can only handle 200 records - needs an iteration to go back till defined start date
  - [x] add scheduler to load every monday upcoming IPOs
  - [ ] decouple logic of building query and the execution
- [ ] adding unit tests
- [x] load Stock Symbols into postgres
  - [x] currently only US is available from finnhub
  - [ ] load worldwide stock details via FMP API
- [x] get historical data per Symbol
  - [x] add scheduler to load every day at 8am historical data for IPOs (only in 25 batches per day, free limit of Aplha Vantage)

### 2. Setup analysis
- [ ] Analyse historical IPOs and theirs success
  - [ ] Define questions to get answeres:
    - What was the best performing IPO from 2022 in 2023?

### 3. Interactive calendar
- [x] Create Calendar page with entries
- [ ] interaktive - I would like to have the calender with entries and on hover over entries some details

### 4. Create API for interactive graph
  - [ ] Create graph

### 5. Implement Discord Bot
- [ ] request upcoming IPOs
- [ ] get stock details by stock symbols

### EXTENSIONS?
 - [ ] adding an calendar overview of dividends

# to run this code locally simply follow these steps 🙂

## create free keys of finance APIs:
[This article on medium.com]( https://medium.com/coinmonks/best-stock-market-apis-ae1efb739ac4) gave me good overview about finance APIs.
I'm using the below ones to gather bits and pieces together.
- finnhub key for IPOs and Stock Symbols (only US is available for free) -> [here](https://finnhub.io/)
- alpha vantage key for historical data per Symbol -> [here](https://www.alphavantage.co/support/#api-key)
- FMP (financial modeling prep) API for wordlwird stock details -> [here](http://site.financialmodelingprep.com/developer/docs/stock-market-quote-free-api/?direct=true)

## get exchange csv and save local in `./dags/local_data/`
- download as csv from finnhub -> [here](https://docs.google.com/spreadsheets/d/1I3pBxjfXB056-g_JYf_6o3Rns3BV2kMGG1nCatb91ls)

## create in root directory a `.env` file and replace `###`
```.env
FLASK_APP=airflow.www.app:cached_app()
DATABASE_URL==###
AIRFLOW__CORE__SQL_ALCHEMY_CONN==###
FINNHUB_API_KEY==###
HOST==###
AIRFLOW_DB==###
APP_DB==###
POSTGRES_USER==###
POSTGRES_PASSWORD=###
AIRFLOW__WEBSERVER__RBAC=False
ADMIN_USER==###
ADMIN_PASSWORD==###
ALPHA_VANTAGE_KEY==###
```

## run docker-compose to initialize postgres and start airflow
```bash
docker-compose up -d
```

## run dags in airflow
via http://localhost:8080/.
local user and password is defined in `airflow_setup.sh`.

alternative via shell `airflow dags trigger -r <dag_id>`.

dag_id's:
* `load_ipo_data_to_postgres`
* `load_monthly_history_stock_values`
* `load_ipo_data_to_postgres`

## install app dependencies with poetry
```bash
poetry install

poetry update (if needed and poetry already installed)
```

## test app
```bash
pytest ./app/test_app -vvv
```

## start app
```bash
poetry shell #to start virtual env
uvicorn app.main:app --reload

#URL shows calendar with entires - not interactive yet
http://localhost:8000/

#URL lists IPOs
http://localhost:8000/IPOs

#URL lists IPOs of specific month
http://localhost:8000/IPOsFilter?year=2023&month=11

#URL interactive graph
http://localhost:8000/StockGraphSymbolFilter?symbol=xyz
```

# P.S. Feedback is always welcome!
![via GIPHY](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTllbnRpZnViZWhub2VoZnM1eTZ5dHA2M2VldHJ3aDJsdHJxdWp1MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ule4vhcY1xEKQ/giphy.gif)

### references - links - sources
- [Airflow](https://airflow.apache.org/)
- [Alpha Vantage](https://www.alphavantage.co/)
- [Docker](https://www.docker.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Fonts](https://fonts.google.com/specimen/Urbanist)
- [Postgres](https://www.postgresql.org/)

another font (https://unblast.com/download/48373/)

Diagram (https://excalidraw.com/#json=Im-3hUokNjZaANgzMbo2Q,OrkPI-u5UUv34eRUVeexjA)