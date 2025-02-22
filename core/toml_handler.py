"""
Title: toml-handler.py
Author: Clayton Bennett
Created: 22 February 2025
"""
from pathlib import Path
import os
import sys
# Use tomllib if the Python version is 3.11+. Otherwise use the toml package.
if sys.version_info >= (3,11):
    import tomllib
else:
    import toml

def load_toml(filepath):
    with open(filepath,"r", encoding="utf-8") as f:
        if sys.version_info >= (3,11):
            data = tomllib.load(f)
        else:
            data = toml.load(f)
        data = check_for_null(data)
    return data

def load_toml_tuple(filepath):
    data = load_toml(filepath)
    data_tuple = tuple(data.items())
    return data_tuple

def check_for_null(data):
    # Iterate through the dictionary
    for section_key, section in data.items():
        for key, value in section.items():
        # If the value is a string and equals "null", replace it with None
            if isinstance(value, str) and value.lower() == "null":
                section[key] = None
                data[section_key]=section
    return data


if "__main__" == __name__:
   filepath = r"C:\Users\user\Documents\pavlov\pavlov25\core\projects\Don-EvonikPAA-MemphisCellulose\configs\config_input_22February_PAA.toml"
   filepath = Path(os.path.normpath(filepath))
   t = load_toml(filepath)
   print(t)
