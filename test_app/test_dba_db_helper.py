import datetime
import pytest
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from app.dba.db_helper import get_symbols, get_entries_from_db
from app.config import HOST, USER, PASSWORD
from app.dba.models import Base, IPO_Calendar

@pytest.fixture
def db_session():
    # Setup a temporary PostgreSQL database for testing
    test_db_url = f"postgresql://{USER}:{PASSWORD}@{HOST}:5432/test_db"
    if not database_exists(test_db_url):
        create_database(test_db_url)
    engine = create_engine(test_db_url)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # cleanup
    with engine.connect() as conn:
        delete_query = delete(IPO_Calendar)
        conn.execute(delete_query)

    # Insert mock data into the database
    items = [
        IPO_Calendar(date=datetime.datetime(2022,1,1),
                     exchange="Test1",
                     name="Test1 success name",
                     numberOfShares=100,
                     price="100",
                     status="test status",
                     symbol="xyz1",
                     totalSharesValue=100),
        IPO_Calendar(date=datetime.datetime(2022,1,2),
                     exchange="Test2",
                     name="Test2 success will all values",
                     numberOfShares=100,
                     price="100",
                     status="test status",
                     symbol="xyz2",
                     totalSharesValue=100),
        IPO_Calendar(date=datetime.datetime(2022,3,2),
                     exchange="Test3",
                     name="Test3 not included - not in time range",
                     numberOfShares=100,
                     price="100",
                     status="test status",
                     symbol="xyz3",
                     totalSharesValue=100),
        IPO_Calendar(date=datetime.datetime(2022,1,2),
                     exchange="Test4",
                     name="Test4 - empty symbol - in time range",
                     numberOfShares=100,
                     price="100",
                     status="test status",
                     symbol="",
                     totalSharesValue=100),
        IPO_Calendar(date=datetime.datetime(2022,1,2),
                     exchange="Test5",
                     name="Test5 - none symbol - in time range",
                     numberOfShares=100,
                     price="100",
                     status="test status",
                     symbol=None,
                     totalSharesValue=100),
        # Add more mock data as needed
    ]
    db.add_all(items)
    db.commit()

    yield db

    # Teardown: Rollback the session and close the connection
    db.rollback()
    db.close()

def test_get_symbols(db_session):
    # Call your function with the mock data
    result = get_symbols(2022,1, db_session)
    # Perform assertions
    expected_result = ["xyz1", "xyz2"]

    assert len(result) == 2
    assert result == expected_result

def test_get_entries_from_db(db_session):
    # Call your function with the mock data
    result = get_entries_from_db(2022,1, db_session)
    # Perform assertions
    expected_result = [(datetime.date(2022, 1, 1), "Test1 success name", "xyz1")
                     , (datetime.date(2022, 1, 2), "Test2 success will all values", "xyz2")
                     , (datetime.date(2022, 1, 2), "Test4 - empty symbol - in time range", "")
                     , (datetime.date(2022, 1, 2), "Test5 - none symbol - in time range", None)
                    ]

    assert len(result) == 4
    assert result == expected_result