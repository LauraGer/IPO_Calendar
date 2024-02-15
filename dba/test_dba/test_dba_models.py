import pytest
from datetime import date
from dba.models_dag import MonthlyHistoryByStockSymbol
from dba.test_dba.utils_db import init_test_database
from dba.test_dba.utils_test_data import test_data_monthly_history

##############################################################
# SETUP - PREPARATION
##############################################################
@pytest.fixture
def test_data():
    return test_data_monthly_history

##############################################################
# TESTING
##############################################################
def test_create_monthly_history(test_data):
    session = next(init_test_database())

    monthly_history = MonthlyHistoryByStockSymbol(**test_data)
    session.add(monthly_history)
    session.commit()

    assert monthly_history.monthly_history_id is not None
    assert monthly_history.symbol == test_data["symbol"]
    assert monthly_history.date == test_data["date"]
    assert monthly_history.open == test_data["open"]
    assert monthly_history.high == test_data["high"]
    assert monthly_history.low == test_data["low"]
    assert monthly_history.close == test_data["close"]
    assert monthly_history.volume == test_data["volume"]

def test_retrieve_monthly_history(test_data):
    session = next(init_test_database())

    retrieved_history = (
        session.query(MonthlyHistoryByStockSymbol)
        .filter_by(symbol=test_data["symbol"], date=test_data["date"])
        .first()
    )

    assert retrieved_history is not None
    assert retrieved_history.symbol == test_data["symbol"]
    assert retrieved_history.date == test_data["date"]
    assert retrieved_history.open == test_data["open"]
    assert retrieved_history.high == test_data["high"]
    assert retrieved_history.low == test_data["low"]
    assert retrieved_history.close == test_data["close"]
    assert retrieved_history.volume == test_data["volume"]