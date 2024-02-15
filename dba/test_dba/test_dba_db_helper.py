import datetime
import os
import pytest
from dba.db_helper import build_date_range_year_month, get_symbols, get_entries_from_db
from dba.models_dag import IPO_Calendar, MonthlyHistoryByStockSymbol
from dba.test_dba.utils_db import cleanup_test_table, init_test_database, engine
from dba.test_dba.utils_test_data import test_data_IPO_Calendar, test_data_MonthlyHistory

TEST_DB_URL = os.getenv("TEST_DB_URL")

##############################################################
# SETUP - PREPARATION
##############################################################
@pytest.fixture
def test_IPO_Calendar_data():
    return test_data_IPO_Calendar

@pytest.fixture
def test_MonthlyHistory_data():
    return test_data_MonthlyHistory

@pytest.fixture
def db_session_IPO_Data(test_IPO_Calendar_data):
    db = next(init_test_database())
    # cleanup
    cleanup_test_table(engine, IPO_Calendar)

    # Insert mock data into the database
    db.add_all(test_IPO_Calendar_data)
    db.commit()

    yield db

    # Teardown: Rollback the session and close the connection
    db.rollback()
    db.close()

@pytest.fixture
def db_session_MonthlyHistory_Data(test_MonthlyHistory_data):
    db = next(init_test_database())
    # cleanup
    cleanup_test_table(engine, MonthlyHistoryByStockSymbol)

    # Insert mock data into the database
    db.add_all(test_MonthlyHistory_data)
    db.commit()

    yield db

    # Teardown: Rollback the session and close the connection
    db.rollback()
    db.close()

##############################################################
# TESTING
##############################################################
def test_build_date_range_year_month():
    result_start, result_end = build_date_range_year_month(2022, 1)

    expected_start = datetime.date(2022,1,1)
    expected_end = datetime.date(2022,1,31)

    print(result_start, result_end)

    assert expected_start == result_start
    assert expected_end == result_end

def test_get_symbols(db_session_IPO_Data):
    result = get_symbols(2022,1, db_session_IPO_Data)

    expected_result = ["xyz1", "xyz2"]

    assert len(result) == 2
    assert result == expected_result

def test_get_entries_from_db(db_session_MonthlyHistory_Data):
    result = get_entries_from_db(2022,1, db_session_MonthlyHistory_Data)

    expected_result = [(datetime.date(2022, 1, 1), "Test1 success name", "xyz1")
                     , (datetime.date(2022, 1, 2), "Test2 success will all values", "xyz2")
                     , (datetime.date(2022, 1, 2), "Test4 - empty symbol - in time range", "")
                     , (datetime.date(2022, 1, 2), "Test5 - none symbol - in time range", None)
                    ]

    assert len(result) == 4
    assert result == expected_result