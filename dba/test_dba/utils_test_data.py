from dba.models_dag import Base, IPO_Calendar, MonthlyHistoryByStockSymbol
from datetime import datetime, date


test_data_monthly_history = {
        "symbol": "AAPL",
        "date": date(2022, 1, 1),
        "open": 150.0,
        "high": 155.0,
        "low": 148.0,
        "close": 152.0,
        "volume": 1000000,
    }

test_data_MonthlyHistory = [
        # DATA
        # MonthlyHistoryByStockSymbol
        MonthlyHistoryByStockSymbol(
            symbol = "Test1",
            date=datetime(2022,1,1),
            open = 1.0,
            high = 2.0,
            low = 0.5,
            close = 1.5,
            volume = 666,
            ),
        MonthlyHistoryByStockSymbol(
            symbol = "Test1",
            date=datetime(2022,2,1),
            open = 1.0,
            high = 2.0,
            low = 0.5,
            close = 1.5,
            volume = 666,
            ),
        MonthlyHistoryByStockSymbol(
            symbol = "Test1",
            date=datetime(2022,3,1),
            open = 1.0,
            high = 2.0,
            low = 0.5,
            close = 1.5,
            volume = 666,
            ),
        MonthlyHistoryByStockSymbol(
            symbol = "Test2",
            date=datetime(2022,3,1),
            open = 1.0,
            high = 2.0,
            low = 0.5,
            close = 1.5,
            volume = 666,
            )
    ]

test_data_IPO_Calendar = [
        # DATA
        # IPO_Calendar
        IPO_Calendar(
            date=datetime(2022,1,1),
            exchange="Test1",
            name="Test1 success name",
            numberOfShares=100,
            price="100",
            status="test status",
            symbol="xyz1",
            totalSharesValue=100
            ),
        IPO_Calendar(
            date=datetime(2022,1,2),
            exchange="Test2",
            name="Test2 success will all values",
            numberOfShares=100,
            price="100",
            status="test status",
            symbol="xyz2",
            totalSharesValue=100
            ),
        IPO_Calendar(
            date=datetime(2022,3,2),
            exchange="Test3",
            name="Test3 not included - not in time range",
            numberOfShares=100,
            price="100",
            status="test status",
            symbol="xyz3",
            totalSharesValue=100
            ),
        IPO_Calendar(
            date=datetime(2022,1,2),
            exchange="Test4",
            name="Test4 - empty symbol - in time range",
            numberOfShares=100,
            price="100",
            status="test status",
            symbol="",
            totalSharesValue=100
            ),
        IPO_Calendar(
            date=datetime(2022,1,2),
            exchange="Test5",
            name="Test5 - none symbol - in time range",
            numberOfShares=100,
            price="100",
            status="test status",
            symbol=None,
            totalSharesValue=100
            )
    ]