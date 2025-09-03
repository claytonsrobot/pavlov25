'''
Title: filename_utils.py
Created: 29 March 2025
Author: Clayton Bennett
'''
import os
from pathlib import Path
def get_this_filename(filename):
    name = os.path.basename(filename).removesuffix('.py')
    return name
