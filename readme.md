# This is a little project to analyse IPO's
# 🚨 🚧 - all WIP - 🚧 🚨

## Current ToDo's
### Read Finnhub Data
- [x] load IPO calendar into postgres
  - [ ] ...
- [ ] load Stock Symbols into postgres
### Setup Analysis
- [ ] Completed task title
### Implement Discord Bot
- [ ] request upcoming IPOs
- [ ] get stock details by stock symbols 

# to run this code locally simply follow these steps 🙂
## create in root directory a `.env` file 
you need a finnhub key - you can get one for free [here](https://finnhub.io/)
```.env
FLASK_APP=airflow.www.app:cached_app()
DATABASE_URL=#####[DATABASE_URL]###### 
AIRFLOW__CORE__SQL_ALCHEMY_CONN=#####[AIRFLOW__CORE__SQL_ALCHEMY_CONN URL]###### 
FINNHUB_API_KEY=#####[YOUR FINNHUB KEY]###### 
HOST=#####[YOUR HOST]###### 
AIRFLOW_DB=#####[YOUR AIRFLOW DB]###### 
APP_DB=#####[YOUR APP DB]###### 
POSTGRES_USER=sa
POSTGRES_PASSWORD=123
AIRFLOW__WEBSERVER__RBAC=False
ADMIN_USER=admin
ADMIN_PASSWORD=123
```

## run docker-compose and create admin user
```bash
docker-compose up -d
```
