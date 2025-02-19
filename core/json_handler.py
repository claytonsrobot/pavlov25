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

if "__main__" == __name__:
   pass 
