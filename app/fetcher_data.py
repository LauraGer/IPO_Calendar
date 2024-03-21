from app.config import HOST, USER, PASSWORD, APP_DB, db_params_ipo_calendar, db_params_app
from dba.models_app import Base, WatchlistUser, AsOfList, AsOfStockHistory
import dba.db_helper as dbh
from dba.crud import Read
# from dba.db_helper import get_session, get_entries_from_db, get_date_symbol_by_year_month, get_engine_by_db_params, get_as_of_distinct_listnames, get_symbols_of_history, get_symbols_min_date_key
from sqlalchemy.exc import IntegrityError

try:
    engine = dbh.get_engine_by_db_params(db_params_app)
    Base.metadata.create_all(bind=engine, checkfirst=True, tables=[AsOfList.__table__])
    Base.metadata.create_all(bind=engine, checkfirst=True, tables=[AsOfStockHistory.__table__])
    Base.metadata.create_all(bind=engine, checkfirst=True, tables=[WatchlistUser.__table__])
except IntegrityError as e:
    print(f"An error occurred: {e}")

class DataFetcher:
    @staticmethod
    def data_result_get_date_symbol_by_year_month(year, month):
        return dbh.get_date_symbol_by_year_month(year, month)

    @staticmethod
    def data_get_entries_from_db(year, month):
        return dbh.get_entries_from_db(year, month)

    @staticmethod
    def data_get_symbols_of_history():
        return dbh.get_symbols_of_history()

    @staticmethod
    def data_get_as_of_distinct_listnames():
        return Read.get_as_of_distinct_listnames(db_params_app)

    @staticmethod
    def data_get_symbols_min_date_key():
        return dbh.get_symbols_min_date_key()

    @staticmethod
    def data_get_symbols_min_date_key_app():
        return Read.get_symbols_min_date_key(db_params_app)

    @staticmethod
    def data_get_symbols_app():
        return Read.get_symbols_of_app(db_params_app)

    @staticmethod
    def data_get_list_details(list_name):
        return Read.get_list_details(db_params_app, list_name)