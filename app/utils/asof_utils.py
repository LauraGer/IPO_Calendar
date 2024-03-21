from app.config import HOST, USER, PASSWORD, APP_DB, db_params_ipo_calendar, db_params_app
from dba.crud import BulkInsert, Create
from dba.db_helper import get_session
from dba.models_app import Base, AsOfList, AsOfStockHistory
from utils.get_sources import AlphaVantage, Finnhub, PoligonIo
from utils.schema import ColumnMapping
from typing import Callable
import datetime
from app.utils.debug_utils import debug_callback
import json
from pydantic import BaseModel
import asyncio
from fastapi.responses import StreamingResponse

class Progress(BaseModel):
    status: str
    percent_complete: int


class ProgressStreamer:
    def __init__(self, progress):
        self.progress = progress

    async def stream_progress(self):
        async def generate():
            for i in range(11):
                await asyncio.sleep(1)  # Simulate work
                self.progress.status = f"Processing step {i}"
                self.progress.percent_complete = i * 10
                print(f"data: {self.progress.json()}")
                yield f"data: {self.progress.json()}\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")


def validate_data_for_model(data, fields):
    # Iterate through each dictionary in the provided data
    for item in data:
        print(f"item: {item}")
        # Check if all expected fields are present in the dictionary
        if not all(field in item for field in fields.keys()):
            return False

        # # Check if the types of the fields match the types defined in your model
        for field, field_type in fields.items():
            if not isinstance(item[field], field_type):
                return False

    return True
