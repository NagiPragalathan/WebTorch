import json

def json_to_dict(jsondata):
    """
    Convert JSON data to a Python dictionary.

    Parameters:
    - jsondata (dict): A JSON data dictionary to be converted.

    Returns:
    - output_dict (dict): A Python dictionary containing the same data as the input JSON.

    This function takes a JSON data dictionary as input and returns the equivalent Python dictionary.
    It is useful for converting JSON data into a format that can be easily manipulated in Python.

    Example:
    json_data = {"key1": "value1", "key2": "value2"}
    python_dict = json_to_dect(json_data)
    """
    output_dict = {}
    for key in jsondata:
        output_dict[key] = jsondata[key]
    return output_dict
    
def get_more(dic_data):
    """
    Recursively extracts nested dictionaries from a given dictionary.

    Args:
        dic_data (dict): A Python dictionary.

    Returns:
        list: A list of dictionaries containing nested dictionary structures.

    Example:
        data = {'key1': {'key2': 'value2', 'key3': {'key4': 'value4'}}}
        nested_dicts = get_more(data)
    """
    stack = []
    for key in dic_data.keys():
        if isinstance(dic_data[key], dict):
            stack.extend(get_more(dic_data[key]))
        else:
            if dic_data not in stack:
                stack.append(dic_data)
    return stack

def get_stack(path):
    """
    Extract a stack of values from a JSON file.

    Parameters:
    - path (str): The path to the JSON file containing nested data.

    Returns:
    - stack (list): A list of values extracted from the nested JSON data.

    This function reads JSON data from a file, converts it to a dictionary, and then extracts
    all values from the nested dictionary using the get_more function. It returns a flat list
    of values in the order they were extracted.

    Example:
    stack_data = get_stack("data.json")
    """
    with open(path, 'r') as data_file:
        read_data = data_file.read()
        data_file.close()
    dict_data = json_to_dict(json.loads(read_data))
    print(get_more(dict_data))
    return get_more(dict_data)
