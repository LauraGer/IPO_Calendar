from numbers import Number

class ColumnMapping:
    alpha_historical_data = {"1. open": "open",
                            "2. high": "high",
                            "3. low": "low",
                            "4. close": "close",
                            "5. volume": "volume"}

    poligon_historical_data = {"o": "open",
                               "h": "high",
                               "l": "low",
                               "c": "close",
                               "v": "volume"}

    expected_fields_as_of_history = {
        "symbol": str,
        "date": str,
        "open": Number,
        "high": Number,
        "low": Number,
        "close": Number,
        "volume": Number
    }