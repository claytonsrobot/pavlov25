"""
Title: json-handler.py
Author: Clayton Bennett
Created: 30 January 2025
"""

import json

def create_tuple_from_json(json_filepath):
    with open(json_filepath) as f:
        data = json.load(f)
    data_tuple = tuple(data.items())
    return data_tuple

def export_to_json(data, filepath, indent=4):
    """
    Generic helper function to export any data structure to a JSON file.

    Args:
        data (dict/list): The data structure to export.
        filepath (str): Path to the output JSON file.
        indent (int): Number of spaces for indentation in the JSON file.
    
    Returns:
        bool: True if export was successful, False otherwise.
    """
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=indent)
        return True
    except Exception as e:
        print(f"Error exporting to JSON: {e}")
        return False
    
if "__main__" == __name__:
   pass 

