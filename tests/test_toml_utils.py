'''
Title: test_toml_utils.py
Author: Clayton Bennett assisted by Microsoft Co-Pilot
Created: 27 February 2025
Purpose: Unit test of the functions in the core.toml_utils.py file.
'''
import sys 
import unittest
from unittest.mock import patch, mock_open

# import all functions from the relative path
from ..core.toml_utils import check_file, check_for_null, load_toml, load_toml_tuple

class TestTomlFunctions(unittest.TestCase):
    
    def test_check_file_exists(self):
        with patch("os.path.isfile", return_value=True):
            self.assertTrue(check_file("dummy_path"))
    
    def test_check_file_not_exists(self):
        with patch("os.path.isfile", return_value=False):
            with self.assertRaises(SystemExit):
                check_file("dummy_path")
    
    def test_check_for_null(self):
        data = {
            "section1": {"key1": "value1", "key2": "null"},
            "section2": {"key3": "Null", "key4": "123"}
        }
        expected = {
            "section1": {"key1": "value1", "key2": None},
            "section2": {"key3": None, "key4": "123"}
        }
        result = check_for_null(data)
        self.assertEqual(result, expected)
    
    @patch("builtins.open", new_callable=mock_open, read_data='{"section": {"key": "value"}}')
    def test_load_toml(self, mock_file):
        with patch("os.path.isfile", return_value=True):
            if sys.version_info >= (3, 11):
                with patch("tomllib.load", return_value={"section": {"key": "value"}}):
                    result = load_toml("dummy_path")
            else:
                with patch("toml.load", return_value={"section": {"key": "value"}}):
                    result = load_toml("dummy_path")
            
            self.assertEqual(result, {"section": {"key": "value"}})

    def test_load_toml_tuple(self):
        data = {"section": {"key1": "value1"}}
        with patch("os.path.isfile", return_value=True):
            with patch("toml.load", return_value=data):
                result = load_toml_tuple("dummy_path")
                self.assertEqual(result, (("section", {"key1": "value1"}),))

if __name__ == "__main__":
    unittest.main()
