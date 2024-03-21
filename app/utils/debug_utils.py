import datetime

def debug_callback(debug_info):
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Prepend the message with the timestamp
    message_with_timestamp = f"[{timestamp}] {debug_info}"
    # Print the debug message
    print(message_with_timestamp)

    debug_info += debug_info

    return debug_info