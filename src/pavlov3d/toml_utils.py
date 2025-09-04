# src/pavlov3d/toml_utils.py
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
"""
Path-aware TOML utilities.

- Uses pathlib.Path internally.
- Keeps compatibility with tests that patch os.path.isfile() or toml.load().
- Python 3.9+ friendly typing.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple
import os
import toml


def check_file(filepath: Path | str) -> bool:
    """
    Return True if filepath exists and is a file.

    This function prefers pathlib.Path.is_file() but consults os.path.isfile()
    first so unit tests that mock os.path.isfile(...) continue to work.
    Accepts either a Path or a string.
    """
    p = Path(filepath)
    # allow tests/legacy callers to mock os.path.isfile; if it returns True, accept it
    try:
        if os.path.isfile(str(filepath)):
            return True
    except Exception:
        # fall back to Path check if os.path raises for whatever reason
        pass
    return p.is_file()


def load_toml(filepath: Path | str) -> Dict[str, Any]:
    """
    Load a TOML file and return a dict.

    Prefer calling toml.load(str(path)) (this works for many toml libs and
    also triggers test mocks of toml.load). If that raises a TypeError
    (some implementations expect a file-like object), fall back to opening
    the file and passing the file object to toml.load.

    Raises FileNotFoundError if the path does not point to an existing file.
    """
    path = Path(filepath)
    if not check_file(path):
        raise FileNotFoundError(path)

    # First, try passing a string path to toml.load (compatible with test mocks)
    try:
        return toml.load(str(path))
    except TypeError:
        # Some toml implementations expect a file-object; open and pass file
        with path.open("r", encoding="utf-8") as fh:
            return toml.load(fh)


def load_toml_tuple(filepath: Path | str) -> Optional[Tuple[str, Any]]:
    """
    Convenience: for TOML files that contain a single top-level table,
    return (key, value) for the first top-level item.

    Returns:
        (key, value) tuple for the first top-level key, or None if the file
        contains no top-level mappings.
    """
    data = load_toml(filepath)
    if not isinstance(data, dict) or not data:
        return None
    first_key = next(iter(data))
    return first_key, data[first_key]
    #data_tuple = tuple(data.items())
    #return data_tuple

def check_for_null(data):
    # Check if the data is a nested dictionary or flat
    if all(isinstance(value, dict) for value in data.values()):
        # If the data has section headers (nested structure)
        for section_key, section in data.items():
            for key, value in section.items():
                # If the value is a string and equals "null", replace it with None
                if isinstance(value, str) and value.lower() == "null":
                    section[key] = None
                    data[section_key] = section
    else:
        # If the data is flat (no section headers)
        for key, value in data.items():
            # If the value is a string and equals "null", replace it with None
            if isinstance(value, str) and value.lower() == "null":
                data[key] = None

    return data

if "__main__" == __name__:
   filepath = r"C:\Users\user\Documents\pavlov\pavlov25\core\projects\Don-EvonikPAA-MemphisCellulose\configs\config_input_22February_PAA.toml"
   filepath = Path(os.path.normpath(filepath))
   t = load_toml(filepath)
   print(t)
