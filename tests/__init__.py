# tests/__init__.py
from .test_core import Test
import os
import sys

# Add the 'src' directory to the Python module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
