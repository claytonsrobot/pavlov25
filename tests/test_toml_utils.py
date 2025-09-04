# tests/test_toml_utils.py
import builtins
from pathlib import Path
import io

import pytest

import pavlov3d.toml_utils as tu


def test_check_file_not_exists(monkeypatch, tmp_path):
    """
    If neither os.path.isfile nor Path.is_file report existence,
    check_file should return False.
    """
    # Ensure os.path.isfile returns False
    monkeypatch.setattr(tu.os.path, "isfile", lambda _p: False)

    # Ensure Path.is_file returns False as well
    monkeypatch.setattr(Path, "is_file", lambda self: False)

    # Using non-existing path (tmp path is fine because we've mocked checks)
    result = tu.check_file(tmp_path / "no-such-file.toml")
    assert result is False


def test_load_toml_tuple_prefers_path_string(monkeypatch, tmp_path):
    """
    load_toml_tuple should call toml.load and return the top-level (key, value)
    pair for a single-key toml structure.
    """
    data = {"section": {"key1": "value1"}}

    # Pretend the file exists
    monkeypatch.setattr(tu.os.path, "isfile", lambda _p: True)
    monkeypatch.setattr(Path, "is_file", lambda self: True)

    # Patch toml.load to return our data (simulating toml.load(str(path)) behavior)
    monkeypatch.setattr(tu, "toml", type("T", (), {"load": lambda src: data}))

    result = tu.load_toml_tuple("dummy_path")
    # Expect a tuple pair (key, value) — i.e., ('section', {...})
    assert result == ("section", {"key1": "value1"})


def test_load_toml_falls_back_to_fileobj_on_typeerror(monkeypatch, tmp_path):
    """
    If toml.load raises TypeError when passed a string path, load_toml should
    open the file and call toml.load(fileobj).
    """
    data = {"section2": {"k": "v"}}
    dummy_file = tmp_path / "dummy.toml"
    dummy_file.write_text('section2 = { k = "v" }', encoding="utf-8")

    # ensure file existence checks pass
    monkeypatch.setattr(tu.os.path, "isfile", lambda p: True)
    monkeypatch.setattr(Path, "is_file", lambda self: True)

    # Create a toml-like loader that raises TypeError on str, but accepts file objects
    def fake_toml_load(arg):
        if isinstance(arg, str):
            raise TypeError("simulate toml lib that expects file-like object")
        # assume file-like: return desired data
        return data

    monkeypatch.setattr(tu, "toml", type("T", (), {"load": fake_toml_load}))

    result = tu.load_toml(str(dummy_file))
    assert result == data


def test_load_toml_raises_when_missing(monkeypatch, tmp_path):
    """
    If the file doesn't exist, load_toml should raise FileNotFoundError (or SystemExit
    depending on your check_file implementation). This test expects FileNotFoundError;
    if your implementation intentionally raises SystemExit change this assertion.
    """
    monkeypatch.setattr(tu.os.path, "isfile", lambda p: False)
    monkeypatch.setattr(Path, "is_file", lambda self: False)

    with pytest.raises((FileNotFoundError, SystemExit)):
        tu.load_toml(tmp_path / "nonexistent.toml")
