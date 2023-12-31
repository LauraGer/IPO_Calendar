# This is a little project to analyse IPO's
# 🚨 🚧 - all WIP - 🚧 🚨

## Current ToDo's
### 1. get IPO and historical data
- [x] load IPO calendar into postgres
  - [x] initial load which gets IPOs from the past till now
    - [x] the API can only handle 200 records - needs an iteration to go back till defined start date
  - [x] add scheduler to load every monday upcoming IPOs
- [x] load Stock Symbols into postgres
  - [ ] load worldwide stock details - currently only US is available
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


# to run this code locally simply follow these steps 🙂

## create free keys of finance APIs:
- finnhub key for IPOs and Stock Symbols -> [here](https://finnhub.io/)
- alpha vantage key for historical data per Symbol -> [here](https://www.alphavantage.co/support/#api-key)

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
- via http://localhost:8080/
- local user and password is defined in `airflow_setup.sh`

* `load_ipo_data_to_postgres`
* `load_monthly_history_stock_values`
* `load_ipo_data_to_postgres`

## install app dependencies with poetry
```bash
poetry install

poetry update (if needed and poetry already installed)
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


### references - links - sources
- [Airflow](https://airflow.apache.org/)
- [Alpha Vantage](https://www.alphavantage.co/)
- [Docker](https://www.docker.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Fonts](https://fonts.google.com/specimen/Urbanist)
- [Postgres](https://www.postgresql.org/)
