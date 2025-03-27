'''
Author: Clayton Bennett
Date Created: 18 July 2023
Name: generate_UML.py

You can make source location a directory or a python file.
'''
from pylint import pyreverse
import os
from src.directories import Directories 

def generate_UML(source_location = Directories.get_core_dir()):
    os.system(f'pyreverse -o png {source_location} -d {source_location}')

if __name__ == "__main__":
    generate_UML(Directories.get_core_dir())
 