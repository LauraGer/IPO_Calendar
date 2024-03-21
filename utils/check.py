def check_result(result, expected_fields):
    # if not isinstance(result, dict):
    #     print("[ERROR] 'result' should be a dictionary.")
    #     return False

    for field, field_type in expected_fields.items():
        # if field not in result:
        #     print(f"Missing field: {field}")
        #     return False
        if not isinstance(result[field], field_type):
            print(f"Field '{field}' has incorrect type. Expected type: {field_type}, Actual type: {type(result[field])}")
            return False

    return True