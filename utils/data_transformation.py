from datetime import datetime

def update_timestamps(json_data, key, strftimeformat):
    """
    Update timestamps in a JSON data structure.

    Parameters:
    - json_data (dict or list): The JSON data structure to be updated.
    - key (str): The key representing the timestamp. Default is 't'.
    """
    if isinstance(json_data, dict) and 'results' in json_data:
        results = json_data['results']
        for result in results:
            if key in result:
                timestamp_ms = result[key]
                timestamp_sec = timestamp_ms / 1000
                dt_object = datetime.fromtimestamp(timestamp_sec)
                formatted_date = dt_object.strftime(strftimeformat)
                result[key] = formatted_date
    elif isinstance(json_data, list):
        for item in json_data:
            update_timestamps(item, key)