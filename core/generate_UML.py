'''
Author: Clayton Bennett
Date Created: 18 July 2023
Name: generate_UML.py

You can make source location a directory or a python file.
'''
from pylint import pyreverse
import os
import inspect

directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
def generate_UML(source_location = directory):
    os.system(f'pyreverse -o png {source_location} -d {source_location}')

if __name__ == "__main__":
    generate_UML(directory)
 