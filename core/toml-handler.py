"""
Title: toml-handler.py
Author: Clayton Bennett
Created: 22 February 2025
"""
import sys
# Use tomllib if the Python version is 3.11+. Otherwise use the toml package.
if sys.version_info >= (3,11):
    import tomllib as tomll
else:
    import toml as tomll

def load_toml(filepath):
    with open(filepath,"rb") as f:
        data = tomll.load(f)
    data_tuple = tuple(data.items())
    return data_tuple

if "__main__" == __name__:
   pass 
