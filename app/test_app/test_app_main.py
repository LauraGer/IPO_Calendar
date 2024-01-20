import os
import pytest
from app.main import app
from httpx import AsyncClient

@pytest.fixture
def mock_data_result(mocker):
    # Mock the data_result function to return predefined data
    mocked_data = [
        {"date": "2023-01-01", "symbol": "ABC"},
        {"date": "2023-01-02", "symbol": "DEF"},
        # Add more mocked data as needed
    ]
    mocker.patch("app.main.DataFetcher.data_result", return_value=mocked_data)
    return mocked_data

@pytest.fixture
def mock_get_entries_from_db(mocker):
    # Mock the data_result function to return predefined data
    mocked_data = [
        {"date": "2023-01-01", "name": "Test Name 1", "symbol": "ABC"},
        {"date": "2023-01-02", "name": "Test Name 2", "symbol": "DEF"},
        # Add more mocked data as needed
    ]
    mocker.patch("app.main.get_entries_from_db", return_value=mocked_data)
    return mocked_data

@pytest.fixture
def expected_html_get_dataset_filter_route():
    expected_result_path = os.path.join(os.path.dirname(__file__), "response", "expected_get_dataset_filter_route.html")
    with open(expected_result_path, "r", encoding="utf-8") as file:
        return file.read()
# @pytest.mark.asyncio
# async def test_index_route():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/")
#         print(response)
#         assert response.status_code == 200
#         assert "Calendar with Hover Details" in response.text

@pytest.mark.asyncio
async def test_calendar_route():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/calendar")

        assert response.status_code == 200
        assert "Interactive Calendar" in response.text

@pytest.mark.asyncio
async def test_get_data_route(mock_data_result):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/calendar/data/2023/1")
        data = response.json()
        print(response.status_code)
        print(response.text)

        assert response.status_code == 200
        assert isinstance(data, list)
        assert data == mock_data_result

# @pytest.mark.asyncio
# async def test_get_dataset_filter_route(mock_get_entries_from_db, expected_html_get_dataset_filter_route):
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/IPOsFilter?year=1999&month=1")
#         assert response.status_code == 200
#         print(expected_html_get_dataset_filter_route)
#         # assert "IPO&#39;s for Ye---ar:" in response.text
#         assert expected_html_get_dataset_filter_route == response.text

# @pytest.mark.asyncio
# async def test_get_stock_graph_symbol_filter_route():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         response = await client.get("/StockGraphSymbolFilter?symbol=ABCDEF")
#         assert response.status_code == 200
#         assert "Graph of " in response.text  # Adjust based on your actual content
